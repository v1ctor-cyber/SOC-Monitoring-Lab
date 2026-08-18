"""Monitora alterações em grupos (Event ID 4728) e resolve SIDs para nomes."""

import sys

from core.collector import ColetaEventosError, coletar_eventos
from core.mapeamentos import nome_grupo, nome_usuario
from core.report import escrever_relatorio_eventos

EVENT_ID = 4728
COLUNAS = {
    "MembroSID": 1,
    "Dominio": 3,
    "GrupoSID": 4,
    "ExecutadoPor": 6,
    "DominioExecutor": 7,
}
CAMINHO_RELATORIO = "reports/grupos_privilegiados.txt"
CAMPOS = [
    ("Membro", "MembroNome"),
    ("Membro SID", "MembroSID"),
    ("Grupo", "GrupoNome"),
    ("Grupo SID", "GrupoSID"),
    ("Executado por", "ExecutadoPor"),
    ("Data evento", "Data"),
]


def adicionar_nomes(evento: dict) -> dict:
    """Acrescenta os nomes legíveis a partir dos SIDs, sem alterar o original."""
    return {
        **evento,
        "MembroNome": nome_usuario(evento["MembroSID"]),
        "GrupoNome": nome_grupo(evento["GrupoSID"]),
    }


def main() -> int:
    try:
        eventos = coletar_eventos(EVENT_ID, COLUNAS, max_events=10)
    except ColetaEventosError as erro:
        print(f"ERRO ao coletar eventos: {erro}", file=sys.stderr)
        return 1

    escrever_relatorio_eventos(
        CAMINHO_RELATORIO,
        titulo="ALERTA SOC - ALTERAÇÃO EM GRUPO",
        eventos=eventos,
        campos=CAMPOS,
        rotulo_total="Total de eventos 4728 detectados",
        transformar=adicionar_nomes,
    )

    print("=== SOC Monitoring Lab ===")
    print(f"Eventos 4728 detectados: {len(eventos)}")
    print(f"Relatório salvo em: {CAMINHO_RELATORIO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
