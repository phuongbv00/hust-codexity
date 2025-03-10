from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from CheckCppFromSnippet import check_cpp_code
import json


app = FastAPI()


def map_cppcheck_to_cwe(cppcheck_id):
    """
    Maps Cppcheck IDs to CWE IDs (this is a simplified example).

    Args:
        cppcheck_id: The Cppcheck ID (e.g., "uninitVariable").

    Returns:
        The corresponding CWE ID or None if not found.
    """
    # This is a very basic mapping. A more complete mapping would be
    # much larger.
    cwe_mapping = {
        "uninitVariable": "CWE-457",  # Use of Uninitialized Variable
        "arrayIndexOutOfBounds": "CWE-129",  # Improper Validation of Array Index
        # Add more mappings as needed...
    }
    return cwe_mapping.get(cppcheck_id)


class CodeSnippet(BaseModel):
    code: str


@app.post("/analyze-code")
async def analyze_code(code_snippet: CodeSnippet):
    """
    API endpoint to analyze C++ code snippets for vulnerabilities.
    """
    try:
        # Run Cppcheck analysis
        report = check_cpp_code(code_snippet.code)

        if report is None:
            return {"vulnerabilities": []}

        # Format the report to match the desired API response
        vulnerabilities = []
        for error in report["errors"]:
            vulnerability = {
                "cwe": map_cppcheck_to_cwe(error["id"]),  # Map to CWE
                "message": error["message"],
                "location": {
                    "line": error["location"]["line"],
                    "column": error["location"]["column"],
                    "file": error["location"]["file"]
                }
            }
            vulnerabilities.append(vulnerability)

        return {"vulnerabilities": vulnerabilities}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")