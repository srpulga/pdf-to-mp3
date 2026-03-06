"""
Conversor de Midia MP3 - Interface Web
Converte arquivos PDF em audio MP3 usando vozes neurais
"""

import asyncio
from pathlib import Path

import streamlit as st

from src.config import PAGE_CONFIG, get_output_dir
from src.selectors.history import (
    history_add_from_result,
    history_as_dataframe,
    history_clear,
    history_count,
    history_get_all,
    history_init,
)
from src.selectors.voices import voice_get_code, voice_get_display_names
from src.services.conversion import conversion_execute
from src.services.pdf import pdf_count_pages
from src.styles import CUSTOM_CSS
from src.types import ConversionJob

st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

OUTPUT_DIR = get_output_dir()

# Inicializar session state
history_init()
if 'fila_conversoes' not in st.session_state:
    st.session_state.fila_conversoes = []
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0


def render_tab_nova_conversao() -> None:
    st.header("Configurar Nova Conversao")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "\U0001f4c4 Selecione o arquivo PDF",
            type=['pdf'],
            help="Escolha um arquivo PDF para converter em audio",
            key=f"pdf_uploader_{st.session_state.uploader_key}",
        )

        if uploaded_file:
            try:
                arquivo_bytes = uploaded_file.getvalue()
                total_paginas = pdf_count_pages(arquivo_bytes=arquivo_bytes)

                st.markdown(
                    f'<div class="info-box">\U0001f4d6 <b>{total_paginas}</b> paginas encontradas</div>',
                    unsafe_allow_html=True,
                )

                nome_base = Path(uploaded_file.name).stem
                saida = st.text_input(
                    "\U0001f4be Nome do arquivo de saida (sem extensao)",
                    value=nome_base,
                    help="O arquivo sera salvo como .mp3",
                )

                voz_selecionada = st.selectbox(
                    "\U0001f3a4 Escolha a voz",
                    options=voice_get_display_names(),
                    help="Selecione a voz que sera usada para narrar o texto",
                )

                col_pag1, col_pag2 = st.columns(2)

                with col_pag1:
                    inicio = st.number_input(
                        "\U0001f4d6 Pagina inicial",
                        min_value=1,
                        max_value=total_paginas,
                        value=1,
                        help="Primeira pagina a ser convertida",
                    )

                with col_pag2:
                    fim = st.number_input(
                        "\U0001f4d6 Pagina final",
                        min_value=1,
                        max_value=total_paginas,
                        value=total_paginas,
                        help="Ultima pagina a ser convertida",
                    )

                if inicio > fim:
                    st.error("\u26a0\ufe0f A pagina inicial deve ser menor ou igual a pagina final!")
                else:
                    st.info(f"\U0001f4c4 Serao convertidas {fim - inicio + 1} pagina(s)")

                    col_btn1, col_btn2 = st.columns(2)
                    voz_nome = voz_selecionada.split('(')[0].strip()
                    voz_code = voice_get_code(display_name=voz_selecionada)

                    with col_btn1:
                        if st.button("\u2795 Adicionar a Fila", use_container_width=True):
                            job = ConversionJob(
                                arquivo_nome=uploaded_file.name,
                                arquivo_bytes=arquivo_bytes,
                                saida=saida + '.mp3',
                                inicio=inicio,
                                fim=fim,
                                voz_nome=voz_nome,
                                voz_code=voz_code,
                            )
                            st.session_state.fila_conversoes.append(job)
                            st.session_state.uploader_key += 1
                            st.toast(f"\u2705 Conversao adicionada a fila: {saida}.mp3")
                            st.rerun()

                    with col_btn2:
                        if st.button("\U0001f680 Converter Agora", use_container_width=True, type="primary"):
                            with st.spinner(f"\U0001f504 Convertendo {uploaded_file.name}..."):
                                saida_arquivo = saida + '.mp3'
                                job = ConversionJob(
                                    arquivo_nome=uploaded_file.name,
                                    arquivo_bytes=arquivo_bytes,
                                    saida=saida_arquivo,
                                    inicio=inicio,
                                    fim=fim,
                                    voz_nome=voz_nome,
                                    voz_code=voz_code,
                                )

                                result = asyncio.run(
                                    conversion_execute(job=job, output_dir=OUTPUT_DIR)
                                )

                                history_add_from_result(
                                    arquivo=uploaded_file.name,
                                    saida=saida_arquivo,
                                    inicio=inicio,
                                    fim=fim,
                                    voz_nome=voz_nome,
                                    success=result.success,
                                )

                                if result.success:
                                    st.success(f"\u2705 {result.message}")
                                    st.info(f"\U0001f4c1 Arquivo salvo em: output/{saida_arquivo}")
                                    st.download_button(
                                        label="\u2b07\ufe0f Baixar Audio MP3",
                                        data=result.audio_bytes,
                                        file_name=saida_arquivo,
                                        mime="audio/mpeg",
                                        use_container_width=True,
                                    )
                                else:
                                    st.error(f"\u274c {result.message}")

            except Exception as e:
                st.error(f"\u274c Erro ao ler PDF: {e}")

    with col2:
        st.markdown("### \u2139\ufe0f Informacoes")
        st.info("""
        **Como usar:**

        1. \U0001f4c4 Faca upload do PDF
        2. \u2699\ufe0f Configure as opcoes
        3. \u2795 Adicione a fila ou
        4. \U0001f680 Converta imediatamente

        **Recursos:**
        - 10 vozes em PT-BR
        - Conversao em lote
        - Alta qualidade
        - Download direto
        """)

        st.markdown("### \U0001f3a4 Vozes Disponiveis")
        st.write("**Masculinas:**")
        st.write("\u2022 Antonio, Donato, Fabio")
        st.write("\u2022 Humberto, Nicolau")

        st.write("**Femininas:**")
        st.write("\u2022 Francisca, Thalita")
        st.write("\u2022 Giovanna, Leila, Manuela")


