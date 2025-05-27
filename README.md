# simpleapp

## Installation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

vim .env
DATABASE_URL=

## Launch Backend Server
uvicorn app.main:app  