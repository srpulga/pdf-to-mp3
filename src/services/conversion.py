from __future__ import annotations

from pathlib import Path

from src.services.pdf import pdf_extract_text
from src.services.tts import tts_generate_audio
from src.types import ConversionJob, ConversionResult


async def conversion_execute(*, job: ConversionJob, output_dir: Path) -> ConversionResult:
    """Executa a conversao completa de PDF para MP3."""
    try:
        texto = pdf_extract_text(
            arquivo_bytes=job.arquivo_bytes,
            inicio=job.inicio,
            fim=job.fim,
        )

        if not texto:
            return ConversionResult(
                success=False,
                message="Nenhum texto encontrado no PDF",
            )

        saida_path = output_dir / job.saida
        audio_bytes = await tts_generate_audio(
            texto=texto,
            voz_code=job.voz_code,
            saida_path=saida_path,
        )

        return ConversionResult(
            success=True,
            message="Conversao concluida com sucesso!",
            audio_bytes=audio_bytes,
        )

    except Exception as e:
        return ConversionResult(
            success=False,
            message=f"Erro na conversao: {e}",
        )
