from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from src.types import HistoryEntry


def history_init() -> None:
    if 'historico' not in st.session_state:
        st.session_state.historico = []


def history_get_all() -> list[HistoryEntry]:
    return st.session_state.historico


def history_add(*, entry: HistoryEntry) -> None:
    st.session_state.historico.append(entry)


def history_add_from_result(
    *,
    arquivo: str,
    saida: str,
    inicio: int,
    fim: int,
    voz_nome: str,
    success: bool,
) -> None:
    entry = HistoryEntry(
        arquivo=arquivo,
        saida=saida,
        paginas=f"{inicio}-{fim}",
        voz=voz_nome,
        timestamp=datetime.now().strftime("%H:%M:%S"),
        status="Sucesso" if success else "Erro",
    )
    history_add(entry=entry)


def history_as_dataframe() -> pd.DataFrame:
    entries = history_get_all()
    if not entries:
        return pd.DataFrame()
    return pd.DataFrame([
        {
            'arquivo': e.arquivo,
            'saida': e.saida,
            'paginas': e.paginas,
            'voz': e.voz,
            'timestamp': e.timestamp,
            'status': e.status,
        }
        for e in entries
    ])


def history_clear() -> None:
    st.session_state.historico = []


def history_count() -> int:
    return len(st.session_state.historico)
