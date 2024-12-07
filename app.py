import streamlit as st
from utils.pdf_processing import extract_text_from_pdf
from utils.openai_api import analyze_text_with_openai
from docx import Document
import re
import difflib
import pytesseract
from PIL import Image
import requests
from io import BytesIO

import PyPDF2
# Function to check assignment doability
def check_assignment_doability(assignment_text, curriculum_text):
    sm = difflib.SequenceMatcher(None, assignment_text, curriculum_text)
    return sm.ratio() * 100

def analyze_doability_with_prompt(assignment_text, curriculum_text):
    prompt = f"""
Please analyze the alignment between the following assignment and the provided curriculum. Assess how closely the content of the assignment matches the topics and objectives outlined in the curriculum. Consider both **exact matches** of concepts and topics as well as **closely related content** that may not be explicitly mentioned in the curriculum but could be inferred from the curriculum's scope or related topics.

Assignment:
{assignment_text}

Curriculum:
{curriculum_text}

Provide a detailed analysis including:
- **Matching Percentage**: Displayed in large text, considering both exact matches and closely related core concepts.
- **Short Bullet Points**:
  - List of **exact matches** between the assignment and curriculum (concepts, topics, skills).
  - List of **closely related content**: Topics from the assignment that are not explicitly covered in the curriculum but are relevant based on the curriculum's scope.
  - List of **non-matching concepts**: Points that the assignment covers but are not present or are weakly covered in the curriculum.

The analysis should provide a percentage match, along with short bullet points to clearly indicate which concepts in the assignment are covered in the curriculum and which are not, helping to assess if the assignment is doable based on what has been taught.

"""
    response = analyze_text_with_openai(prompt)
    
    # Extract matching percentage from the response
    match_percentage = re.search(r'(\d{1,3})%', response)  # Captures percentages
    
    # Extract Exact Matches and Not Exact Matches
    exact_matches = re.findall(r'Exact Matches: ([^\n]*)', response)
    not_exact_matches = re.findall(r'Not Exact Matches: ([^\n]*)', response)
    
    # Return response, matching percentage, exact matches, and not exact matches
    return response, match_percentage.group(0) if match_percentage else "0%", exact_matches, not_exact_matches

# Function to extract text from DOCX files
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to extract text from image using OCR
def extract_text_from_image(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text

# Function to handle different file types and extract text
def extract_text_from_file(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        return extract_text_from_image(uploaded_file)
    else:
        return None

def main():
    st.set_page_config(page_title="Document Generator & Doability Checker", layout="wide")

    # Get the current page from URL query parameters or set it to the default page
    query_params = st.query_params
    current_page = query_params.get("page", "Doability")  # Default to "Doability" page

    # Display the correct page based on the current_page
    if current_page == "Doability":
        doability_checker()

def doability_checker():
    st.header("Assignment Doability Checker")
    
    # File upload for assignment (supporting multiple file types)
    uploaded_file = st.file_uploader("Upload an Assignment file (PDF, DOCX, Image)", type=["pdf", "docx", "jpg", "jpeg", "png"], key="assignment")
    
    # Define only the Nxtwave Course curriculum
    curriculum_options = {
        "Nxtwave Course": "curriculums/nxtwave_course.pdf"
    }
    
    if uploaded_file is not None:
        # Step 1: Extract assignment text based on file type
        with st.spinner('Reading assignment file...'):
            assignment_text = extract_text_from_file(uploaded_file)
            if assignment_text:
                st.success("Assignment file read successfully!")
            else:
                st.error("Unsupported file type or error extracting text from file.")
                return
        
        if st.button("Check Doability"):
            results = []
            with st.spinner('Checking assignment doability...'):
                for curriculum_name, curriculum_path in curriculum_options.items():
                    # Extract text from the Nxtwave Course curriculum
                    curriculum_text = extract_text_from_pdf(curriculum_path)
                    response, matching_percentage, exact_matches, not_exact_matches = analyze_doability_with_prompt(assignment_text, curriculum_text)
                    
                    results.append({
                        "Curriculum": curriculum_name,
                        "Matching Percentage": matching_percentage,
                        "Detailed Analysis": response,
                        "Exact Matches": exact_matches,
                        "Not Exact Matches": not_exact_matches
                    })
            
            # Display the result for the Nxtwave Course curriculum directly
            if results:
                result = results[0]  # Only one result for the Nxtwave Course
                
                # Adjust column widths: 6:6:6 means equal width columns, but can be adjusted (e.g., 12:12:12 or 10:10:10)
                col1, col2, col3 = st.columns([3, 6, 3])  # Increasing middle column width
                
                with col1:
                    st.write(f"**Matching Percentage:** {result['Matching Percentage']}")
                with col2:
                    st.write(f"**Detailed Analysis:** {result['Detailed Analysis']}")
                    for match in result['Exact Matches']:
                        st.write(f"- {match}")
                    for match in result['Not Exact Matches']:
                        st.write(f"- {match}")
                with col3:
                    pass  # You can leave this empty or use it for other content if needed


if __name__ == "__main__":
    main()
