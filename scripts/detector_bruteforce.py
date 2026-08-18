"""
Detecta falhas de autenticação (Event ID 4625) e resume por usuário e IP.

NOTA: isso é uma AUDITORIA de falhas, não uma detecção de brute force de
verdade — não há threshold (ex: "5+ falhas do mesmo IP em 5 minutos").
Ver roadmap do README para o item de correlação/threshold.
"""

import sys
from collections import Counter

from core.collector import ColetaEventosError, coletar_eventos
from core.report import escrever_relatorio_contagem

EVENT_ID = 4625
COLUNAS = {
    "Usuario": 5,
    "Motivo": 8,
    "LogonType": 10,
    "Processo": 18,
    "IP": 19,
}
CAMINHO_RELATORIO = "reports/alerta_bruteforce.txt"


def main() -> int:
    try:
        eventos = coletar_eventos(EVENT_ID, COLUNAS, max_events=20)
    except ColetaEventosError as erro:
        print(f"ERRO ao coletar eventos: {erro}", file=sys.stderr)
        return 1

    if not eventos:
        print("Nenhum evento 4625 encontrado.")
        return 0

    contagem_usuarios = Counter(evento["Usuario"] for evento in eventos)
    contagem_ips = Counter(evento["IP"] for evento in eventos)

    escrever_relatorio_contagem(
        CAMINHO_RELATORIO,
        titulo="ALERTA SOC",
        total=len(eventos),
        secoes=[
            ("Usuários", dict(contagem_usuarios)),
            ("IPs", dict(contagem_ips)),
        ],
        rotulo_total="Total de falhas",
    )

    print("=== SOC Monitoring Lab ===")
    print(f"Falhas detectadas: {len(eventos)}")
    print(f"Relatório salvo em: {CAMINHO_RELATORIO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
