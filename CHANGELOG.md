# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-03-06

### Added
- Cross-platform installers: Windows (.exe), Ubuntu (.deb), macOS (.dmg)
- PyInstaller spec file with full Streamlit support (conversor_mp3.spec)
- GitHub Actions CI/CD pipeline for automated builds
- Inno Setup script for professional Windows installer
- .deb packaging scripts for Ubuntu/Debian
- create-dmg script for macOS disk image
- Placeholder app icons for all platforms (assets/)
- pyproject.toml with project metadata

### Changed
- Refactored project into modular architecture (services, selectors, config, types)
- Moved launcher and build scripts to scripts/ directory
- Launcher now uses streamlit.web.bootstrap.run() for frozen executable compatibility
- Output directory resolves to ~/ConversorMP3/output/ when running as packaged app
- Updated Python requirement to 3.9+ (dropped 3.7 support)

### Technical
- PyInstaller --onedir mode with Streamlit data files and metadata collection
- Automated builds via GitHub Actions on tag push (v*)
- Matrix builds across Windows, Ubuntu 22.04, and macOS

## [1.0.0] - 2024-11-29

### Added
- Initial release of PDF to MP3 Converter
- Web interface with Streamlit
- 10 Portuguese (Brazil) neural voices
- Batch PDF conversion support
- Page range selection
- Real-time progress tracking
- Conversion history
- Cross-platform support (Windows, macOS, Linux)
- Download MP3 files directly from browser
- Windows batch script launcher (run.bat)
- Executable builder script (build_exe.py)

### Features
- **Voices**: Antonio, Francisca, Donato, Thalita, Fabio, Giovanna, Humberto, Leila, Manuela, Nicolau
- **Format**: High-quality MP3 audio output
- **Interface**: Clean and intuitive web interface
- **Output**: All MP3 files saved to output/ directory

### Technical
- Python 3.7+ compatibility
- PyPDF2 for PDF text extraction
- Edge TTS for neural text-to-speech
- Streamlit for web interface
- Pandas for data handling
