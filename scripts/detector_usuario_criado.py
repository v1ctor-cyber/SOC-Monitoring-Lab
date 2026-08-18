"""Detecta criação de contas de usuário local (Event ID 4720)."""

import sys

from core.collector import ColetaEventosError, coletar_eventos
from core.report import escrever_relatorio_eventos

EVENT_ID = 4720
COLUNAS = {
    "UsuarioCriado": 0,
    "DominioCriado": 1,
    "UsuarioCriador": 4,
    "DominioCriador": 5,
}
CAMINHO_RELATORIO = "reports/contas_criadas.txt"
CAMPOS = [
    ("Conta criada", "UsuarioCriado"),
    ("Domínio", "DominioCriado"),
    ("Criada por", "UsuarioCriador"),
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
        titulo="ALERTA SOC - CRIAÇÃO DE USUÁRIO",
        eventos=eventos,
        campos=CAMPOS,
        rotulo_total="Total de contas criadas detectadas",
    )

    print("=== SOC Monitoring Lab ===")
    print(f"Eventos 4720 detectados: {len(eventos)}")
    print(f"Relatório salvo em: {CAMINHO_RELATORIO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
