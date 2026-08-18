"""
core/collector.py

Responsável por UMA coisa só: falar com o Windows Event Log e devolver
uma lista de dicionários Python. Nenhum detector individual deve montar
comando PowerShell ou fazer parsing de CSV por conta própria — todos
chamam `coletar_eventos()` daqui.

Isso existe porque, antes desse módulo, os 7 scripts do projeto
duplicavam exatamente essa lógica (subprocess + PowerShell + CSV),
mudando só o Event ID e as colunas. Qualquer correção de bug tinha
que ser copiada em 7 arquivos. Agora existe em um lugar só.
"""

import csv
import subprocess
from io import StringIO


class ColetaEventosError(Exception):
    """Erro ao coletar eventos do Windows Event Log."""


def _montar_script_powershell(event_id: int, colunas: dict[str, int], max_events: int) -> str:
    """
    Monta o script PowerShell que extrai as colunas pedidas de um Event ID.

    `colunas` é um dict {nome_da_coluna: indice_na_propriedade}, na ordem
    em que devem aparecer no CSV de saída. O campo "Data" (TimeCreated)
    é sempre incluído automaticamente — nenhum detector precisa declarar.
    """
    linhas_propriedades = "\n".join(
        f"            {nome} = $props[{indice}].Value"
        for nome, indice in colunas.items()
    )

    return f"""
    $eventos = Get-WinEvent -FilterHashtable @{{
        LogName='Security'
        Id={event_id}
    }} -MaxEvents {max_events} -ErrorAction Stop

    $saida = foreach ($evento in $eventos) {{
        $props = $evento.Properties

        [PSCustomObject]@{{
{linhas_propriedades}
            Data = $evento.TimeCreated
        }}
    }}

    $saida | ConvertTo-Csv -NoTypeInformation
    """


def coletar_eventos(event_id: int, colunas: dict[str, int], max_events: int = 20) -> list[dict]:
    """
    Coleta eventos do Security Log do Windows para um Event ID específico.

    Retorna uma lista de dicionários (um por evento), cada um contendo as
    chaves de `colunas` mais "Data". Lista vazia significa "não há eventos
    desse tipo no momento" — isso é diferente de erro de coleta, que
    levanta ColetaEventosError em vez de falhar silenciosamente.
    """
    script = _montar_script_powershell(event_id, colunas, max_events)
    comando = ["powershell", "-NoProfile", "-Command", script]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise ColetaEventosError(
            f"PowerShell não respondeu em 30s ao coletar Event ID {event_id}."
        ) from exc

    if resultado.returncode != 0:
        # Isso cobre, por exemplo, falta de permissão (precisa rodar como
        # Administrador) ou o log 'Security' não existir nessa máquina.
        # Antes, um erro aqui virava silenciosamente "Nenhum evento encontrado",
        # o que é perigoso: silêncio não deveria significar "está tudo bem".
        raise ColetaEventosError(
            f"PowerShell falhou ao coletar Event ID {event_id}: "
            f"{resultado.stderr.strip() or 'sem detalhes de erro'}"
        )

    csv_texto = resultado.stdout.strip()
    if not csv_texto:
        return []

    return list(csv.DictReader(StringIO(csv_texto)))
