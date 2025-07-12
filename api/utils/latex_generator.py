# utils/pdf_generator.py

import os
import subprocess
import tempfile
from django.http import FileResponse
import logging
from django.http import HttpResponse, JsonResponse
import tempfile, subprocess, os, shutil
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

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
    

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_path = os.path.join(temp_dir, "document.tex")
            pdf_path = os.path.join(temp_dir, "document.pdf")
            logo_path = os.path.join(temp_dir, "logo.png")

            # Write .tex file
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(generate_latex(json_data))

            # Copy logo file safely
            logo_source = os.path.join(settings.BASE_DIR, "static/logo.png")
            if not os.path.exists(logo_source):
                logger.error("❌ logo.png not found at: %s", logo_source)
                return JsonResponse({"error": "logo.png not found"}, status=500)

            shutil.copy(logo_source, logo_path)

            # Check if pdflatex is available
            if shutil.which("pdflatex") is None:
                logger.error("❌ pdflatex not found in environment")
                return JsonResponse({"error": "PDF generator not installed"}, status=500)

            # Run pdflatex
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "document.tex"],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if not os.path.exists(pdf_path):
                logger.error("❌ pdflatex output:\n%s", result.stdout.decode())
                return JsonResponse({"error": "PDF compilation failed"}, status=500)

            return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename="generated_exam.pdf")

    except Exception as e:
        logger.exception("Unhandled PDF error")
        return JsonResponse({"error": str(e)}, status=500)


# def generate_pdf_response_from_json(json_data):
#     with tempfile.TemporaryDirectory() as temp_dir:
#         tex_path = os.path.join(temp_dir, "document.tex")
#         pdf_path = os.path.join(temp_dir, "document.pdf")
#         logo_path = os.path.join(temp_dir, "logo.png")

#         # Write LaTeX file
#         with open(tex_path, "w", encoding="utf-8") as f:
#             f.write(generate_latex(json_data))

#         # Copy logo.png (you can adjust the path to your static location)
#         from django.conf import settings
#         import shutil
#         shutil.copy(os.path.join(settings.BASE_DIR, "static/logo.png"), logo_path)


#         # Compile to PDF
#         try:
#             # Compile LaTeX (don't fail on warnings)
#             result = subprocess.run(
#                 ["pdflatex", "-interaction=nonstopmode", "document.tex"],
#                 cwd=temp_dir,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#             )

#             if not os.path.exists(pdf_path):
#                 logger.error("❌ PDFLaTeX Error:\n%s", result.stdout.decode())
#                 raise Exception("PDF compilation failed")



#         except subprocess.CalledProcessError:
#             raise Exception("PDF compilation failed")

#         # Return the compiled PDF as response
#         return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename="generated_exam.pdf")
