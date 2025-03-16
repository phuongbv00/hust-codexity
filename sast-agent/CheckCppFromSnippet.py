import subprocess
import os
import json
import sys
import tempfile
import shutil


def check_cpp_code(cpp_code):
    """
    Checks a C++ code snippet for bugs using Cppcheck.

    Args:
        cpp_code: The C++ code snippet as a string.

    Returns:
        A dictionary containing the Cppcheck report, or None if an error occurred.
    """

    # Check if the code snippet already has #include <iostream> and a main function
    if "#include <iostream>" not in cpp_code:
        cpp_code = "#include <iostream>\n" + cpp_code

    if "int main()" not in cpp_code:
        cpp_code = "int main() {\n" + cpp_code + "\nreturn 0;\n}"

    with tempfile.TemporaryDirectory() as temp_dir:
        cpp_file_path = os.path.join(temp_dir, "temp.cpp")

        # Write the C++ code snippet to a temporary file.
        with open(cpp_file_path, "w") as f:
            f.write(cpp_code)

        if shutil.which("cppcheck") is None:
            print("Error: Cppcheck executable not found in PATH. Please install Cppcheck or add it to your PATH.")
            return None

        try:
            # Add cppcheck's directory to the PATH temporarily (if needed).
            # Change this path to the actual directory if it's different.
            cppcheck_dir = "C:/Program Files/Cppcheck"  # Or wherever cppcheck.exe is
            if cppcheck_dir:
                if os.path.exists(cppcheck_dir):
                    os.environ["PATH"] = cppcheck_dir + os.pathsep + os.environ["PATH"]

            # Construct the Cppcheck command.
            # -j4: use 4 threads to check. You can adjust it.
            # --xml: Output in XML format
            # --output-file=cppcheck_report.xml : output into a file.
            # The final argument is the path to the cpp file.

            command = [
                "cppcheck",
                "-j4",
                "--xml",
                "--output-file=cppcheck_report.xml",
                "--check-level=exhaustive",
                cpp_file_path
            ]

            # Execute Cppcheck and capture the output.
            process = subprocess.run(
                command, capture_output=True, text=True, check=True
            )

            # Check if the output file was created.
            if os.path.exists("cppcheck_report.xml"):
                # Read the xml file, then parse it into json file.
                xml_content = ""
                with open("cppcheck_report.xml", "r") as f:
                    xml_content = f.read()

                json_content = xml_to_json(xml_content)
                os.remove("cppcheck_report.xml")
                return json_content
            else:
                print(
                    f"Error: An error has occured. file cppcheck_report.xml does not exists")
                print(process.stderr)
                return None

        except subprocess.CalledProcessError as e:
            print(f"Error: Cppcheck failed with exit code {e.returncode}")
            print(f"Cppcheck stderr: {e.stderr}")
            return None
        except FileNotFoundError:
            print(
                "Error: Cppcheck not found. Please ensure it is installed and in your PATH.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


def xml_to_json(xml_string):
    """
    Converts a Cppcheck XML string to a JSON-like dictionary.

    Args:
        xml_string: The XML string from Cppcheck.

    Returns:
        A dictionary representing the Cppcheck report or None if there are no error.
    """
    import xml.etree.ElementTree as ET

    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

    results = {"file": "", "errors": []}
    errors = []

    # check if there is an errors tag.
    if not root.find('errors'):
        return None

    for error_elem in root.findall(".//error"):
        error = {}
        error["id"] = error_elem.get("id")
        error["message"] = error_elem.get("msg")
        error["severity"] = error_elem.get("severity")

        location = {}
        location_elem = error_elem.find("location")
        if location_elem is not None:
            location["line"] = int(location_elem.get("line", 0))
            location["column"] = int(location_elem.get("column", 0))
            location["file"] = location_elem.get("file")

        error["location"] = location
        errors.append(error)


    results["file"] = xml_string.split("file=\"")[1].split("\"")[0]
    results["errors"] = errors

    return results


# --- SAST execution starts here ---
if __name__ == "__main__":
    # Example Usage with Code Snippet
    cpp_code_snippet = """
        int x = 10;
        int y; // uninitialized
        std::cout << y; // possible bug
    """

    report = check_cpp_code(cpp_code_snippet)

    if report:
        print(json.dumps(report, indent=2))
        print("Cppcheck found", len(report["errors"]), "problems")
    else:
        print("Cppcheck found no problems or an error occurred.")