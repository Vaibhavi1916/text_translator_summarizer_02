import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Download required NLTK data
nltk.download("punkt")
nltk.download("punkt_tab")


# ------------------- Text Summarization -------------------
def summarize_text(text, sentences_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join(str(sentence) for sentence in summary)


# ------------------- Save as Word -------------------
def save_as_word(text, filename="summary.docx"):
    doc = Document()
    doc.add_heading("Text Summary", 0)
    doc.add_paragraph(text)
    doc.save(filename)


# ------------------- Save as PDF -------------------
def save_as_pdf(text, filename="summary.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.drawString(50, height - 50, "Text Summary")
    text_object = c.beginText(50, height - 80)
    text_object.setFont("Times-Roman", 12)

    for line in text.split("\n"):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()


# ------------------- Streamlit App -------------------
def main():
    st.title("Text Translator & Summarizer")
    st.write("### Presented by Vaibhavi Zunzunkar - JD College")

    option = st.radio("Choose an option:", ["Enter Text", "Upload File"])

    text_input = ""
    if option == "Enter Text":
        text_input = st.text_area("Enter your text here:")
    elif option == "Upload File":
        uploaded_file = st.file_uploader("Upload a text/CSV file", type=["txt", "csv"])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                text_input = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
                text_input = " ".join(df.astype(str).values.flatten())

    if text_input:
        if st.button("Summarize"):
            summary = summarize_text(text_input)
            st.subheader("Summary")
            st.write(summary)

            save_as_word(summary, "summary.docx")
            save_as_pdf(summary, "summary.pdf")

            with open("summary.docx", "rb") as f:
                st.download_button("Download Word", f, file_name="summary.docx")

            with open("summary.pdf", "rb") as f:
                st.download_button("Download PDF", f, file_name="summary.pdf")


if __name__ == "__main__":
    main()
