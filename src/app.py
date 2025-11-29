"""
Conversor de Mídia MP3 - Interface Web
Converte arquivos PDF em áudio MP3 usando vozes neurais
"""

import os
import asyncio
from pathlib import Path
import streamlit as st
import PyPDF2
import edge_tts
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Conversor de Mídia MP3",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vozes disponíveis
VOZES_DISPONIVEIS = {
    "Antonio (Masculina - Natural)": "pt-BR-AntonioNeural",
    "Francisca (Feminina - Natural)": "pt-BR-FranciscaNeural",
    "Donato (Masculina - Profunda)": "pt-BR-DonatoNeural",
    "Thalita (Feminina - Jovem)": "pt-BR-ThalitaNeural",
    "Fabio (Masculina - Energética)": "pt-BR-FabioNeural",
    "Giovanna (Feminina - Suave)": "pt-BR-GiovannaNeural",
    "Humberto (Masculina - Madura)": "pt-BR-HumbertoNeural",
    "Leila (Feminina - Profissional)": "pt-BR-LeilaNeural",
    "Manuela (Feminina - Calma)": "pt-BR-ManuelaNeural",
    "Nicolau (Masculina - Jovem)": "pt-BR-NicolauNeural",
}

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1557b0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Diretório de saída
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Inicializar session state
if 'fila_conversoes' not in st.session_state:
    st.session_state.fila_conversoes = []
if 'historico' not in st.session_state:
    st.session_state.historico = []


async def converter_pdf_mp3(arquivo_bytes, arquivo_nome, saida, inicio, fim, voz_code):
    """Converter PDF para MP3"""
    try:
        # Salvar arquivo temporariamente
        temp_pdf = f"temp_{arquivo_nome}"
        with open(temp_pdf, 'wb') as f:
            f.write(arquivo_bytes)

        # Ler PDF
        texto_completo = ""
        with open(temp_pdf, 'rb') as arquivo_pdf:
            leitor = PyPDF2.PdfReader(arquivo_pdf)
            total_paginas = len(leitor.pages)

            inicio_idx = max(0, inicio - 1)
            fim_idx = min(total_paginas, fim)

            for i in range(inicio_idx, fim_idx):
                pagina = leitor.pages[i]
                texto = pagina.extract_text()
                if texto:
                    texto_limpo = texto.replace('\n', ' ').strip()
                    texto_completo += texto_limpo + " "

        # Remover arquivo temporário
        os.remove(temp_pdf)

        if not texto_completo.strip():
            return False, "Nenhum texto encontrado no PDF", None

        # Caminho completo para o arquivo de saída
        saida_path = OUTPUT_DIR / saida

        # Gerar áudio
        comunicacao = edge_tts.Communicate(texto_completo, voz_code)
        await comunicacao.save(str(saida_path))

        # Ler arquivo gerado para download
        with open(saida_path, 'rb') as f:
            audio_bytes = f.read()

        return True, "Conversão concluída com sucesso!", audio_bytes

    except Exception as e:
        return False, f"Erro na conversão: {str(e)}", None


