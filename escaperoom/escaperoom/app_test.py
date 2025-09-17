import streamlit as st
from pathlib import Path

st.title("اختبار الصوت")

# مسار ملف الصوت
sound_file = Path("sounds/correct.mp3")

if sound_file.exists():
    st.audio(str(sound_file))
else:
    st.error("لم أجد ملف sounds/correct.mp3 — تأكد من وضعه في المجلد.")