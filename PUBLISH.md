# Guia Rápido: Publicar no GitHub

## Passo 1: Inicializar Git

```bash
# Inicializar repositório
git init

# Adicionar todos os arquivos
git add .

# Primeiro commit
git commit -m "Initial release v1.0.0

- Web interface with Streamlit
- 10 Portuguese neural voices
- Batch conversion support
- Page range selection
- Real-time progress tracking
- Cross-platform compatibility"
```

## Passo 2: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome: `pdftomp3` ou `pdf-to-mp3-converter`
3. Descrição: `Convert PDF documents to high-quality MP3 audio files using neural voices`
4. Visibilidade: **Public**
5. **NÃO** adicione README, .gitignore ou LICENSE
6. Clique em "Create repository"

## Passo 3: Conectar e Publicar

```bash
# Adicionar remote (substitua SEU_USUARIO pelo seu username)
git remote add origin https://github.com/SEU_USUARIO/pdftomp3.git

# Renomear branch para main
git branch -M main

# Push inicial
git push -u origin main
```

## Passo 4: Configurar Repositório

### Topics (Tags)
Adicione as seguintes tags no GitHub:
- `python`
- `pdf`
- `mp3`
- `tts`
- `text-to-speech`
- `streamlit`
- `audio-conversion`
- `pdf-to-audio`
- `neural-voices`
- `accessibility`

### Sobre (About)
Adicione a descrição:
```
Convert PDF documents to high-quality MP3 audio files using neural voices
```

## Passo 5: Criar Release v1.0.0

```bash
# Criar tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial public release"
git push origin v1.0.0
```

No GitHub:
1. Vá em "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Public Release`
4. Description:
```markdown
## Initial Public Release

First stable release of PDF to MP3 Converter!

### Features
- Web interface with Streamlit
- 10 Portuguese (Brazil) neural voices
- Batch PDF conversion
- Page range selection
- Cross-platform support (Windows, macOS, Linux)
- Real-time progress tracking
- Conversion history

### Installation
```bash
pip install -r requirements.txt
streamlit run src/app.py
```
```

5. Marque como "Set as the latest release"
6. Publish release

## Passo 6: Atualizar README

Depois de publicar, atualize o README substituindo:
- `https://github.com/yourusername/pdftomp3` pelo seu URL real

```bash
# Editar README.md com o URL correto
git add README.md
git commit -m "Update GitHub URLs in README"
git push
```

## Estrutura Final

```
pdftomp3/
├── src/
│   └── app.py              # Main application
├── output/                 # Generated MP3 files (git ignored)
├── examples/               # Example PDFs
├── requirements.txt        # Dependencies
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
├── README.md              # Documentation
├── CONTRIBUTING.md        # Contribution guide
├── run.bat                # Windows launcher
├── launcher.py            # Executable launcher
└── build_exe.py           # Build script
```

## Checklist Final

- [x] Git inicializado
- [x] Repositório criado no GitHub
- [x] Código enviado
- [x] Topics configuradas
- [x] Release criada
- [x] README atualizado com URL correto
- [ ] Screenshot adicionado (opcional)

## Divulgação (Opcional)

Compartilhe em:
- Reddit: r/Python, r/opensource
- Twitter/X: #Python #OpenSource #PDF #TTS
- LinkedIn
- Dev.to

---

**Pronto! Seu projeto está publicado e pronto para receber contribuições!**
