"""Detecta inclusão no grupo Administradores (Event ID 4732) — privilege escalation."""

import sys

from core.collector import ColetaEventosError, coletar_eventos
from core.mapeamentos import nome_usuario
from core.report import escrever_relatorio_eventos

EVENT_ID = 4732
COLUNAS = {
    "MembroSID": 1,
    "Grupo": 2,
    "DominioGrupo": 3,
    "GrupoSID": 4,
    "ExecutadoPor": 6,
    "DominioExecutor": 7,
}
CAMINHO_RELATORIO = "reports/admin_group_changes.txt"
CAMPOS = [
    ("Membro", "MembroNome"),
    ("Membro SID", "MembroSID"),
    ("Grupo", "Grupo"),
    ("Grupo SID", "GrupoSID"),
    ("Executado por", "ExecutadoPor"),
    ("Data evento", "Data"),
]


def adicionar_nome(evento: dict) -> dict:
    return {**evento, "MembroNome": nome_usuario(evento["MembroSID"])}


def main() -> int:
    try:
        eventos = coletar_eventos(EVENT_ID, COLUNAS, max_events=10)
    except ColetaEventosError as erro:
        print(f"ERRO ao coletar eventos: {erro}", file=sys.stderr)
        return 1

    eventos_admin = [e for e in eventos if e["Grupo"].lower() == "administradores"]

    escrever_relatorio_eventos(
        CAMINHO_RELATORIO,
        titulo="ALERTA SOC - ALTERAÇÃO EM GRUPO ADMINISTRATIVO",
        eventos=eventos_admin,
        campos=CAMPOS,
        rotulo_total="Total de eventos administrativos detectados",
        transformar=adicionar_nome,
    )

    print("=== SOC Monitoring Lab ===")
    print(f"Eventos administrativos detectados: {len(eventos_admin)}")
    print(f"Relatório salvo em: {CAMINHO_RELATORIO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
