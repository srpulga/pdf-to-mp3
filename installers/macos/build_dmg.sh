#!/bin/bash
# Script para criar .dmg do Conversor MP3 no macOS
# Uso: bash installers/macos/build_dmg.sh
set -e

VERSION="1.0.0"
APP_NAME="ConversorMP3"

echo "========================================="
echo "  Criando .dmg - Conversor MP3"
echo "========================================="

# Verificar se o build do PyInstaller existe
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "ERRO: dist/${APP_NAME}.app nao encontrado!"
    echo "Execute primeiro: pyinstaller conversor_mp3.spec"
    exit 1
fi

# Verificar se create-dmg esta instalado
if ! command -v create-dmg &> /dev/null; then
    echo "Instalando create-dmg..."
    brew install create-dmg
fi

# Converter PNG para ICNS se necessario
if [ ! -f "assets/icon.icns" ] && [ -f "assets/icon.png" ]; then
    echo "Gerando icon.icns a partir do PNG..."
    ICONSET="assets/icon.iconset"
    mkdir -p "$ICONSET"
    sips -z 16 16     assets/icon.png --out "$ICONSET/icon_16x16.png"
    sips -z 32 32     assets/icon.png --out "$ICONSET/icon_16x16@2x.png"
    sips -z 32 32     assets/icon.png --out "$ICONSET/icon_32x32.png"
    sips -z 64 64     assets/icon.png --out "$ICONSET/icon_32x32@2x.png"
    sips -z 128 128   assets/icon.png --out "$ICONSET/icon_128x128.png"
    sips -z 256 256   assets/icon.png --out "$ICONSET/icon_128x128@2x.png"
    sips -z 256 256   assets/icon.png --out "$ICONSET/icon_256x256.png"
    sips -z 512 512   assets/icon.png --out "$ICONSET/icon_256x256@2x.png"
    sips -z 512 512   assets/icon.png --out "$ICONSET/icon_512x512.png"
    sips -z 1024 1024 assets/icon.png --out "$ICONSET/icon_512x512@2x.png" 2>/dev/null || \
    cp assets/icon.png "$ICONSET/icon_512x512@2x.png"
    iconutil -c icns "$ICONSET" -o assets/icon.icns
    rm -rf "$ICONSET"
fi

# Criar diretorio de output
mkdir -p installers/output

# Limpar DMG anterior
rm -f "installers/output/${APP_NAME}_${VERSION}.dmg"

# Criar DMG com create-dmg
create-dmg \
    --volname "${APP_NAME}" \
    --volicon "assets/icon.icns" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "${APP_NAME}.app" 150 185 \
    --hide-extension "${APP_NAME}.app" \
    --app-drop-link 450 185 \
    --no-internet-enable \
    "installers/output/${APP_NAME}_${VERSION}.dmg" \
    "dist/${APP_NAME}.app"

echo ""
echo "========================================="
echo "  DMG criado com sucesso!"
echo "  installers/output/${APP_NAME}_${VERSION}.dmg"
echo "========================================="
echo ""
echo "NOTA: Se o app nao estiver assinado, o usuario precisara:"
echo "  xattr -cr /Applications/${APP_NAME}.app"
echo "  ou: Preferencias do Sistema > Seguranca > Abrir Mesmo Assim"
