"""
At the top of your response, include this format, here is an example:
=====================================================
SecScanner AI
Python Security Analysis Report
=====================================================

Filename: vulnerable.py

Issues found: 4

Critical: 2
High: 2
Medium: 0
Low: 0

For each issue use this exact format:

----------
SEVERITY: [CRITICAL/HIGH/MEDIUM/LOW]
TYPE: [Vulnerability Name]
DESCRIPTION: [One sentence explaining the issue and the line number where it occurs]
IMPACT: [One sentence on potential damage]
FIX: [Code snippet only]
----------

Code:
{code}


Add a summary at the end of your response, including the total number of issues found and their severity levels.
Here is an example of the summary format:

Overall Security Score: 32/100

██████████░░░░


Grade:
D

Top Risks

✓ SQL Injection
✓ Command Injection
✓ Hardcoded Secrets

"""