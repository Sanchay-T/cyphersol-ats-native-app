import pdfplumber
import pandas as pd
import PyPDF2

def extract_pdf_data(pdf_path):
    print(f"Testing PDF extraction: {pdf_path}")
    
    try:
        # Using pdfplumber
        print("\nAttempting extraction with pdfplumber...")
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Successfully opened PDF. Pages: {len(pdf.pages)}")
            
            all_tables = []
            for page_num, page in enumerate(pdf.pages):
                print(f"Processing page {page_num + 1}")
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table)
                    # Remove empty rows and columns
                    df = df.dropna(how='all').dropna(axis=1, how='all')
                    all_tables.append(df)
            
            if all_tables:
                final_df = pd.concat(all_tables, ignore_index=True)
                print("\nExtraction successful!")
                print("\nFirst few rows of extracted data:")
                print(final_df.head())
                
                # Save to CSV for inspection
                output_path = "extracted_data.csv"
                final_df.to_csv(output_path, index=False)
                print(f"\nSaved extracted data to {output_path}")
                
                return final_df
            else:
                print("No tables found in PDF")
                return None
                
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        return None

if __name__ == "__main__":
    pdf_path = r"C:\Users\Abcom\cyphersol-ats-native-app\HDFC (3).pdf"
    df = extract_pdf_data(pdf_path)