"""Extraction de texte depuis un communiqué PDF."""
import argparse
from pathlib import Path
import pdfplumber

def extract_pdf_text(path_pdf):
    out=[]
    with pdfplumber.open(path_pdf) as pdf:
        for page in pdf.pages:
            out.append(page.extract_text() or '')
    return '\n'.join(out)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input', required=True); p.add_argument('--out', required=True); args=p.parse_args()
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(extract_pdf_text(args.input), encoding='utf-8')
if __name__=='__main__': main()
