"""Audita remoção de contas de usuário local (Event ID 4726)."""

import sys

from core.collector import ColetaEventosError, coletar_eventos
from core.report import escrever_relatorio_eventos

EVENT_ID = 4726
COLUNAS = {
    "UsuarioRemovido": 0,
    "DominioRemovido": 1,
    "SIDRemovido": 2,
    "ExecutadoPor": 4,
    "DominioExecutor": 5,
}
CAMINHO_RELATORIO = "reports/contas_removidas.txt"
CAMPOS = [
    ("Conta removida", "UsuarioRemovido"),
    ("Domínio", "DominioRemovido"),
    ("SID removido", "SIDRemovido"),
    ("Executado por", "ExecutadoPor"),
    ("Domínio executor", "DominioExecutor"),
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
        titulo="ALERTA SOC - CONTA DE USUÁRIO REMOVIDA",
        eventos=eventos,
        campos=CAMPOS,
        rotulo_total="Total de contas removidas detectadas",
    )

    print("=== SOC Monitoring Lab ===")
    print(f"Eventos 4726 detectados: {len(eventos)}")
    print(f"Relatório salvo em: {CAMINHO_RELATORIO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
