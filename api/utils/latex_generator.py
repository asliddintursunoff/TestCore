# utils/pdf_generator.py

import os
import subprocess
import tempfile
from django.http import FileResponse


def generate_latex(json_data):
    header = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage[a4paper, margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{multicol}
\usepackage{fancyhdr}
\usepackage{enumitem}
\usepackage{tikz}
\setlength{\columnseprule}{0.4pt}  % Vertical line between columns
\setlength{\columnsep}{1cm}        % Column spacing

\pagestyle{fancy}
\fancyhf{}
\rhead{Page \thepage}
\lhead{""" + json_data["subjects"][0]["subject_name"] + r"""}

\begin{document}
\begin{center}
    {\LARGE \textbf{""" + json_data["test_name"] + r"""}} \\
    \vspace{0.2cm}

    \vspace{0.3cm}
    \includegraphics[width=3cm]{logo.png}
\end{center}
\vspace{0.5cm}
\begin{multicols}{2}
\raggedcolumns

"""




    body = ""
    q_num = 1
    for subject in json_data["subjects"]:
        for q in subject["questions"]:
            body += f"\\noindent \\textbf{{{q_num}.}} {q['question']}\\\\\n"

            body += "\\begin{itemize}[leftmargin=1.8em, itemsep=0.2em, labelsep=0.4em]\n"
            for idx, ans in enumerate(q["answers"]):
                label = chr(65 + idx)  # A, B, C...
                body += f"  \\item[\\textcircled{{\\scriptsize {label}}}] {ans['answer']}\n"
            body += "\\end{itemize}\n"
            body += "\\vspace{0.4cm}\n"
            q_num += 1

    footer = r"""
\end{multicols}
\end{document}
"""
    return header + body + footer



def generate_pdf_response_from_json(json_data):
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, "document.tex")
        pdf_path = os.path.join(temp_dir, "document.pdf")
        logo_path = os.path.join(temp_dir, "logo.png")

        # Write LaTeX file
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(generate_latex(json_data))

        # Copy logo.png (you can adjust the path to your static location)
        from django.conf import settings
        import shutil
        shutil.copy(os.path.join(settings.BASE_DIR, "static/logo.PNG"), logo_path)

        # Compile to PDF
        try:
            # Compile LaTeX (don't fail on warnings)
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "document.tex"],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if not os.path.exists(pdf_path):
                # Optional: print output to diagnose why it failed
                print("❌ PDFLaTeX Error Output:\n", result.stdout.decode())
                raise Exception("PDF compilation failed")


        except subprocess.CalledProcessError:
            raise Exception("PDF compilation failed")

        # Return the compiled PDF as response
        return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename="generated_exam.pdf")
