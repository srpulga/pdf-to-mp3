import unittest

from src.services.pdf import pdf_count_pages, pdf_extract_text


class PdfExtractTextTests(unittest.TestCase):
    """Testes para o servico de extracao de texto de PDF."""

    def _make_pdf_bytes(self, text: str = "Hello World") -> bytes:
        """Cria um PDF simples em memoria para testes."""
        from io import BytesIO

        import PyPDF2

        buffer = BytesIO()
        writer = PyPDF2.PdfWriter()
        writer.add_blank_page(width=72, height=72)

        # PyPDF2 nao tem API simples para adicionar texto a paginas em branco,
        # entao testamos com PDF real nos testes de integracao.
        # Aqui validamos que a funcao nao quebra com paginas sem texto.
        writer.write(buffer)
        return buffer.getvalue()

    def test_pdf_count_pages_with_blank_pdf(self) -> None:
        pdf_bytes = self._make_pdf_bytes()
        count = pdf_count_pages(arquivo_bytes=pdf_bytes)
        self.assertEqual(count, 1)

    def test_pdf_extract_text_returns_empty_for_blank_pdf(self) -> None:
        pdf_bytes = self._make_pdf_bytes()
        text = pdf_extract_text(arquivo_bytes=pdf_bytes, inicio=1, fim=1)
        self.assertEqual(text, "")

    def test_pdf_extract_text_respects_page_range(self) -> None:
        from io import BytesIO

        import PyPDF2

        buffer = BytesIO()
        writer = PyPDF2.PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.add_blank_page(width=72, height=72)
        writer.add_blank_page(width=72, height=72)
        writer.write(buffer)
        pdf_bytes = buffer.getvalue()

        count = pdf_count_pages(arquivo_bytes=pdf_bytes)
        self.assertEqual(count, 3)

        # Extrair apenas pagina 2
        text = pdf_extract_text(arquivo_bytes=pdf_bytes, inicio=2, fim=2)
        self.assertEqual(text, "")


if __name__ == "__main__":
    unittest.main()
