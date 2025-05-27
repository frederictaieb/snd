# simpleapp

## Installation
### Dependencies
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Database
```
vim .env
DATABASE_URL=
```

## Starting Backend Server
```
uvicorn app.main:app  
```