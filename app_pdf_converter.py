import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from io import BytesIO
import zipfile
import re

def converter_pdf_para_excel(pdf_file):
    reader = PdfReader(pdf_file)
    linhas_total = []
    for page in reader.pages:
        texto = page.extract_text()
        if texto:
            linhas_total += texto.splitlines()
    df = pd.DataFrame(linhas_total, columns=["Linha"])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

st.title("📄🔁 Conversor de PDF para Excel (.XLSX) em ZIP")
st.markdown("Envie múltiplos arquivos PDF que deseja converter. Você receberá um único arquivo `.zip` com todas as planilhas convertidas.")

uploaded_files = st.file_uploader("📤 Envie os PDFs:", type="pdf", accept_multiple_files=True)

if uploaded_files:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for pdf_file in uploaded_files:
            nome_base = re.sub(r"\.pdf$", "", pdf_file.name, flags=re.IGNORECASE)
            nome_saida = f"{nome_base}_convertido.xlsx"
            excel_bytes = converter_pdf_para_excel(pdf_file)
            zipf.writestr(nome_saida, excel_bytes.getvalue())

    zip_buffer.seek(0)

    st.success("✅ Conversão concluída com sucesso!")
    st.download_button(
        label="📥 Baixar arquivo ZIP com todos os Excel",
        data=zip_buffer,
        file_name="planilhas_convertidas.zip",
        mime="application/zip"
