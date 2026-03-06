# PDF to MP3 Converter

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

**Convert PDF documents to high-quality MP3 audio files using neural voices**

</div>

---

## About

PDF to MP3 Converter is a web application that transforms PDF documents into natural-sounding audio files using Microsoft's Edge TTS neural voices. Perfect for creating audiobooks, accessibility, or listening to documents on the go.

## Screenshots

<div align="center">

### Nova Conversao
![Nova Conversao](images/nova-conversao.png)

### Fila de Conversoes
![Fila de Conversoes](images/fila-de-conversoes.png)

### Historico de Conversoes
![Historico de Conversoes](images/historico-de-conversoes.png)

</div>

## Features

- **Web Interface** - Clean and intuitive Streamlit interface
- **10 Portuguese Voices** - Choose from masculine and feminine neural voices
- **Batch Conversion** - Queue multiple PDFs and convert them all at once
- **Page Selection** - Convert specific pages or page ranges
- **Real-time Progress** - Track conversion status with progress bars
- **Instant Download** - Download MP3 files directly from the browser
- **Conversion History** - Keep track of all your conversions
- **Cross-platform** - Works on Windows, macOS, and Linux
- **Standalone Installers** - No Python required for end users

## Installation

### Option 1: Download Installer (Recommended)

Download the latest installer for your platform from the [Releases](https://github.com/yourusername/pdftomp3/releases) page:

| Platform | File | Notes |
|----------|------|-------|
| Windows  | `ConversorMP3_Setup_x.x.x.exe` | Run the installer, follow the wizard |
| Ubuntu/Debian | `conversor-mp3_x.x.x_amd64.deb` | `sudo dpkg -i conversor-mp3_x.x.x_amd64.deb` |
| macOS    | `ConversorMP3_x.x.x.dmg` | Drag to Applications folder |

The installers bundle everything needed (including Python) - no extra setup required.

### Option 2: Run from Source

Requires Python 3.9+.

```bash
# Clone the repository
git clone https://github.com/yourusername/pdftomp3.git
cd pdftomp3

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

#### Windows Users

For convenience, Windows users can double-click [run.bat](run.bat) to start the application (requires Python to be installed).

## Usage

1. **Upload PDF** - Click to select your PDF file
2. **Configure** - Choose voice, output name, and page range
3. **Convert** - Click "Convert Now" for instant conversion or "Add to Queue" for batch processing
4. **Download** - Download your MP3 file

### Available Voices

| Voice | Type | Characteristic |
|-------|------|----------------|
| Antonio | Male | Natural and versatile |
| Francisca | Female | Natural and clear |
| Donato | Male | Deep and serious |
| Thalita | Female | Young and energetic |
| Fabio | Male | Energetic |
| Giovanna | Female | Smooth and calm |
| Humberto | Male | Mature and professional |
| Leila | Female | Professional |
| Manuela | Female | Calm and relaxing |
| Nicolau | Male | Young and dynamic |

## Project Structure

```
pdftomp3/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── config.py              # App configuration and constants
│   ├── styles.py              # Custom CSS styles
│   ├── types.py               # Data types (ConversionJob, etc.)
│   ├── services/              # Business logic
│   │   ├── conversion.py      # Conversion orchestration
│   │   ├── pdf.py             # PDF text extraction
│   │   └── tts.py             # Text-to-speech service
│   └── selectors/             # State management
│       ├── history.py         # Conversion history
│       └── voices.py          # Voice selection
├── scripts/
│   ├── launcher.py            # Entry point for packaged executable
│   └── build_exe.py           # Build script (PyInstaller)
├── tests/                     # Unit tests
├── assets/                    # App icons (ico, png, icns)
├── installers/
│   ├── windows/installer.iss  # Inno Setup script
│   ├── linux/                 # .deb package scripts
│   └── macos/                 # .dmg build script
├── .github/workflows/         # CI/CD (GitHub Actions)
├── conversor_mp3.spec         # PyInstaller spec file
├── pyproject.toml             # Project metadata
├── requirements.txt           # Python dependencies
├── run.bat                    # Windows launcher script
├── LICENSE                    # MIT License
├── CHANGELOG.md               # Version history
└── README.md                  # This file
```

## Technologies

- **[Python](https://www.python.org/)** - Core language
- **[Streamlit](https://streamlit.io/)** - Web framework
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - PDF text extraction
- **[Edge TTS](https://github.com/rany2/edge-tts)** - Neural text-to-speech
- **[Pandas](https://pandas.pydata.org/)** - Data handling

## Building Installers

### Local Build (Windows)

```bash
# Install build dependencies
pip install pyinstaller

# Build executable
python scripts/build_exe.py

# Or directly with PyInstaller
pyinstaller conversor_mp3.spec --noconfirm
```

The app bundle will be created in `dist/ConversorMP3/`.

To create the Windows installer, install [Inno Setup](https://jrsoftware.org/isinfo.php) and run:

```bash
iscc installers/windows/installer.iss
```

### Automated Build (CI/CD)

Push a version tag to trigger builds for all platforms via GitHub Actions:

```bash
git tag v2.0.0
git push origin v2.0.0
```

The workflow builds Windows (.exe), Ubuntu (.deb), and macOS (.dmg) installers and publishes them as a GitHub Release.

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions

- Add support for more languages (English, Spanish, French, etc.)
- Audio speed and pitch controls
- Mobile-friendly interface
- Docker support
- API endpoints

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Microsoft Edge TTS team for the amazing neural voices
- Streamlit team for the excellent web framework
- All contributors who help improve this project

## Support

- Report bugs or request features in the [Issues](https://github.com/yourusername/pdftomp3/issues) section
- Star this repo if you find it useful

---

<div align="center">

**Made with Python for the open source community**

</div>
