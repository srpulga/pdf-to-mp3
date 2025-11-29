"""
Script para criar executável Windows (.exe)
Uso: python build_exe.py
"""
import os
import sys
import subprocess

def check_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Instala PyInstaller"""
    print("Instalando PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe():
    """Cria o executável"""
    print("\n" + "="*60)
    print("    CRIANDO EXECUTÁVEL WINDOWS (.exe)")
    print("="*60 + "\n")

    # Verificar PyInstaller
    if not check_pyinstaller():
        print("PyInstaller não encontrado.")
        resposta = input("Deseja instalar? (s/n): ").lower()
        if resposta == 's':
            install_pyinstaller()
        else:
            print("Abortando...")
            return

    print("Construindo executável...")
    print("Isso pode demorar alguns minutos...\n")

    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Um único arquivo
        "--windowed",                   # Sem console (Windows)
        "--name=ConversorMP3",          # Nome do executável
        "--icon=NONE",                  # Sem ícone (você pode adicionar depois)
        "--add-data=src:src",           # Incluir pasta src
        "launcher.py"                   # Script principal
    ]

    try:
        subprocess.run(cmd, check=True)

        print("\n" + "="*60)
        print("    SUCESSO!")
        print("="*60)
        print("\nExecutável criado em: dist/ConversorMP3.exe")
        print("\nPara distribuir, copie:")
        print("  - dist/ConversorMP3.exe")
        print("  - src/ (pasta completa)")
        print("\n" + "="*60 + "\n")

    except subprocess.CalledProcessError as e:
        print(f"\nERRO ao criar executável: {e}")
        print("Tente instalar novamente o PyInstaller:")
        print("  pip install --upgrade pyinstaller")

def main():
    """Função principal"""
    if not os.path.exists("launcher.py"):
        print("ERRO: launcher.py não encontrado!")
        print("Execute este script na pasta raiz do projeto.")
        return

    if not os.path.exists("src/app.py"):
        print("ERRO: src/app.py não encontrado!")
        return

    print("Projeto encontrado!")
    print("\nEste script irá criar um executável (.exe) para Windows.")
    print("O processo pode demorar alguns minutos.\n")

    resposta = input("Deseja continuar? (s/n): ").lower()
    if resposta == 's':
        build_exe()
    else:
        print("Operação cancelada.")

if __name__ == "__main__":
    main()
