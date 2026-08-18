"""
core/report.py

Responsável por UMA coisa só: escrever o relatório .txt em disco, no
formato padrão do SOC Monitoring Lab. Nenhum detector formata texto de
relatório por conta própria.

Dois formatos são suportados:
- `escrever_relatorio_eventos`: lista evento por evento (a maioria dos
  detectores usa esse).
- `escrever_relatorio_contagem`: agrega por contagem (usado pelo
  detector de brute force, que resume "quantas falhas por usuário/IP"
  em vez de listar cada falha individualmente).
"""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

SEPARADOR = "-" * 40


def _cabecalho(titulo: str, total: int, rotulo_total: str) -> str:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return (
        f"=== {titulo} ===\n\n"
        f"Data do relatório: {agora}\n"
        f"{rotulo_total}: {total}\n\n"
    )


def escrever_relatorio_eventos(
    caminho: str,
    titulo: str,
    eventos: list[dict],
    campos: list[tuple[str, str]],
    rotulo_total: str = "Total de eventos detectados",
    transformar: Callable[[dict], dict] | None = None,
) -> None:
    """
    Escreve um relatório listando evento por evento.

    `campos` é uma lista de (rotulo_exibido, chave_no_evento), na ordem
    em que devem aparecer — ex: [("Usuário", "Usuario"), ("Domínio", "Dominio")].

    `transformar`, se passado, roda em cada evento antes de exibir — é o
    lugar certo para trocar um SID por um nome legível (ver core/mapeamentos.py),
    em vez de cada detector reimplementar esse lookup na hora de escrever.
    """
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(_cabecalho(titulo, len(eventos), rotulo_total))

        for evento in eventos:
            evento_exibido = transformar(evento) if transformar else evento
            for rotulo, chave in campos:
                valor = evento_exibido.get(chave, "-")
                arquivo.write(f"{rotulo:<15}: {valor}\n")
            arquivo.write(SEPARADOR + "\n")


def escrever_relatorio_contagem(
    caminho: str,
    titulo: str,
    total: int,
    secoes: list[tuple[str, dict[str, int]]],
    rotulo_total: str = "Total de eventos detectados",
) -> None:
    """
    Escreve um relatório agregado por contagem, em seções.

    `secoes` é uma lista de (nome_da_secao, {chave: quantidade}) — ex:
    [("Usuários", {"admin": 3}), ("IPs", {"10.0.0.5": 3})].
    """
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(_cabecalho(titulo, total, rotulo_total))

        for nome_secao, contagem in secoes:
            arquivo.write(f"{nome_secao}:\n")
            for chave, qtd in contagem.items():
                arquivo.write(f"- {chave}: {qtd}\n")
            arquivo.write("\n")
