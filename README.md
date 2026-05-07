# SecureNotes

Modern Flask notes app with a cybersecurity-inspired dark UI.

## Run locally

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

### Demo account
- **Username:** `demo`
- **Password:** `demo1234`

## Structure
```
SecureNotes/
├── app.py              # Routes & app factory
├── models.py           # SQLAlchemy models (User, Note)
├── requirements.txt
├── static/
│   └── css/style.css   # Dark cyber theme
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    └── edit_note.html
```
