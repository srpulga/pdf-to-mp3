import sys
from pathlib import Path

PAGE_CONFIG = {
    "page_title": "Conversor de Midia MP3",
    "page_icon": "\U0001f3b5",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

VOZES_DISPONIVEIS: dict[str, str] = {
    "Antonio (Masculina - Natural)": "pt-BR-AntonioNeural",
    "Francisca (Feminina - Natural)": "pt-BR-FranciscaNeural",
    "Donato (Masculina - Profunda)": "pt-BR-DonatoNeural",
    "Thalita (Feminina - Jovem)": "pt-BR-ThalitaNeural",
    "Fabio (Masculina - Energetica)": "pt-BR-FabioNeural",
    "Giovanna (Feminina - Suave)": "pt-BR-GiovannaNeural",
    "Humberto (Masculina - Madura)": "pt-BR-HumbertoNeural",
    "Leila (Feminina - Profissional)": "pt-BR-LeilaNeural",
    "Manuela (Feminina - Calma)": "pt-BR-ManuelaNeural",
    "Nicolau (Masculina - Jovem)": "pt-BR-NicolauNeural",
}


def get_output_dir() -> Path:
    if getattr(sys, '_MEIPASS', None):
        output_dir = Path.home() / "ConversorMP3" / "output"
    else:
        output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
