from src.config import VOZES_DISPONIVEIS


def voice_list_all() -> dict[str, str]:
    return VOZES_DISPONIVEIS


def voice_get_code(*, display_name: str) -> str:
    return VOZES_DISPONIVEIS[display_name]


def voice_get_display_names() -> list[str]:
    return list(VOZES_DISPONIVEIS.keys())
