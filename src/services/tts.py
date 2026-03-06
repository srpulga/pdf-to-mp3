from pathlib import Path

import edge_tts


async def tts_generate_audio(*, texto: str, voz_code: str, saida_path: Path) -> bytes:
    """Gera audio MP3 a partir de texto usando Edge TTS."""
    comunicacao = edge_tts.Communicate(texto, voz_code)
    await comunicacao.save(str(saida_path))

    with open(saida_path, 'rb') as f:
        return f.read()
