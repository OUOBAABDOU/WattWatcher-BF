"""OCR des communiqués publiés sous forme d'image. Nécessite Tesseract OCR."""
import argparse
from pathlib import Path
from PIL import Image
import pytesseract

def extract_image_text(path_image, lang='fra'):
    return pytesseract.image_to_string(Image.open(path_image), lang=lang)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input', required=True); p.add_argument('--out', required=True); p.add_argument('--lang', default='fra'); args=p.parse_args()
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(extract_image_text(args.input,args.lang), encoding='utf-8')
if __name__=='__main__': main()
