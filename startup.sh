python process_data_files.py &&
uvicorn main:app --port=8000 --reload &
streamlit run app.py