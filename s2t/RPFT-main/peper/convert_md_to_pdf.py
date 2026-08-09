import subprocess
import sys
import os
import argparse

def convert_md_to_pdf(input_file, output_file=None):
    """
    Converts a Markdown file to PDF using Pandoc with XeLaTeX engine.
    Ensures correct rendering of Cyrillic characters, LaTeX formulas, and code blocks.
    """
    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.pdf"

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    # Check for pandoc
    try:
        subprocess.run(["pandoc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("Error: 'pandoc' is not installed. Please install pandoc.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: Failed to run pandoc.")
        sys.exit(1)

    # Check for xelatex
    try:
        subprocess.run(["xelatex", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("Error: 'xelatex' is not installed. Please install texlive-xetex.")
        sys.exit(1)

    print(f"Converting '{input_file}' to '{output_file}'...")

    # Construct the pandoc command
    # -V mainfont="DejaVu Sans" : Sets the main font to one that supports Cyrillic
    # -V monofont="DejaVu Sans Mono" : Sets the monospaced font for code blocks
    # --pdf-engine=xelatex : Uses XeLaTeX which handles UTF-8 and fonts better than pdflatex
    # --highlight-style=tango : Sets a nice color scheme for code blocks
    # -V geometry:margin=2cm : Sets page margins
    # -V colorlinks=true : Makes links colored and clickable
    # -V linkcolor=blue : Sets link color
    # -V urlcolor=blue : Sets URL color
    command = [
        "pandoc",
        input_file,
        "-o", output_file,
        "--pdf-engine=xelatex",
        "-V", "mainfont=DejaVu Sans",
        "-V", "monofont=DejaVu Sans Mono",
        "-V", "geometry:margin=2cm",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue",
        "--highlight-style=tango"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("Conversion successful!")
            print(f"Output saved to: {os.path.abspath(output_file)}")
        else:
            print("Conversion failed!")
            print("Pandoc stderr:")
            print(result.stderr)
            sys.exit(result.returncode)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Markdown to PDF with LaTeX and code support.",
    )
    # Делаем input_file обязательным позиционным аргументом
    parser.add_argument(
        "input_file",
        help="Path to the input Markdown file (required)",
    )
    # output_file остаётся необязательным; если не указан, берётся имя input_file с расширением .pdf
    parser.add_argument(
        "output_file",
        nargs="?",
        help="Path to the output PDF file (optional)",
    )

    args = parser.parse_args()

    convert_md_to_pdf(args.input_file, args.output_file)
