from pathlib import Path

def generate_reference_document(analyzed_text, output_filename):
    output_dir = Path('output/analyzed_documents')
    
    # If output_dir exists and is not a directory, delete it
    if output_dir.exists() and not output_dir.is_dir():
        output_dir.unlink()  # This removes the file if it exists
    
    # Create the directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / output_filename
    
    template = Path('templates/reference_template.md').read_text(encoding='utf-8')
    document_content = template.format(content=analyzed_text)
    
    # Write the document content using UTF-8 encoding
    output_path.write_text(document_content, encoding='utf-8')
    
    return output_path