def render_tab_fila() -> None:
    st.header("Fila de Conversoes")

    if not st.session_state.fila_conversoes:
        st.info("\U0001f4ed Nenhuma conversao na fila. Adicione conversoes na aba 'Nova Conversao'.")
        return

    st.success(f"\U0001f4cb {len(st.session_state.fila_conversoes)} conversao(oes) na fila")

    for idx, job in enumerate(st.session_state.fila_conversoes):
        with st.expander(f"\U0001f3b5 {job.saida} - {job.voz_nome}"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**Arquivo:** {job.arquivo_nome}")
                st.write(f"**Paginas:** {job.inicio} - {job.fim}")
                st.write(f"**Voz:** {job.voz_nome}")
                st.write(f"**Adicionado:** {job.timestamp}")

            with col2:
                if st.button("\U0001f5d1\ufe0f Remover", key=f"remove_{idx}"):
                    st.session_state.fila_conversoes.pop(idx)
                    st.rerun()

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("\U0001f680 Processar Toda a Fila", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()

            total = len(st.session_state.fila_conversoes)
            resultados = []

            for idx, job in enumerate(st.session_state.fila_conversoes):
                status_text.text(f"\U0001f504 Processando {idx + 1}/{total}: {job.saida}")
                progress_bar.progress(idx / total)

                result = asyncio.run(
                    conversion_execute(job=job, output_dir=OUTPUT_DIR)
                )

                history_add_from_result(
                    arquivo=job.arquivo_nome,
                    saida=job.saida,
                    inicio=job.inicio,
                    fim=job.fim,
                    voz_nome=job.voz_nome,
                    success=result.success,
                )

                if result.success and result.audio_bytes:
                    resultados.append({"saida": job.saida, "audio_bytes": result.audio_bytes})

            progress_bar.progress(1.0)
            status_text.text(f"\u2705 Todas as {total} conversoes foram processadas!")

            st.session_state.fila_conversoes = []
            st.balloons()

            if resultados:
                st.markdown("### \u2b07\ufe0f Downloads")
                for idx, item in enumerate(resultados):
                    st.download_button(
                        label=f"\u2b07\ufe0f Baixar {item['saida']}",
                        data=item["audio_bytes"],
                        file_name=item["saida"],
                        mime="audio/mpeg",
                        use_container_width=True,
                        key=f"download_fila_{idx}",
                    )

    with col2:
        if st.button("\U0001f9f9 Limpar Fila", use_container_width=True):
            st.session_state.fila_conversoes = []
            st.rerun()


def render_tab_historico() -> None:
    st.header("Historico de Conversoes")

    if history_count() == 0:
        st.info("\U0001f4ed Nenhuma conversao realizada ainda.")
        return

    st.success(f"\U0001f4ca {history_count()} conversao(oes) no historico")

    df = history_as_dataframe()

    def highlight_status(val: str) -> str:
        color = 'lightgreen' if val == 'Sucesso' else 'lightcoral'
        return f'background-color: {color}'

    st.dataframe(
        df.style.map(highlight_status, subset=['status']),
        use_container_width=True,
    )

    entries = history_get_all()
    for idx, entry in enumerate(entries):
        if entry.status == "Sucesso":
            filepath = OUTPUT_DIR / entry.saida
            if filepath.exists():
                st.download_button(
                    label=f"\u2b07\ufe0f Baixar {entry.saida}",
                    data=filepath.read_bytes(),
                    file_name=entry.saida,
                    mime="audio/mpeg",
                    use_container_width=True,
                    key=f"download_hist_{idx}",
                )

    if st.button("\U0001f5d1\ufe0f Limpar Historico"):
        history_clear()
        st.rerun()


def main() -> None:
    st.markdown(
        '<h1 class="main-header">\U0001f3b5 Conversor de Midia MP3</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="subtitle">Converta PDFs em audio com vozes naturais de alta qualidade</p>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs([
        "\U0001f4dd Nova Conversao",
        "\U0001f4cb Fila de Conversoes",
        "\U0001f4ca Historico",
    ])

    with tab1:
        render_tab_nova_conversao()

    with tab2:
        render_tab_fila()

    with tab3:
        render_tab_historico()

    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Desenvolvido com Python \U0001f40d | '
        'Powered by Edge TTS \U0001f3a4</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
