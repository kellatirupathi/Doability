import streamlit as st
from pathlib import Path
from utils.pdf_processing import extract_text_from_pdf
from utils.openai_api import analyze_text_with_openai
from docx import Document
import re

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
            parts = re.split(r'(\*\*.*?\*\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])  # Remove the ** markers
                    run.bold = True
                else:
                    p.add_run(part)
    
    doc.save(output_path_docx)
    
    return output_path_docx

def main():
    st.title("Reference Document Generator")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
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

1. **Introduction**: A brief overview of the assignment, including its purpose and goals.
   
2. **Step-by-Step Instructions**: A clear, sequential guide outlining the actions necessary to complete the assignment. Each step should be described in a way that is accessible to users of all skill levels but no need of codes.

3. **Best Practices**: Suggestions and tips for effectively completing the assignment, ensuring a high standard of work, and avoiding common mistakes.

4. **Submission Guidelines**: Detailed instructions on how to submit the finished assignment, including any required formats or materials.

5. **Frequently Asked Questions (FAQ)**: Answers to common questions or issues that might arise during the assignment, providing additional clarity and support.
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

if __name__ == "__main__":
    main()