def main():
    # Cabeçalho
    st.markdown('<h1 class="main-header">🎵 Conversor de Mídia MP3</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Converta PDFs em áudio com vozes naturais de alta qualidade</p>', unsafe_allow_html=True)

    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["📝 Nova Conversão", "📋 Fila de Conversões", "📊 Histórico"])

    # TAB 1: Nova Conversão
    with tab1:
        st.header("Configurar Nova Conversão")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Upload de arquivo
            uploaded_file = st.file_uploader(
                "📄 Selecione o arquivo PDF",
                type=['pdf'],
                help="Escolha um arquivo PDF para converter em áudio"
            )

            if uploaded_file:
                # Ler informações do PDF
                try:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    total_paginas = len(pdf_reader.pages)

                    st.markdown(f'<div class="info-box">📖 <b>{total_paginas}</b> páginas encontradas</div>',
                               unsafe_allow_html=True)

                    # Nome do arquivo de saída
                    nome_base = Path(uploaded_file.name).stem
                    saida = st.text_input(
                        "💾 Nome do arquivo de saída (sem extensão)",
                        value=nome_base,
                        help="O arquivo será salvo como .mp3"
                    )

                    # Seleção de voz
                    voz_selecionada = st.selectbox(
                        "🎤 Escolha a voz",
                        options=list(VOZES_DISPONIVEIS.keys()),
                        help="Selecione a voz que será usada para narrar o texto"
                    )

                    # Controle de páginas
                    col_pag1, col_pag2 = st.columns(2)

                    with col_pag1:
                        inicio = st.number_input(
                            "📖 Página inicial",
                            min_value=1,
                            max_value=total_paginas,
                            value=1,
                            help="Primeira página a ser convertida"
                        )

                    with col_pag2:
                        fim = st.number_input(
                            "📖 Página final",
                            min_value=1,
                            max_value=total_paginas,
                            value=total_paginas,
                            help="Última página a ser convertida"
                        )

                    # Validação
                    if inicio > fim:
                        st.error("⚠️ A página inicial deve ser menor ou igual à página final!")
                    else:
                        st.info(f"📄 Serão convertidas {fim - inicio + 1} página(s)")

                        # Botões de ação
                        col_btn1, col_btn2 = st.columns(2)

                        with col_btn1:
                            if st.button("➕ Adicionar à Fila", use_container_width=True):
                                conversao = {
                                    'arquivo_nome': uploaded_file.name,
                                    'arquivo_bytes': uploaded_file.getvalue(),
                                    'saida': saida + '.mp3',
                                    'inicio': inicio,
                                    'fim': fim,
                                    'voz_nome': voz_selecionada.split('(')[0].strip(),
                                    'voz_code': VOZES_DISPONIVEIS[voz_selecionada],
                                    'status': 'Aguardando',
                                    'timestamp': datetime.now().strftime("%H:%M:%S")
                                }
                                st.session_state.fila_conversoes.append(conversao)
                                st.success(f"✅ Conversão adicionada à fila: {saida}.mp3")
                                st.rerun()

                        with col_btn2:
                            if st.button("🚀 Converter Agora", use_container_width=True, type="primary"):
                                with st.spinner(f"🔄 Convertendo {uploaded_file.name}..."):
                                    saida_arquivo = saida + '.mp3'
                                    voz_code = VOZES_DISPONIVEIS[voz_selecionada]

                                    sucesso, mensagem, audio_bytes = asyncio.run(
                                        converter_pdf_mp3(
                                            uploaded_file.getvalue(),
                                            uploaded_file.name,
                                            saida_arquivo,
                                            inicio,
                                            fim,
                                            voz_code
                                        )
                                    )

                                    if sucesso:
                                        st.success(f"✅ {mensagem}")
                                        st.info(f"📁 Arquivo salvo em: output/{saida_arquivo}")

                                        # Adicionar ao histórico
                                        st.session_state.historico.append({
                                            'arquivo': uploaded_file.name,
                                            'saida': saida_arquivo,
                                            'paginas': f"{inicio}-{fim}",
                                            'voz': voz_selecionada.split('(')[0].strip(),
                                            'timestamp': datetime.now().strftime("%H:%M:%S"),
                                            'status': 'Sucesso'
                                        })

                                        # Botão de download
                                        st.download_button(
                                            label="⬇️ Baixar Áudio MP3",
                                            data=audio_bytes,
                                            file_name=saida_arquivo,
                                            mime="audio/mpeg",
                                            use_container_width=True
                                        )
                                    else:
                                        st.error(f"❌ {mensagem}")

                                        # Adicionar ao histórico
                                        st.session_state.historico.append({
                                            'arquivo': uploaded_file.name,
                                            'saida': saida_arquivo,
                                            'paginas': f"{inicio}-{fim}",
                                            'voz': voz_selecionada.split('(')[0].strip(),
                                            'timestamp': datetime.now().strftime("%H:%M:%S"),
                                            'status': 'Erro'
                                        })

                except Exception as e:
                    st.error(f"❌ Erro ao ler PDF: {str(e)}")

        with col2:
            # Painel de informações
            st.markdown("### ℹ️ Informações")
            st.info("""
            **Como usar:**

            1. 📄 Faça upload do PDF
            2. ⚙️ Configure as opções
            3. ➕ Adicione à fila ou
            4. 🚀 Converta imediatamente

            **Recursos:**
            - 10 vozes em PT-BR
            - Conversão em lote
            - Alta qualidade
            - Download direto
            """)

            st.markdown("### 🎤 Vozes Disponíveis")
            st.write("**Masculinas:**")
            st.write("• Antonio, Donato, Fabio")
            st.write("• Humberto, Nicolau")

            st.write("**Femininas:**")
            st.write("• Francisca, Thalita")
            st.write("• Giovanna, Leila, Manuela")

    # TAB 2: Fila de Conversões
    with tab2:
        st.header("Fila de Conversões")

        if not st.session_state.fila_conversoes:
            st.info("📭 Nenhuma conversão na fila. Adicione conversões na aba 'Nova Conversão'.")
        else:
            st.success(f"📋 {len(st.session_state.fila_conversoes)} conversão(ões) na fila")

            # Mostrar fila
            for idx, conv in enumerate(st.session_state.fila_conversoes):
                with st.expander(f"🎵 {conv['saida']} - {conv['voz_nome']}"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Arquivo:** {conv['arquivo_nome']}")
                        st.write(f"**Páginas:** {conv['inicio']} - {conv['fim']}")
                        st.write(f"**Voz:** {conv['voz_nome']}")
                        st.write(f"**Adicionado:** {conv['timestamp']}")

                    with col2:
                        if st.button(f"🗑️ Remover", key=f"remove_{idx}"):
                            st.session_state.fila_conversoes.pop(idx)
                            st.rerun()

            # Botões de controle
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button("🚀 Processar Toda a Fila", type="primary", use_container_width=True):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    total = len(st.session_state.fila_conversoes)

                    for idx, conv in enumerate(st.session_state.fila_conversoes):
                        status_text.text(f"🔄 Processando {idx + 1}/{total}: {conv['saida']}")
                        progress_bar.progress((idx) / total)

                        sucesso, mensagem, audio_bytes = asyncio.run(
                            converter_pdf_mp3(
                                conv['arquivo_bytes'],
                                conv['arquivo_nome'],
                                conv['saida'],
                                conv['inicio'],
                                conv['fim'],
                                conv['voz_code']
                            )
                        )

                        # Adicionar ao histórico
                        st.session_state.historico.append({
                            'arquivo': conv['arquivo_nome'],
                            'saida': conv['saida'],
                            'paginas': f"{conv['inicio']}-{conv['fim']}",
                            'voz': conv['voz_nome'],
                            'timestamp': datetime.now().strftime("%H:%M:%S"),
                            'status': 'Sucesso' if sucesso else 'Erro'
                        })

                    progress_bar.progress(1.0)
                    status_text.text(f"✅ Todas as {total} conversões foram processadas!")

                    # Limpar fila
                    st.session_state.fila_conversoes = []
                    st.balloons()
                    st.rerun()

            with col2:
                if st.button("🧹 Limpar Fila", use_container_width=True):
                    st.session_state.fila_conversoes = []
                    st.rerun()

    # TAB 3: Histórico
    with tab3:
        st.header("Histórico de Conversões")

        if not st.session_state.historico:
            st.info("📭 Nenhuma conversão realizada ainda.")
        else:
            st.success(f"📊 {len(st.session_state.historico)} conversão(ões) no histórico")

            # Mostrar histórico em tabela
            import pandas as pd
            df = pd.DataFrame(st.session_state.historico)

            # Aplicar formatação condicional
            def highlight_status(val):
                color = 'lightgreen' if val == 'Sucesso' else 'lightcoral'
                return f'background-color: {color}'

            st.dataframe(
                df.style.applymap(highlight_status, subset=['status']),
                use_container_width=True
            )

            # Botão limpar histórico
            if st.button("🗑️ Limpar Histórico"):
                st.session_state.historico = []
                st.rerun()

    # Rodapé
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Desenvolvido com Python 🐍 | '
        'Powered by Edge TTS 🎤</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
