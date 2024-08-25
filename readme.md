import streamlit as st
from pathlib import Path
from utils.pdf_processing import extract_text_from_pdf
from utils.openai_api import analyze_text_with_openai
from docx import Document
import re
import difflib
from PIL import Image
import pytesseract

# Existing Reference Document Generator
def generate_reference_document(analyzed_text, output_filename_docx):
    output_dir = Path('output/analyzed_documents')
    
    if output_dir.exists() and not output_dir.is_dir():
        output_dir.unlink()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path_docx = output_dir / output_filename_docx
    doc = Document()

    for line in analyzed_text.splitlines():
        if line.startswith('#### '):
            p = doc.add_paragraph(line[5:])
            p.style = 'Heading 4'        
        elif line.startswith('### '):
            p = doc.add_paragraph(line[4:])
            p.style = 'Heading 3'
        elif line.startswith('## '):
            p = doc.add_paragraph(line[3:])
            p.style = 'Heading 2'
        elif line.startswith('# '):
            p = doc.add_paragraph(line[2:])
            p.style = 'Heading 1'
        else:
            p = doc.add_paragraph()
            parts = re.split(r'(\\.?\\*)', line)
            for part in parts:
                if part.startswith('') and part.endswith(''):
                    run = p.add_run(part[2:-2])  # Remove the ** markers
                    run.bold = True
                else:
                    p.add_run(part)
    
    doc.save(output_path_docx)
    
    return output_path_docx

# Function to check assignment doability
def check_assignment_doability(assignment_text, curriculum_text):
    sm = difflib.SequenceMatcher(None, assignment_text, curriculum_text)
    return sm.ratio() * 100

def analyze_doability_with_prompt(assignment_text, curriculum_text):
    prompt = f"""
Please analyze the alignment between the following assignment and the provided curriculum. Assess how closely the content of the assignment matches the topics and objectives outlined in the curriculum. If any content in the assignment does not directly match the curriculum, identify the underlying topic or concept and compare it to related areas in the curriculum.

Assignment:
{assignment_text}

Curriculum:
{curriculum_text}

Provide a detailed analysis, including a Matching Percentage displayed in large text. Explain how the alignment was determined, particularly noting any content that was compared based on underlying concepts rather than exact matches.
"""
    response = analyze_text_with_openai(prompt)
    match_percentage = re.search(r'\b(\d{1,3})%\b', response)
    return response, match_percentage.group(0) if match_percentage else "N/A"

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def analyze_questions_with_prompt(extracted_text):
    prompt = f"""
Please analyze the following questions extracted from an image. Provide a detailed response, explaining the concepts behind each question and offering suggestions or tips for answering them effectively.

Questions:
{extracted_text}
"""
    response = analyze_text_with_openai(prompt)
    return response

def main():
    st.set_page_config(page_title="Document Generator & Doability Checker", layout="wide")
    
    # Sidebar buttons for navigation
    st.sidebar.title("Navigation")
    
    doability_page = st.sidebar.button("Assignment Doability Checker")
    document_page = st.sidebar.button("Reference Document Generator")
    questions_page = st.sidebar.button("Reference Document Questions")

    if doability_page:
        st.session_state["page"] = "Doability"
    if document_page:
        st.session_state["page"] = "Document"
    if questions_page:
        st.session_state["page"] = "Questions"

    # Default to Doability Checker if no state set
    if "page" not in st.session_state:
        st.session_state["page"] = "Doability"
    
    # Display the correct page based on the user's selection
    if st.session_state["page"] == "Doability":
        doability_checker()
    elif st.session_state["page"] == "Document":
        reference_document_generator()
    elif st.session_state["page"] == "Questions":
        reference_document_questions()

# Function for the Doability Checker page
def doability_checker():
    st.header("Assignment Doability Checker")
    
    uploaded_file = st.file_uploader("Upload an Assignment PDF file", type="pdf", key="assignment")
    curriculum_options = {
        "Fundamentals": "curriculums/fundamentals.pdf",
        "MERN Fullstack": "curriculums/mern_fullstack.pdf",
        "Data Analytics": "curriculums/data_analytics.pdf",
        "Java Fullstack": "curriculums/java_fullstack.pdf",
        "QA Testing": "curriculums/qa_testing.pdf"
    }
    
    selected_curriculum = st.selectbox("Select a Curriculum PDF file", list(curriculum_options.keys()))
    
    if uploaded_file is not None and selected_curriculum:
        with st.spinner('Reading assignment PDF...'):
            assignment_text = extract_text_from_pdf(uploaded_file)
            st.success("Assignment PDF read successfully!")
        
        curriculum_path = curriculum_options[selected_curriculum]
        curriculum_text = extract_text_from_pdf(curriculum_path)
        
        if st.button("Check Doability"):
            with st.spinner('Checking assignment doability...'):
                response, matching_percentage = analyze_doability_with_prompt(assignment_text, curriculum_text)
                st.success(f"Assignment doability check completed with a matching percentage of {matching_percentage}.")
                st.write(response)

# Function for the Reference Document Generator page
def reference_document_generator():
    st.header("Reference Document Generator")
    
    uploaded_file = st.file_uploader("Upload a PDF file for Reference Document", type="pdf", key="reference")
    if uploaded_file is not None:
        with st.spinner('Reading PDF...'):
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.success("PDF read successfully!")
        
        with st.spinner('Analyzing text...'):
            prompt = f"""
Please create a comprehensive reference document that provides clear and detailed instructions for completing the following assignment. The document should be easy to follow and help users understand the assignment objectives and the steps required to achieve them.

Assignment Description:
{pdf_text}

The reference document should include:

Reference Document of Assignment title name:

1. Objective: A brief overview of the assignment, including its purpose and goals.
   
2. Step-by-Step Instructions: A clear, sequential guide outlining the actions necessary to complete the assignment. Each step should be described in a way that is accessible to users of all skill levels but no need of codes.

3. Best Practices: Suggestions and tips for effectively completing the assignment, ensuring a high standard of work, and avoiding common mistakes.

4. Submission Guidelines: Detailed instructions on how to submit the finished assignment, including any required formats or materials.

5. Frequently Asked Questions (FAQ): Answers to common questions or issues that might arise during the assignment, providing additional clarity and support.
"""
            analyzed_text = analyze_text_with_openai(prompt)
            st.success("Text analyzed successfully!")
            
            output_filename_docx = f"Reference_Document_{uploaded_file.name}.docx"
            output_path_docx = generate_reference_document(analyzed_text, output_filename_docx)
            
            with open(output_path_docx, "rb") as file:
                st.download_button(
                    label="Download as Word Document",
                    data=file,
                    file_name=output_filename_docx,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

# Function for the Reference Document Questions page
def reference_document_questions():
    st.header("Reference Document Questions")
    
    uploaded_images = st.file_uploader("Upload images (jpg, png, jpeg) containing questions", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if uploaded_images:
        extracted_texts = []
        for image_file in uploaded_images:
            image = Image.open(image_file)
            extracted_text = extract_text_from_image(image)
            extracted_texts.append(extracted_text)
        
        combined_text = "\n\n".join(extracted_texts)
        
        with st.spinner('Analyzing extracted text...'):
            response = analyze_questions_with_prompt(combined_text)
            st.success("Text analyzed successfully!")
            st.write(response)

if _name_ == "_main_":
    main()
