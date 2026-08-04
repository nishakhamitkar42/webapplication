# Sales Executive Portfolio Web Application

A professional and modern portfolio web application built using Python, Flask, and SQLite on the backend (following MVC pattern), with clean, premium HTML/CSS/JS on the frontend. The application features page templates for a complete professional portfolio and includes a REST API-powered Contact Form that stores submissions in a local SQLite database.

## Architecture (MVC Pattern)

- **Model**: `models/contact.py` manages contact entries and handles interactions with the SQLite database.
- **View**: Handled through Jinja templates (`templates/`) styled using premium vanilla CSS (`frontend/css/style.css`) and interactive JS (`frontend/js/main.js`).
- **Controller**: Flask route handlers split between `controllers/main_controller.py` (webpages navigation) and `controllers/api_controller.py` (REST API).

## Directory Structure

```
protifilio/
├── app.py                      # Main entrypoint
├── database/
│   └── db.py                   # SQLite Initialization & connection manager
├── models/
│   └── contact.py              # SQLite Interaction Model
├── controllers/
│   ├── main_controller.py      # Website page controllers
│   └── api_controller.py       # REST API controllers
├── templates/                  # Views (HTML Jinja Templates)
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── projects.html
│   ├── certification.html
│   ├── skills.html
│   ├── achievements.html
│   └── contact.html
├── frontend/                   # Static files (CSS, JS, Images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── profile.webp        # Generated portrait image
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git untracked pattern file
└── README.md                   # This file
```

## Setup & Running Guide

This project is managed using the modern `uv` Python package manager.

### Prerequisites

- Python 3.10+
- `uv` package manager

### 1. Initialize Virtual Environment

Run the following command to create a virtual environment in the project directory:

```bash
uv venv
```

### 2. Activate Virtual Environment

- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

Install the project dependencies (Flask):

```bash
uv pip install flask
```

Or run directly using `uv run`:

```bash
uv run python app.py
```

### 4. Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will be accessible at: `http://127.0.0.1:5000/`
