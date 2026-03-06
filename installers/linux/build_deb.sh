#!/bin/bash
# Script para criar pacote .deb do Conversor MP3
# Uso: bash installers/linux/build_deb.sh
set -e

VERSION="1.0.0"
PACKAGE_NAME="conversor-mp3"
BUILD_DIR="installers/output/${PACKAGE_NAME}_${VERSION}"

echo "========================================="
echo "  Criando pacote .deb - Conversor MP3"
echo "========================================="

# Verificar se o build do PyInstaller existe
if [ ! -d "dist/ConversorMP3" ]; then
    echo "ERRO: dist/ConversorMP3 nao encontrado!"
    echo "Execute primeiro: pyinstaller conversor_mp3.spec"
    exit 1
fi

# Limpar build anterior
rm -rf "$BUILD_DIR"

# Criar estrutura do .deb
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/lib/${PACKAGE_NAME}"
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

# Copiar metadados DEBIAN
cp installers/linux/DEBIAN/control "$BUILD_DIR/DEBIAN/"
cp installers/linux/DEBIAN/postinst "$BUILD_DIR/DEBIAN/"
chmod 755 "$BUILD_DIR/DEBIAN/postinst"

# Copiar aplicacao (output do PyInstaller)
cp -r dist/ConversorMP3/* "$BUILD_DIR/usr/lib/${PACKAGE_NAME}/"

# Criar symlink script
cat > "$BUILD_DIR/usr/bin/${PACKAGE_NAME}" << 'SCRIPT'
#!/bin/bash
exec /usr/lib/conversor-mp3/ConversorMP3 "$@"
SCRIPT
chmod 755 "$BUILD_DIR/usr/bin/${PACKAGE_NAME}"

# Copiar desktop entry e icone
cp installers/linux/conversor-mp3.desktop "$BUILD_DIR/usr/share/applications/"
cp assets/icon.png "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/${PACKAGE_NAME}.png"

# Calcular tamanho instalado
INSTALLED_SIZE=$(du -sk "$BUILD_DIR/usr" | cut -f1)
echo "Installed-Size: ${INSTALLED_SIZE}" >> "$BUILD_DIR/DEBIAN/control"

# Criar pacote .deb
mkdir -p installers/output
dpkg-deb --build "$BUILD_DIR" "installers/output/${PACKAGE_NAME}_${VERSION}_amd64.deb"

# Limpar diretorio temporario
rm -rf "$BUILD_DIR"

echo ""
echo "========================================="
echo "  Pacote .deb criado com sucesso!"
echo "  installers/output/${PACKAGE_NAME}_${VERSION}_amd64.deb"
echo "========================================="
echo ""
echo "Para instalar: sudo dpkg -i installers/output/${PACKAGE_NAME}_${VERSION}_amd64.deb"
echo "Para remover:  sudo dpkg -r ${PACKAGE_NAME}"
