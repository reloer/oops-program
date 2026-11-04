
import fitz
from io import BytesIO

def extract_text(filename, file_data):

    if filename.lower().endswith(".txt"):
        return file_data.decode("utf-8", errors="replace")

    if filename.lower().endswith(".pdf"):

        pdf = fitz.open(
            stream=BytesIO(file_data),
            filetype="pdf"
        )

        text = ""

        for page in pdf:
            text += page.get_text() + "\n"

        return text

    raise ValueError("Unsupported file format")


def split_text(text, chunk_size=1200, overlap=180):

    text = " ".join(text.split())

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        if end < len(text):
            boundary = text.rfind(" ", start, end)

            if boundary > start + chunk_size // 2:
                end = boundary

        chunks.append(text[start:end].strip())

        if end == len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks
