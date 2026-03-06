import io

import PyPDF2


def pdf_extract_text(*, arquivo_bytes: bytes, inicio: int, fim: int) -> str:
    """Extrai texto de um PDF a partir dos bytes do arquivo."""
    leitor = PyPDF2.PdfReader(io.BytesIO(arquivo_bytes))
    total_paginas = len(leitor.pages)

    inicio_idx = max(0, inicio - 1)
    fim_idx = min(total_paginas, fim)

    texto_completo = ""
    for i in range(inicio_idx, fim_idx):
        pagina = leitor.pages[i]
        texto = pagina.extract_text()
        if texto:
            texto_limpo = texto.replace('\n', ' ').strip()
            texto_completo += texto_limpo + " "

    return texto_completo.strip()


def pdf_count_pages(*, arquivo_bytes: bytes) -> int:
    """Retorna o numero total de paginas de um PDF."""
    leitor = PyPDF2.PdfReader(io.BytesIO(arquivo_bytes))
    return len(leitor.pages)
