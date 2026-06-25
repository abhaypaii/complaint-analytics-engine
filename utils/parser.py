import pandas as pd
import fitz  # PyMuPDF
from docx import Document


def parse_file(uploaded_file):

    filename = uploaded_file.name.lower()

    # CSV
    if filename.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

        return df.to_markdown(index=False)

    # Excel
    elif filename.endswith(".xlsx"):

        sheets = pd.read_excel(
            uploaded_file,
            sheet_name=None
        )

        text = ""

        for sheet_name, df in sheets.items():

            text += f"\n\n## Sheet: {sheet_name}\n"

            text += df.to_markdown(index=False)

        return text

    # Word
    elif filename.endswith(".docx"):

        doc = Document(uploaded_file)

        text = "\n".join(
            para.text
            for para in doc.paragraphs
            if para.text.strip()
        )

        return text

    # PDF
    elif filename.endswith(".pdf"):

        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        text = ""

        for page in pdf:

            text += page.get_text()

        pdf.close()

        return text

    else:

        raise ValueError(
            "Unsupported file type."
        )