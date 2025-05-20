
import os
import pandas as pd
from PyPDF2 import PdfReader
from zipfile import ZipFile

def converter_pdf_para_excel(pdf_path, nome_saida=None):
    reader = PdfReader(pdf_path)
    linhas_total = []
    for page in reader.pages:
        texto = page.extract_text()
        if texto:
            linhas_total += texto.splitlines()
    df = pd.DataFrame(linhas_total, columns=["Linha"])
    if not nome_saida:
        base = os.path.basename(pdf_path).replace(".pdf", "")
        nome_saida = f"{base}_convertido.xlsx"
    df.to_excel(nome_saida, index=False)
    return nome_saida

def processar_pdfs_em_pasta(pasta_entrada="pdfs", pasta_saida="convertidos", nome_zip="arquivos_convertidos_excel.zip"):
    os.makedirs(pasta_saida, exist_ok=True)
    arquivos_convertidos = []

    for nome in os.listdir(pasta_entrada):
        if nome.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta_entrada, nome)
            nome_saida = os.path.join(pasta_saida, nome.replace(".pdf", "_convertido.xlsx"))
            print(f"🔄 Convertendo: {nome}")
            convertido = converter_pdf_para_excel(caminho_pdf, nome_saida)
            arquivos_convertidos.append(convertido)

    with ZipFile(nome_zip, "w") as zipf:
        for arquivo in arquivos_convertidos:
            zipf.write(arquivo, arcname=os.path.basename(arquivo))

    print(f"✅ Conversão finalizada! Arquivo gerado: {nome_zip}")

if __name__ == "__main__":
    processar_pdfs_em_pasta()
