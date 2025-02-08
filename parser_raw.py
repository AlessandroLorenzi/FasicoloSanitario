import fitz


class ParserRaw:
    def __init__(self, pdf_path):
        self.raw_content = self.extract_text_from_pdf(pdf_path)

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
        return text

    def get_all_values(self):
        return None
