"""
Launcher para o Conversor de Mídia MP3
Este arquivo é usado para criar o executável .exe
"""
import os
import sys
import subprocess
import webbrowser
import time
from threading import Thread

def open_browser():
    """Abre o navegador após alguns segundos"""
    time.sleep(3)
    webbrowser.open('http://localhost:8501')

def main():
    """Função principal"""
    # Adicionar pasta src ao path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    sys.path.insert(0, src_dir)

    # Caminho do app
    app_path = os.path.join(src_dir, 'app.py')

    if not os.path.exists(app_path):
        print("ERRO: Arquivo app.py não encontrado!")
        print(f"Procurando em: {app_path}")
        input("Pressione Enter para sair...")
        sys.exit(1)

    # Abrir navegador em thread separada
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    print("="*50)
    print("    CONVERSOR DE MÍDIA MP3")
    print("="*50)
    print("\nIniciando aplicação...")
    print("O navegador será aberto automaticamente.")
    print("\nFeche esta janela para encerrar o servidor.")
    print("="*50)

    # Executar streamlit
    try:
        subprocess.run([
            sys.executable,
            '-m',
            'streamlit',
            'run',
            app_path,
            '--server.headless=true',
            '--browser.gatherUsageStats=false'
        ])
    except KeyboardInterrupt:
        print("\nEncerrando aplicação...")
    except Exception as e:
        print(f"\nERRO: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()
