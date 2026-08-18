"""Audita logons bem-sucedidos de contas humanas (Event ID 4624)."""

import sys

from core.collector import ColetaEventosError, coletar_eventos
from core.report import escrever_relatorio_eventos

EVENT_ID = 4624
COLUNAS = {
    "Usuario": 5,
    "Dominio": 6,
    "LogonType": 8,
    "Processo": 17,
    "IP": 18,
}
CAMINHO_RELATORIO = "reports/logons_sucesso.txt"
TIPOS_HUMANOS = {"2", "7", "10", "11"}
CAMPOS = [
    ("Usuário", "Usuario"),
    ("Domínio", "Dominio"),
    ("Logon Type", "LogonType"),
    ("Processo", "Processo"),
    ("IP", "IP"),
    ("Data evento", "Data"),
]


def eh_logon_humano(evento: dict) -> bool:
    return (
        evento["LogonType"] in TIPOS_HUMANOS
        and evento["Usuario"].upper() not in {"SISTEMA", "SYSTEM"}
    )


def main() -> int:
    try:
        eventos = coletar_eventos(EVENT_ID, COLUNAS, max_events=50)
    except ColetaEventosError as erro:
        print(f"ERRO ao coletar eventos: {erro}", file=sys.stderr)
        return 1

    logons_humanos = [e for e in eventos if eh_logon_humano(e)]

    escrever_relatorio_eventos(
        CAMINHO_RELATORIO,
        titulo="RELATÓRIO SOC - LOGONS BEM-SUCEDIDOS",
        eventos=logons_humanos,
        campos=CAMPOS,
        rotulo_total="Total de logons humanos detectados",
    )

    print("=== SOC Monitoring Lab ===")
    print(f"Logons humanos detectados: {len(logons_humanos)}")
    print(f"Relatório salvo em: {CAMINHO_RELATORIO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
