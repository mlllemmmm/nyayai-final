## Setup Instructions

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt

3. Generate vector database:
   python backend/ingest.py

4. Run server:
   uvicorn backend.main:app --reload
