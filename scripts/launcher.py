"""
Launcher para o Conversor de Midia MP3
Este arquivo e usado como entry point para o executavel empacotado
"""
import os
import sys

# IMPORTANTE: Forcar modo producao ANTES de qualquer import do Streamlit.
# Sem isso, o Streamlit detecta developmentMode=True no PyInstaller
# (porque __file__ nao contem "site-packages") e tenta conectar ao
# servidor de desenvolvimento React em localhost:3000, causando 404.
os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"

import webbrowser
import time
from threading import Thread


def get_base_path():
    """Retorna o caminho base, seja rodando como script ou como executavel frozen."""
    if getattr(sys, '_MEIPASS', None):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def open_browser():
    """Abre o navegador apos alguns segundos"""
    time.sleep(3)
    webbrowser.open('http://localhost:8501')


def main():
    """Funcao principal"""
    base = get_base_path()
    app_path = os.path.join(base, 'src', 'app.py')

    if not os.path.exists(app_path):
        print("ERRO: Arquivo app.py nao encontrado!")
        print(f"Procurando em: {app_path}")
        input("Pressione Enter para sair...")
        sys.exit(1)

    # Abrir navegador em thread separada
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    print("=" * 50)
    print("    CONVERSOR DE MIDIA MP3")
    print("=" * 50)
    print("\nIniciando aplicacao...")
    print("O navegador sera aberto automaticamente.")
    print("\nFeche esta janela para encerrar o servidor.")
    print("=" * 50)

    # Usar bootstrap.run() diretamente em vez de subprocess
    # Isso e essencial para funcionar quando empacotado com PyInstaller
    try:
        from streamlit.web.bootstrap import load_config_options, run
        flag_options = {
            "global.developmentMode": False,
            "server.headless": True,
            "browser.gatherUsageStats": False,
            "server.port": 8501,
        }
        # Aplicar config ANTES de iniciar o servidor.
        # bootstrap.run() nao aplica flag_options imediatamente — so registra
        # um callback para recarregar. Sem esta chamada, o Streamlit usa os
        # defaults e detecta developmentMode=True no PyInstaller.
        load_config_options(flag_options)
        run(app_path, False, [], flag_options)
    except KeyboardInterrupt:
        print("\nEncerrando aplicacao...")
    except Exception as e:
        print(f"\nERRO: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)


if __name__ == "__main__":
    main()
