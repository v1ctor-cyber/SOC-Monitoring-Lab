"""
core/mapeamentos.py

SIDs do Windows não são legíveis ("S-1-5-21-...-1005" não diz nada pra
quem lê o relatório). Esses dicionários traduzem SID → nome conhecido
NESTE laboratório específico.

Isso estava duplicado em detector_admin_group.py e
detector_grupo_privilegiado.py — cada um com sua própria cópia parcial
dos mesmos dados. Centralizado aqui, é editado em um lugar só.

IMPORTANTE (limitação conhecida, vale documentar no README): esses SIDs
são específicos da máquina onde o laboratório foi montado. Em outra
máquina/domínio, os SIDs de usuário mudam — isso é esperado, o lab é
um ambiente de estudo local, não uma ferramenta portátil "out of the box".
Uma evolução futura seria resolver o nome dinamicamente via
`Get-LocalUser`/`Get-ADUser` em vez de um dicionário fixo.
"""

USUARIOS: dict[str, str] = {
    "S-1-5-21-1764120652-1249086577-3640239003-1001": "vitin",
    "S-1-5-21-1764120652-1249086577-3640239003-1003": "CodexSandboxOffline",
    "S-1-5-21-1764120652-1249086577-3640239003-1004": "CodexSandboxOnline",
    "S-1-5-21-1764120652-1249086577-3640239003-1005": "socadmin",
}

GRUPOS: dict[str, str] = {
    "S-1-5-21-1764120652-1249086577-3640239003-513": "CodexSandboxUsers",
    "S-1-5-32-544": "Administradores",
    "S-1-5-32-545": "Usuários",
}


def nome_usuario(sid: str) -> str:
    return USUARIOS.get(sid, "Desconhecido")


def nome_grupo(sid: str) -> str:
    return GRUPOS.get(sid, "Desconhecido")
