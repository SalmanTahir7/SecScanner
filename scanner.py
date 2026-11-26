import os
import sys
from dotenv import load_dotenv
from colorama import init, Fore, Style
import google.genai as genai
import json
from report_generator import generate_html_report
import argparse

init(autoreset=True)  # Initialize colorama

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("file")

parser.add_argument(
    "--html",
    action="store_true",
    help="Generate HTML report"
)

args = parser.parse_args()


api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

security_prompt = """
You are a cybersecurity expert performing static analysis on Python code.
Analyze this code for security vulnerabilities. Be concise.

Return ONLY valid JSON.

Do not include markdown.
Do not include triple backticks.
Do not include explanations outside the JSON.

Return this exact schema:

{{
  "filename": "{filename}",
  "summary": {{
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "score": 100,
    "grade": "A"
  }},
  "findings": [
    {{
      "severity": "CRITICAL",
      "type": "SQL Injection",
      "line": 42,
      "description": "User input is directly used in a database query.",
      "impact": "An attacker could manipulate queries and access unauthorized data.",
      "fix": "Use parameterized queries instead of string concatenation."
    }}
  ]
}}

Analyze this code:

{code}
"""

def create_score_bar(score, length=20):
    filled = int((score / 100) * length)
    empty = length - filled

    bar = "█" * filled + "░" * empty

    return bar

def calculate_score(findings):
    score = 100

    penalties = {
        "CRITICAL": 25,
        "HIGH": 15,
        "MEDIUM": 8,
        "LOW": 3
    }

    for finding in findings:
        severity = finding["severity"]
        score -= penalties.get(severity, 0)

    return max(score, 0)

def print_report(data):
    print("=" * 60)
    print("SecScanner AI")
    print("Python Security Analysis Report")
    print("=" * 60)

    print(f"Filename: {data['filename']}")
    print()

    print(f"Issues Found: {len(data['findings'])}")
    print(f"Critical: {Fore.RED}{Style.BRIGHT}{summary['critical']}{Style.RESET_ALL}")
    print(f"High: {Fore.YELLOW}{Style.BRIGHT}{summary['high']}{Style.RESET_ALL}")
    print(f"Medium: {Fore.BLUE}{Style.BRIGHT}{summary['medium']}{Style.RESET_ALL}")
    print(f"Low: {Fore.GREEN}{Style.BRIGHT}{summary['low']}{Style.RESET_ALL}")
    print()

    for finding in data["findings"]:

        print("-" * 50)

        severity = finding["severity"]

        if severity == "CRITICAL":
            severity = f"{Fore.RED}{Style.BRIGHT}{severity}{Style.RESET_ALL}"

        elif severity == "HIGH":
            severity = f"{Fore.YELLOW}{Style.BRIGHT}{severity}{Style.RESET_ALL}"

        elif severity == "MEDIUM":
            severity = f"{Fore.BLUE}{severity}{Style.RESET_ALL}"

        elif severity == "LOW":
            severity = f"{Fore.GREEN}{severity}{Style.RESET_ALL}"

        severity = finding.get("severity", "Unknown")

        if severity == "CRITICAL":
            severity = f"{Fore.RED}{Style.BRIGHT}{severity}{Style.RESET_ALL}"
        
        elif severity == "HIGH":
            severity = f"{Fore.YELLOW}{Style.BRIGHT}{severity}{Style.RESET_ALL}"
        
        elif severity == "MEDIUM":
            severity = f"{Fore.BLUE}{Style.BRIGHT}{severity}{Style.RESET_ALL}"
        
        elif severity == "LOW":
            severity = f"{Fore.GREEN}{Style.BRIGHT}{severity}{Style.RESET_ALL}"

        score = calculate_score(data["findings"])
        
        print(f"Severity: {severity}")
        print(f"Type: {finding.get('type', 'Unknown')}")
        print(f"Line: {finding.get('line', 'Unknown')}")
        print(f"Description: {finding.get('description', 'No description provided')}")
        print(f"Impact: {finding.get('impact', 'No impact provided')}")
        print(f"Fix:\n{finding.get('fix', 'No fix provided')}")

    print()
    print("=" * 60)
    
    print(
        f"Overall Security Score: {score}/100"
    )
    
    print(create_score_bar(score))
    
    print()
    
    print(f"Grade: {grade}")
    
    print("=" * 60)


# File path from command line: python scanner.py <file_path>
if len(sys.argv) < 2:
    print("Usage: python scanner.py <file_path>")
    sys.exit(1)

code_path = sys.argv[1]
with open(code_path, "r") as f:
    code = f.read()

prompt = security_prompt.replace(
    "{code}",
    code
).replace(
    "{filename}",
    os.path.basename(code_path)
)
# .format(code=code, filename=os.path.basename(code_path))

try:
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite', contents=prompt
    )
    data = json.loads(response.text)
    summary = data["summary"]
    score = summary.get("score", 0)
    grade = summary.get("grade", "N/A")
    findings = data["findings"]
    print_report(data)
    if args.html:
     generate_html_report(
     filename=code_path,
     findings=findings
     )
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
