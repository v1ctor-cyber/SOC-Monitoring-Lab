import subprocess
import csv
from io import StringIO
from datetime import datetime
from pathlib import Path

usuarios = {
    "S-1-5-21-1764120652-1249086577-3640239003-1003": "CodexSandboxOffline",
    "S-1-5-21-1764120652-1249086577-3640239003-1004": "CodexSandboxOnline",
    "S-1-5-21-1764120652-1249086577-3640239003-1001": "vitin",
}

grupos = {
    "S-1-5-21-1764120652-1249086577-3640239003-513": "CodexSandboxUsers",
    "S-1-5-32-544": "Administradores",
    "S-1-5-32-545": "Usuários",
}

comando = [
    "powershell",
    "-Command",
    r"""
    $eventos = Get-WinEvent -FilterHashtable @{
        LogName='Security'
        Id=4728
    } -MaxEvents 10

    $saida = foreach ($evento in $eventos) {
        $props = $evento.Properties

        [PSCustomObject]@{
            MembroSID       = $props[1].Value
            Dominio         = $props[3].Value
            GrupoSID        = $props[4].Value
            ExecutadoPor    = $props[6].Value
            DominioExecutor = $props[7].Value
            Data            = $evento.TimeCreated
        }
    }

    $saida | ConvertTo-Csv -NoTypeInformation
    """
]

resultado = subprocess.run(comando, capture_output=True, text=True)
csv_texto = resultado.stdout.strip()

if not csv_texto:
    print("Nenhum evento 4728 encontrado.")
    exit()

eventos = list(csv.DictReader(StringIO(csv_texto)))

Path("reports").mkdir(exist_ok=True)
caminho_relatorio = "reports/grupos_privilegiados.txt"

with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
    arquivo.write("=== ALERTA SOC - ALTERAÇÃO EM GRUPO ===\n\n")
    arquivo.write(f"Data do relatório: {datetime.now():%d/%m/%Y %H:%M:%S}\n")
    arquivo.write(f"Total de eventos 4728 detectados: {len(eventos)}\n\n")

    for evento in eventos:
        membro_sid = evento["MembroSID"]
        grupo_sid = evento["GrupoSID"]

        membro_nome = usuarios.get(membro_sid, "Desconhecido")
        grupo_nome = grupos.get(grupo_sid, "Desconhecido")

        arquivo.write(f"Membro          : {membro_nome}\n")
        arquivo.write(f"Membro SID      : {membro_sid}\n")
        arquivo.write(f"Grupo           : {grupo_nome}\n")
        arquivo.write(f"Grupo SID       : {grupo_sid}\n")
        arquivo.write(f"Executado por   : {evento['ExecutadoPor']}\n")
        arquivo.write(f"Data evento     : {evento['Data']}\n")
        arquivo.write("-" * 40 + "\n")

print("=== SOC Monitoring Lab ===\n")
print(f"Eventos 4728 detectados: {len(eventos)}")
print(f"Relatório salvo em: {caminho_relatorio}")