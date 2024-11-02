import os
import PyPDF2
import pdfplumber
import tabula

def validate_pdf(pdf_path):
    """
    Validates PDF file and returns best extraction method
    """
    results = {
        "valid": False,
        "best_method": None,
        "error": None,
        "info": {}
    }
    
    try:
        # Basic file checks
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("PDF file not found")
        
        # Try PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            results["info"]["pages"] = len(reader.pages)
            results["info"]["text_extractable"] = bool(reader.pages[0].extract_text())
        
        # Try tabula
        tables = tabula.read_pdf(pdf_path, pages='1')
        if tables and len(tables) > 0:
            results["best_method"] = "tabula"
            results["valid"] = True
            return results
        
        # Try pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            if pdf.pages[0].extract_table():
                results["best_method"] = "pdfplumber"
                results["valid"] = True
                return results
        
        raise ValueError("No suitable extraction method found")
        
    except Exception as e:
        results["error"] = str(e)
        return results

if __name__ == "__main__":
    pdf_path = r"C:\Users\Abcom\cyphersol-ats-native-app\HDFC (3).pdf"
    results = validate_pdf(pdf_path)
    print("PDF Validation Results:")
    print(f"Valid: {results['valid']}")
    print(f"Best Method: {results['best_method']}")
    print(f"Error: {results['error']}")
    print(f"Info: {results['info']}") 