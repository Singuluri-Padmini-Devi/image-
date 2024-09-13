import fitz  # PyMuPDF
import pdfplumber
import csv
import io

def extract_text_pymupdf(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    text = ''
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text with PyMuPDF: {e}")
    return text

def extract_text_and_tables_pdfplumber(pdf_path):
    """Extract text and tables from PDF using pdfplumber."""
    text = ''
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                
                # Extract tables
                page_tables = page.extract_tables()
                for table in page_tables:
                    tables.append(table)
    except Exception as e:
        print(f"Error extracting text and tables with pdfplumber: {e}")
    return text, tables

def save_tables_as_csv(tables, filename):
    """Save extracted tables as a CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for table in tables:
                for row in table:
                    writer.writerow(row)
                writer.writerow([])  # Add an empty line between tables
    except Exception as e:
        print(f"Error saving tables to CSV: {e}")

def extract_text_from_pdf(pdf_path):
    """Extract text and tables from PDF using both PyMuPDF and pdfplumber."""
    text_pymupdf = extract_text_pymupdf(pdf_path)
    text_pdfplumber, tables = extract_text_and_tables_pdfplumber(pdf_path)

    # Combine the results from both methods
    combined_text = f"--- PyMuPDF Extraction ---\n{text_pymupdf.strip()}\n\n--- pdfplumber Extraction ---\n{text_pdfplumber.strip()}"
    
    if not combined_text.strip():
        combined_text = "No text extracted from the PDF."
    
    return combined_text, tables

def main():
    pdf_path = r"C:\Users\User\Downloads\text_tab.pdf"  # Update with your PDF path

    print("Extracting text and tables from PDF...")
    combined_text, tables = extract_text_from_pdf(pdf_path)
    
    # Print the extracted text
    print(combined_text)
    
    # Save the extracted text to a file
    with open('extracted_text_output.txt', 'w', encoding='utf-8') as f:
        f.write(combined_text)
    
    # Save the extracted tables to a CSV file
    save_tables_as_csv(tables, 'tables_output.csv')

if __name__ == '__main__':
    main()
