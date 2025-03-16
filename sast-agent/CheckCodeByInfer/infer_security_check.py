import subprocess
import json
import os
import tempfile
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Vulnerability:
    """Class for representing a security vulnerability"""
    file: str
    line: int
    bug_type: str
    qualifier: str
    severity: str
    suggestion: str
    cwe: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert vulnerability to dictionary"""
        return {
            "file": self.file,
            "line": self.line,
            "bug_type": self.bug_type,
            "qualifier": self.qualifier,
            "severity": self.severity,
            "suggestion": self.suggestion,
            "cwe": self.cwe
        }

@dataclass
class SecurityReport:
    """Class for representing the security analysis report"""
    status: str
    issues: Dict[str, List[Vulnerability]]
    total_issues: int
    analysis_time: float
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary"""
        return {
            "status": self.status,
            "issues": {
                severity: [vuln.to_dict() for vuln in vulns]
                for severity, vulns in self.issues.items()
            },
            "total_issues": self.total_issues,
            "analysis_time": self.analysis_time
        }

def analyze_code_snippet(code_snippet: str, file_extension: str = ".cpp") -> SecurityReport:
    """
    Analyze code snippet for security vulnerabilities
    
    Args:
        code_snippet (str): Code snippet to analyze
        file_extension (str): File extension (.cpp, .c, .java, etc.)
        
    Returns:
        SecurityReport: Security analysis results
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
        return SecurityReport(
            status="error",
            issues={},
            total_issues=0,
            analysis_time=datetime.now().timestamp(),
        )

def run_infer_security_check(project_path: str, output_dir: str = "infer-out") -> SecurityReport:
    """
    Run Infer to check for security vulnerabilities in source code
    
    Args:
        project_path (str): Path to project to analyze
        output_dir (str): Directory to store analysis results
        
    Returns:
        SecurityReport: Security analysis results
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
            security_issues: Dict[str, List[Vulnerability]] = {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }
            
            for issue in results:
                severity = _determine_severity(issue)
                vulnerability = Vulnerability(
                    file=issue.get("file", ""),
                    line=issue.get("line", 0),
                    bug_type=issue.get("bug_type", ""),
                    qualifier=issue.get("qualifier", ""),
                    severity=severity,
                    suggestion=_get_security_suggestion(issue.get("bug_type", "")),
                    cwe=_map_to_cwe(issue.get("bug_type", ""))
                )
                security_issues[severity].append(vulnerability)
                
            return SecurityReport(
                status="success",
                issues=security_issues,
                total_issues=len(results),
                analysis_time=os.path.getmtime(report_path)
            )
        
        return SecurityReport(
            status="error",
            issues={},
            total_issues=0,
            analysis_time=datetime.now().timestamp()
        )
        
    except subprocess.CalledProcessError as e:
        return SecurityReport(
            status="error",
            issues={},
            total_issues=0,
            analysis_time=datetime.now().timestamp()
        )
    except Exception as e:
        return SecurityReport(
            status="error",
            issues={},
            total_issues=0,
            analysis_time=datetime.now().timestamp()
        )

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

def _map_to_cwe(bug_type: str) -> Optional[str]:
    """
    Map Infer bug type to CWE ID
    """
    cwe_mapping = {
        "null_dereference": "CWE-476",  # NULL Pointer Dereference
        "memory_leak": "CWE-401",       # Memory Leak
        "buffer_overflow": "CWE-120",    # Buffer Overflow
        "race_condition": "CWE-362",     # Race Condition
        "deadlock": "CWE-833",          # Deadlock
        "resource_leak": "CWE-772",      # Missing Release of Resource
        "use_after_free": "CWE-416",    # Use After Free
        "command_injection": "CWE-78",   # OS Command Injection
        "sql_injection": "CWE-89",      # SQL Injection
        "xss": "CWE-79"                 # Cross-site Scripting
    }
    return cwe_mapping.get(bug_type.lower())

def save_report_to_json(report: SecurityReport, output_file: str = "security_report.json") -> None:
    """
    Save report to JSON file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)

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
    print(json.dumps(results.to_dict(), indent=2))
