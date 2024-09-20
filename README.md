**Prerequisites**
Before you begin, ensure you have the following installed on your system:

Python 3.6+
pip (Python package installer)
Virtual Environment (optional but recommended)

**Project Structure**
Organize your project directory as follows:
typeConversion/
├── app.py
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── uploads/
│   └── converted/
└── requirements.txt

app.py: The main Flask application file.
templates/: Directory containing HTML templates.
static/uploads/: Directory to store uploaded images.
static/converted/: Directory to store converted images.
requirements.txt: File listing all Python dependencies.

**Installing Dependencies**

First, create a virtual environment (optional but recommended):
cd typeConversion
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the dependencies:
pip install -r requirements.txt

**Running the Application**

1. Activate the Virtual Environment (if you created one):
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2.Run the Flask App:
   python app.py
