from pypdf import PdfReader

def get_reference_summary():
    reader = PdfReader("Problemas_semana3_pareajas.pdf")

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

texto = get_reference_summary()
print(texto)