
# Grade 8 Geometry — Interactive ATL Activities (Streamlit, 3D Plotly)

This repository contains a Streamlit app with three interactive inquiry activities designed for Grade 8 Geometry.
The activities practise Critical Thinking (ATL) while students investigate surface area, design compound volumes, and explore scale-factor patterns.
Fully interactive 3D visuals use Plotly: students can rotate and zoom the models.

## Files
- `app.py` — main Streamlit app with 3D Plotly visualizations
- `README.md` — instructions for running locally and uploading to GitHub
- `requirements.txt` — Python packages required

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
   pip install streamlit numpy pandas plotly
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
5. Open the URL displayed (usually http://localhost:8501).

## How to upload to GitHub (web UI)
1. Create a new repository on GitHub, or use an existing one.
2. Click **Add file → Upload files** and upload `app.py`, `README.md`, `requirements.txt`.
3. Commit changes and then deploy on Streamlit Cloud (share.streamlit.io) using the GitHub repo.

## Notes for teachers
- Plotly 3D is more resource-intensive; recommend desktops/laptops for students.
- Collect screenshots, short written justifications, and exported summaries as formative evidence.
