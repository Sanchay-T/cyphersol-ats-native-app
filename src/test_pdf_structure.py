import pdfplumber
import pandas as pd

def analyze_pdf_structure(pdf_path):
    print(f"Analyzing PDF: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"\nTotal pages: {len(pdf.pages)}")
            
            # Analyze first page
            first_page = pdf.pages[0]
            
            # Get page dimensions
            print(f"\nPage dimensions: {first_page.width} x {first_page.height}")
            
            # Extract and show text
            text = first_page.extract_text()
            print("\nFirst 200 characters of text:")
            print(text[:200] if text else "No text found")
            
            # Try to extract table
            table = first_page.extract_table()
            if table:
                print("\nTable structure found!")
                df = pd.DataFrame(table)
                print("\nColumn count:", len(df.columns))
                print("First few rows:")
                print(df.head())
            else:
                print("\nNo table structure found")
                
            # Extract words with positions
            words = first_page.extract_words()
            print(f"\nFound {len(words)} words on first page")
            if words:
                print("Sample words with positions:")
                for word in words[:5]:
                    print(f"Word: {word['text']}, Position: ({word['x0']}, {word['top']})")
                    
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    pdf_path = r"C:\Users\Abcom\cyphersol-ats-native-app\HDFC (3).pdf"
    analyze_pdf_structure(pdf_path) 