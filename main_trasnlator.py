import streamlit as st
from deep_translator import GoogleTranslator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import nltk

# Download punkt for Sumy/NLTK (needed on Streamlit Cloud)
nltk.download("punkt")

# ---------------- Summarization Function ---------------- #
def summarize_text(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

# ---------------- PDF Export ---------------- #
def save_as_pdf(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text_object = c.beginText(50, height - 50)
    for line in text.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()
    buffer.seek(0)
    return buffer

# ---------------- Word Export ---------------- #
def save_as_word(text):
    buffer = BytesIO()
    doc = Document()
    doc.add_paragraph(text)
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Text Translator & Summarizer", page_icon="📘", layout="centered")

st.title("📘 Text Translator & Summarizer")
st.write("### Presented by Vaibhavi Zunzunkar BT55 - JD College")

option = st.radio("Choose an option:", ["Type Text", "Upload File"])

text_input = ""

if option == "Type Text":
    text_input = st.text_area("✍️ Enter your text here", height=200)

elif option == "Upload File":
    uploaded_file = st.file_uploader("📂 Upload a text file", type=["txt"])
    if uploaded_file is not None:
        text_input = uploaded_file.read().decode("utf-8")

if text_input:
    st.subheader("🔍 Summary")
    summary = summarize_text(text_input)
    st.write(summary)

    st.subheader("🌍 Translate Summary")
    target_lang = st.selectbox("Select target language", ["en", "hi", "fr", "de", "es"])
    translated = GoogleTranslator(source="auto", target=target_lang).translate(summary)
    st.write(translated)

    # ---------------- Download Buttons ---------------- #
    st.subheader("⬇️ Download Options")
    pdf_buffer = save_as_pdf(summary)
    word_buffer = save_as_word(summary)

    st.download_button("Download as PDF", data=pdf_buffer, file_name="summary.pdf", mime="application/pdf")
    st.download_button("Download as Word", data=word_buffer, file_name="summary.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
