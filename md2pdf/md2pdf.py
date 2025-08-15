#md2pdf.py

import os
import sys
from tkinter import Tk, filedialog
import pypandoc

def select_md_file():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a Markdown file",
        filetypes=[("Markdown files", "*.md")]
    )
    return file_path

def convert_md_to_pdf(md_file):
    pdf_file = os.path.splitext(md_file)[0] + ".pdf"

    # Custom LaTeX template to reduce margins and set landscape
    latex_preamble = r"""
    \usepackage[landscape,margin=0.5in]{geometry}
    \usepackage{hyperref}
    """

    try:
        output = pypandoc.convert_file(
            md_file,
            to="pdf",
            outputfile=pdf_file,
            extra_args=[
                "--pdf-engine=pdflatex",
                "--highlight-style=pygments",
                "--number-sections",
                "--listings",
                "--toc",
                "--metadata", "link-citations=true",
                "--variable", f"geometry:landscape",
                "--variable", f"geometry:margin=0.5in",
                "--variable", f"header-includes:{latex_preamble}"
            ]
        )
        print(f"✅ PDF saved as: {pdf_file}")
    except RuntimeError as e:
        print("❌ Error during conversion:")
        print(e)
        sys.exit(1)

def main():
    md_file = select_md_file()
    if md_file:
        convert_md_to_pdf(md_file)
    else:
        print("⚠️ No file selected.")

if __name__ == "__main__":
    main()
