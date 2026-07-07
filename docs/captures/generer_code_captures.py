from pygments import highlight
from pygments.lexers import PythonLexer, SqlLexer
from pygments.formatters import ImageFormatter
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Custom style for code highlighting
class CodeStyle(Style):
    styles = {
        Comment:                '#6a9955',
        Keyword:                '#569cd6',
        Name:                   '#9cdcfe',
        Name.Function:          '#dcdcaa',
        Name.Class:             '#4ec9b0',
        String:                 '#ce9178',
        Number:                 '#b5cea8',
        Operator:               '#d4d4d4',
        Error:                  '#f44747',
    }

# Configuration
CAPTURES_DIR = Path(__file__).parent
ROOT_DIR = CAPTURES_DIR.parent.parent

# Code files to capture
CODE_FILES = [
    ("21_app_principal.png", ROOT_DIR / "backend" / "app.py", "python"),
    ("22_scrape_medias.png", ROOT_DIR / "ingestion" / "scrape_medias.py", "python"),
    ("23_clean_coupures.png", ROOT_DIR / "processing" / "clean_coupures.py", "python"),
    ("24_train_model.png", ROOT_DIR / "ml" / "train_model.py", "python"),
    ("25_schema_sql.png", ROOT_DIR / "database" / "schema.sql", "sql"),
]

def capture_code(filename, file_path, language):
    """Capture a code file as an image"""
    try:
        if not file_path.exists():
            print(f"  [ERREUR] {filename}: Fichier non trouvé {file_path}")
            return
        
        # Read the code
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Limit to first 50 lines for readability
        lines = code.split('\n')[:50]
        code = '\n'.join(lines)
        
        # Select lexer
        if language == "python":
            lexer = PythonLexer()
        elif language == "sql":
            lexer = SqlLexer()
        else:
            lexer = PythonLexer()
        
        # Create formatter
        formatter = ImageFormatter(
            style=CodeStyle,
            line_numbers=True,
            line_number_bg='#1e1e1e',
            line_number_fg='#858585',
            bg='#1e1e1e',
            font_size=10,
            line_number_chars=3,
            margin=10,
            padding=10,
        )
        
        # Highlight code
        output_path = CAPTURES_DIR / filename
        with open(output_path, 'wb') as f:
            highlight(code, lexer, formatter, f)
        
        print(f"  [OK] {filename}")
    except Exception as e:
        print(f"  [ERREUR] {filename}: {e}")

def main():
    """Main function to capture all code files"""
    print("=== Génération des captures de code source ===")
    
    for filename, file_path, language in CODE_FILES:
        capture_code(filename, file_path, language)
    
    print("\n=== Génération terminée ===")
    print(f"Captures sauvegardées dans : {CAPTURES_DIR}")

if __name__ == "__main__":
    main()
