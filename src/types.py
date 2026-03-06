from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConversionJob:
    arquivo_nome: str
    arquivo_bytes: bytes
    saida: str
    inicio: int
    fim: int
    voz_nome: str
    voz_code: str
    status: str = "Aguardando"
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


@dataclass
class HistoryEntry:
    arquivo: str
    saida: str
    paginas: str
    voz: str
    timestamp: str
    status: str


@dataclass
class ConversionResult:
    success: bool
    message: str
    audio_bytes: bytes | None = None
