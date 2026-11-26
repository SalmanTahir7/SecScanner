from pathlib import Path
from jinja2 import Environment, FileSystemLoader



def generate_html_report(filename, findings):

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template("report.html")

    html = template.render(
        filename=filename,
        findings=findings
    )

    reports = Path("reports")
    reports.mkdir(exist_ok=True)

    output = reports / "report.html"

    output.write_text(html)

    print(f"\nHTML report saved to {output}")