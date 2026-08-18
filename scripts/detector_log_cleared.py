"""Detecta limpeza do Security Log (Event ID 1102) — possível evasão de rastros."""

import sys

from core.collector import ColetaEventosError, coletar_eventos
from core.report import escrever_relatorio_eventos

EVENT_ID = 1102
COLUNAS = {
    "UsuarioSID": 0,
    "Usuario": 1,
    "Host": 2,
    "LogonID": 3,
    "ProcessoID": 4,
    "RecordID": 5,
}
CAMINHO_RELATORIO = "reports/security_log_cleared.txt"
CAMPOS = [
    ("Usuário", "Usuario"),
    ("Usuário SID", "UsuarioSID"),
    ("Host", "Host"),
    ("Logon ID", "LogonID"),
    ("Processo ID", "ProcessoID"),
    ("Record ID", "RecordID"),
    ("Data evento", "Data"),
]


def main() -> int:
    try:
        eventos = coletar_eventos(EVENT_ID, COLUNAS, max_events=10)
    except ColetaEventosError as erro:
        print(f"ERRO ao coletar eventos: {erro}", file=sys.stderr)
        return 1

    escrever_relatorio_eventos(
        CAMINHO_RELATORIO,
        titulo="ALERTA SOC - SECURITY LOG APAGADO",
        eventos=eventos,
        campos=CAMPOS,
        rotulo_total="Total de eventos 1102 detectados",
    )

    print("=== SOC Monitoring Lab ===")
    print(f"Eventos 1102 detectados: {len(eventos)}")
    print(f"Relatório salvo em: {CAMINHO_RELATORIO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
