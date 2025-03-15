import subprocess
import json
import os
import tempfile
from typing import Dict, List, Optional

def analyze_code_snippet(code_snippet: str, file_extension: str = ".cpp") -> Dict:
    """
    Analyze code snippet for security vulnerabilities
    
    Args:
        code_snippet (str): Code snippet to analyze
        file_extension (str): File extension (.cpp, .c, .java, etc.)
        
    Returns:
        Dict: Security analysis results
    """
    try:
        # Create temporary directory to store code
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary file with code
            temp_file = os.path.join(temp_dir, f"temp_code{file_extension}")
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(code_snippet)
            
            # Create simple Makefile
            makefile_content = f"all:\n\tclang{file_extension} -c {temp_file}"
            with open(os.path.join(temp_dir, "Makefile"), "w") as f:
                f.write(makefile_content)
            
            # Run security analysis
            return run_infer_security_check(temp_dir)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error analyzing code snippet: {str(e)}"
        }

def run_infer_security_check(project_path: str, output_dir: str = "infer-out") -> Dict:
    """
    Run Infer to check for security vulnerabilities in source code
    
    Args:
        project_path (str): Path to project to analyze
        output_dir (str): Directory to store analysis results
        
    Returns:
        Dict: Security analysis results
    """
    try:
        # Delete old output directory if exists
        if os.path.exists(output_dir):
            subprocess.run(["rm", "-rf", output_dir], check=True)
            
        # Run Infer
        subprocess.run([
            "infer",
            "run",
            "--bufferoverrun",  # Check for buffer overflow
            "--racerd",         # Check for race conditions
            "--starvation",     # Check for deadlocks
            "--pulse",          # Check for memory safety
            "--null-safety",    # Check for null pointers
            "--taint-analysis", # Check for taint analysis
            "-o", output_dir,   # Output directory
            "--",              
            "make"              # Build command
        ], cwd=project_path, check=True)
        
        # Read results from report.json
        report_path = os.path.join(output_dir, "report.json")
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                results = json.load(f)
                
            # Classify issues by severity
            security_issues = {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }
            
            for issue in results:
                severity = _determine_severity(issue)
                security_issues[severity].append({
                    "file": issue.get("file"),
                    "line": issue.get("line"),
                    "bug_type": issue.get("bug_type"),
                    "qualifier": issue.get("qualifier"),
                    "severity": severity,
                    "suggestion": _get_security_suggestion(issue.get("bug_type", ""))
                })
                
            return {
                "status": "success",
                "issues": security_issues,
                "total_issues": len(results),
                "analysis_time": os.path.getmtime(report_path)
            }
        
        return {
            "status": "error",
            "message": "Report file not found"
        }
        
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Error running Infer: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unknown error: {str(e)}"
        }

def _determine_severity(issue: Dict) -> str:
    """
    Determine severity of the issue
    """
    bug_type = issue.get("bug_type", "").lower()
    
    # Critical severity issues
    if any(critical in bug_type for critical in [
        "null_dereference", 
        "memory_leak", 
        "buffer_overflow",
        "command_injection",
        "sql_injection",
        "xss"
    ]):
        return "critical"
    
    # High severity issues
    elif any(high in bug_type for high in [
        "race_condition", 
        "deadlock", 
        "resource_leak",
        "use_after_free"
    ]):
        return "high"
    
    # Medium severity issues
    elif any(medium in bug_type for medium in [
        "uninitialized_value", 
        "parameter_not_null_checked",
        "integer_overflow"
    ]):
        return "medium"
    
    # Low severity issues
    else:
        return "low"

def _get_security_suggestion(bug_type: str) -> str:
    """
    Get remediation suggestion based on bug type
    """
    suggestions = {
        "null_dereference": "Check for null pointer before use",
        "memory_leak": "Free memory after use",
        "buffer_overflow": "Check buffer size and limit input",
        "race_condition": "Use mutex or locks for synchronization",
        "deadlock": "Review and reorder lock acquisition",
        "resource_leak": "Ensure resources are freed in all paths",
        "use_after_free": "Don't use pointers after freeing",
        "command_injection": "Validate and sanitize user input",
        "sql_injection": "Use prepared statements",
        "xss": "Escape or sanitize user input"
    }
    return suggestions.get(bug_type.lower(), "Review and fix according to guidelines")

def save_report_to_json(report: Dict, output_file: str = "security_report.json") -> None:
    """
    Save report to JSON file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Example usage with code snippet
    code_snippet = """
    #include <stdio.h>
    #include <stdlib.h>
    
    void vulnerable_function(char* input) {
        char buffer[10];
        strcpy(buffer, input);  // Potential buffer overflow
        
        char* ptr = NULL;
        printf("%s", ptr);      // Null pointer dereference
        
        char* mem = malloc(10);
        // Memory leak - no free
    }
    
    int main() {
        vulnerable_function("very long input string");
        return 0;
    }
    """
    
    # Analyze code snippet
    results = analyze_code_snippet(code_snippet, ".c")
    
    # Save results to JSON file
    save_report_to_json(results)
    
    # Print results to screen
    print(json.dumps(results, indent=2))
