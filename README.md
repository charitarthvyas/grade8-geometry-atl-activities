
# Grade 8 Geometry — Interactive ATL Activities (Streamlit)

This repository contains a simple Streamlit app with three interactive inquiry activities designed for Grade 8 Geometry.
The activities practise Critical Thinking (ATL) while students investigate surface area, design compound volumes, and explore scale-factor patterns.

## Files
- `app.py` — main Streamlit app
- `README.md` — this file

## How to run locally
1. Install Python 3.8+
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate     # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
3. Install dependencies:
   ```bash
   pip install streamlit numpy pandas matplotlib
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
5. Open the URL displayed (usually http://localhost:8501).

## How to upload to GitHub
1. Create a new repository on GitHub.
2. Add the files (`app.py`, `README.md`) and push using git:
   ```bash
   git init
   git add app.py README.md
   git commit -m "Initial commit: Streamlit ATL activities"
   git branch -M main
   git remote add origin <your-repo-URL>
   git push -u origin main
   ```

## Notes for teachers
- Encourage students to record screenshots and short justifications as formative evidence.
- The app is lightweight and requires no internet services to run locally.
