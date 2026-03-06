"""
Script para criar executaveis e instaladores
Uso: python build_exe.py
"""
import os
import sys
import subprocess


def check_pyinstaller():
    """Verifica se PyInstaller esta instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Instala PyInstaller"""
    print("Instalando PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)


def build():
    """Cria o executavel usando o spec file"""
    print("\n" + "=" * 60)
    print("    CRIANDO EXECUTAVEL - CONVERSOR MP3")
    print("=" * 60 + "\n")

    # Verificar PyInstaller
    if not check_pyinstaller():
        print("PyInstaller nao encontrado.")
        resposta = input("Deseja instalar? (s/n): ").lower()
        if resposta == 's':
            install_pyinstaller()
        else:
            print("Abortando...")
            return

    print("Construindo executavel com spec file...")
    print("Isso pode demorar alguns minutos...\n")

    try:
        subprocess.run(
            ["pyinstaller", "conversor_mp3.spec", "--noconfirm"],
            check=True
        )

        print("\n" + "=" * 60)
        print("    SUCESSO!")
        print("=" * 60)
        print("\nExecutavel criado em: dist/ConversorMP3/")
        print("\nPara distribuir no Windows, use o Inno Setup:")
        print("  iscc installers/windows/installer.iss")
        print("\n" + "=" * 60 + "\n")

    except subprocess.CalledProcessError as e:
        print(f"\nERRO ao criar executavel: {e}")
        print("Tente instalar novamente o PyInstaller:")
        print("  pip install --upgrade pyinstaller")


def main():
    """Funcao principal"""
    if not os.path.exists("conversor_mp3.spec"):
        print("ERRO: conversor_mp3.spec nao encontrado!")
        print("Execute este script na pasta raiz do projeto.")
        return

    if not os.path.exists("src/app.py"):
        print("ERRO: src/app.py nao encontrado!")
        return

    print("Projeto encontrado!")
    print("\nEste script ira criar o executavel usando PyInstaller.")
    print("O processo pode demorar alguns minutos.\n")

    resposta = input("Deseja continuar? (s/n): ").lower()
    if resposta == 's':
        build()
    else:
        print("Operacao cancelada.")


if __name__ == "__main__":
    main()
