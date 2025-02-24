import fitz  # PyMuPDF for PDF text extraction
import re
import spacy
import nltk
from textblob import TextBlob

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Keywords for investment-related information
KEY_SECTIONS = [
    "growth prospects", "future outlook", "market trends", 
    "business risks", "financial outlook", "key triggers",
    "revenue forecast", "earnings report"
]

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def extract_key_sections(text):
    """Extracts key sections related to investment analysis."""
    extracted_data = {}
    lines = text.split("\n")
    
    current_section = None
    for line in lines:
        line_lower = line.lower()
        for section in KEY_SECTIONS:
            if section in line_lower:
                current_section = section
                extracted_data[current_section] = []
        
        if current_section:
            extracted_data[current_section].append(line.strip())
    
    return extracted_data

def extract_financial_figures(text):
    """Extracts financial figures (revenues, percentages, and currency values)."""
    financial_data = re.findall(r"\$\d+(?:,\d{3})*(?:\.\d+)?|\d+%", text)
    return financial_data

def summarize_text(text):
    """Summarizes extracted key sections using NLP techniques."""
    blob = TextBlob(text)
    return blob.sentences[:5]  # Return the first 5 meaningful sentences

def analyze_pdf(pdf_path):
    """Main function to analyze the PDF and extract key investment insights."""
    text = extract_text_from_pdf(pdf_path)
    key_sections = extract_key_sections(text)
    financial_data = extract_financial_figures(text)

    insights = {}
    for section, content in key_sections.items():
        section_text = " ".join(content)
        summary = summarize_text(section_text)
        insights[section] = summary

    return {
        "financial_data": financial_data,
        "insights": insights
    }

if __name__ == "__main__":
    pdf_path = "company_report.pdf"  # Change to your PDF file
    report = analyze_pdf(pdf_path)

    print("=== Financial Figures Extracted ===")
    print(report["financial_data"])

    print("\n=== Key Investment Insights ===")
    for section, summary in report["insights"].items():
        print(f"\n[{section.upper()}]")
        for sentence in summary:
            print(f"- {sentence}")
