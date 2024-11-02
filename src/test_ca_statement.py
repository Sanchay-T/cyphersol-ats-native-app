from utils.CA_Statement_Analyzer import CABankStatement

def test_ca_statement():
    # Test parameters
    bank_names = ["HDFC"]
    pdf_paths = [r"C:\Users\Abcom\cyphersol-ats-native-app\HDFC (3).pdf"]
    pdf_passwords = [""]
    start_date = ["01/01/2024"]
    end_date = ["12/1/2024"]
    CA_ID = "TEST_ID_001"
    
    # Progress callback for debugging
    def debug_progress(current, total, info):
        print(f"Progress: {info} ({current}/{total})")
    
    progress_data = {
        'progress_func': debug_progress,
        'current_progress': 0,
        'total_progress': 100
    }
    
    try:
        # Initialize CABankStatement
        converter = CABankStatement(
            bank_names, 
            pdf_paths, 
            pdf_passwords, 
            start_date, 
            end_date, 
            CA_ID, 
            progress_data
        )
        
        # Try extraction
        print("Starting extraction...")
        result = converter.start_extraction()
        
        print("\nExtraction successful!")
        print("\nResult summary:")
        print(f"Number of banks processed: {result['summary']['total_banks']}")
        print(f"Processing period: {result['summary']['period']}")
        print(f"Status: {result['summary']['processing_status']}")
        
        return result
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return None

if __name__ == "__main__":
    test_ca_statement()