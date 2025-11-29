@echo off
title Conversor de Midia MP3
color 0A
echo ========================================
echo    CONVERSOR DE MIDIA MP3
echo    Iniciando aplicacao...
echo ========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python em: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.

REM Verificar se as dependencias estao instaladas
echo Verificando dependencias...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Dependencias nao encontradas.
    echo.
    echo Atualizando pip e instalando dependencias...
    python -m pip install --upgrade pip setuptools wheel
    echo.
    echo Instalando dependencias (pode demorar alguns minutos)...
    pip install -r requirements.txt --only-binary :all:
    if errorlevel 1 (
        echo.
        echo [AVISO] Tentativa com pacotes pre-compilados falhou.
        echo Tentando instalacao padrao...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo.
            echo [ERRO] Falha ao instalar dependencias!
            echo.
            echo Consulte o arquivo WINDOWS_INSTALL.md para solucoes.
            pause
            exit /b 1
        )
    )
)

echo [OK] Dependencias instaladas!
echo.
echo Abrindo aplicacao no navegador...
echo Aguarde alguns segundos...
echo.
echo Pressione Ctrl+C para fechar o servidor
echo ========================================
echo.

REM Executar aplicacao
python -m streamlit run src/app.py --server.headless=true --browser.gatherUsageStats=false

pause
