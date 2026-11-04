
# MindVault 🧠

Personal Digital Memory System built using Python.

## Features

- Personal memory storage
- SQLite database
- PDF and TXT document processing
- Memory categorization
- TF-IDF based intelligent search
- Memory-based question answering
- Memory dashboard
- Activity analytics
- JSON backup

## Technologies

- Python
- Streamlit
- SQLite
- Pandas
- Scikit-learn
- PyMuPDF

## Installation

Clone the repository:

    git clone YOUR_GITHUB_REPOSITORY_URL

Enter the project:

    cd MindVault

Create virtual environment:

    python -m venv .venv

Activate on Windows:

    .venv\Scripts\activate

Install requirements:

    pip install -r requirements.txt

Run the application:

    streamlit run app.py

## Database

All memories are stored locally in:

    database/mindvault.db

## Privacy

The application does not send saved memories
to an external AI service.

## Future Improvements

- Transformer embeddings
- FAISS vector search
- Local LLM integration
- Knowledge graph
- OCR document processing
- Automated reminders
