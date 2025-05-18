
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from io import BytesIO
import re

def converter_pdf_para_excel(pdf_file, nome_saida):
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

# Streamlit App
st.title("Conversor de PDF para Planilha .XLSX")
st.markdown("Envie arquivos PDF dos itens de julgamento (ex: item-1.pdf, item-2.pdf...) para converter em Excel.")

uploaded_files = st.file_uploader("Envie os arquivos PDF:", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for pdf_file in uploaded_files:
        nome_base = re.sub(r"\.pdf$", "", pdf_file.name)
        nome_saida = f"{nome_base}_convertido.xlsx"
        excel_bytes = converter_pdf_para_excel(pdf_file, nome_saida)

        st.success(f"Arquivo convertido: {nome_saida}")
        st.download_button(
            label=f"🔗 Baixar {nome_saida}",
            data=excel_bytes,
            file_name=nome_saida,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
