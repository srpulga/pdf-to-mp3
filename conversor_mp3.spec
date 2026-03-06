# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file para o Conversor de Midia MP3
Usa modo --onedir para compatibilidade com Streamlit
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

block_cipher = None

# Coletar todos os dados do Streamlit (assets frontend JS/CSS/HTML)
streamlit_datas = collect_data_files('streamlit')
edge_tts_datas = collect_data_files('edge_tts')

# Coletar metadados dos pacotes (necessario para importlib.metadata)
metadata_packages = [
    'streamlit', 'altair', 'pandas', 'pyarrow', 'numpy',
    'PyPDF2', 'edge_tts', 'jsonschema', 'jsonschema_specifications',
    'referencing', 'narwhals', 'pydeck', 'tornado', 'click',
    'rich', 'toml', 'packaging', 'tenacity', 'watchdog',
    'gitpython', 'protobuf', 'requests', 'pillow', 'cachetools',
]
all_metadata = []
for pkg in metadata_packages:
    try:
        all_metadata += copy_metadata(pkg)
    except Exception:
        pass

# Coletar hidden imports
streamlit_hidden = collect_submodules('streamlit')
pandas_hidden = collect_submodules('pandas._libs')

a = Analysis(
    ['scripts/launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
    ] + streamlit_datas + edge_tts_datas + all_metadata,
    hiddenimports=streamlit_hidden + pandas_hidden + [
        'pkg_resources.py2_warn',
        'altair',
        'pyarrow',
        'edge_tts',
        'asyncio',
        'PyPDF2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ConversorMP3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Manter console para ver logs do Streamlit
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if sys.platform == 'win32' else ('assets/icon.icns' if sys.platform == 'darwin' else None),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ConversorMP3',
)

# macOS: criar .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='ConversorMP3.app',
        icon='assets/icon.icns',
        bundle_identifier='com.conversormp3.app',
        info_plist={
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleName': 'Conversor MP3',
            'NSHighResolutionCapable': True,
        },
    )
