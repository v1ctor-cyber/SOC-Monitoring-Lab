import subprocess
import csv
from io import StringIO
from datetime import datetime
from pathlib import Path

comando = [
    "powershell",
    "-Command",
    r"""
    $eventos = Get-WinEvent -FilterHashtable @{
        LogName='Security'
        Id=1102
    } -MaxEvents 10

    $saida = foreach ($evento in $eventos) {
        $props = $evento.Properties

        [PSCustomObject]@{
            UsuarioSID = $props[0].Value
            Usuario    = $props[1].Value
            Host       = $props[2].Value
            LogonID    = $props[3].Value
            ProcessoID = $props[4].Value
            RecordID   = $props[5].Value
            Data       = $evento.TimeCreated
        }
    }

    $saida | ConvertTo-Csv -NoTypeInformation
    """
]

resultado = subprocess.run(comando, capture_output=True, text=True)
csv_texto = resultado.stdout.strip()

if not csv_texto:
    print("Nenhum evento 1102 encontrado.")
    exit()

eventos = list(csv.DictReader(StringIO(csv_texto)))

Path("reports").mkdir(exist_ok=True)
caminho_relatorio = "reports/security_log_cleared.txt"

with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
    arquivo.write("=== ALERTA SOC - SECURITY LOG APAGADO ===\n\n")
    arquivo.write(f"Data do relatório: {datetime.now():%d/%m/%Y %H:%M:%S}\n")
    arquivo.write(f"Total de eventos 1102 detectados: {len(eventos)}\n\n")

    for evento in eventos:
        arquivo.write(f"Usuário      : {evento['Usuario']}\n")
        arquivo.write(f"Usuário SID  : {evento['UsuarioSID']}\n")
        arquivo.write(f"Host         : {evento['Host']}\n")
        arquivo.write(f"Logon ID     : {evento['LogonID']}\n")
        arquivo.write(f"Processo ID  : {evento['ProcessoID']}\n")
        arquivo.write(f"Record ID    : {evento['RecordID']}\n")
        arquivo.write(f"Data evento  : {evento['Data']}\n")
        arquivo.write("-" * 40 + "\n")

print("=== SOC Monitoring Lab ===\n")
print(f"Eventos 1102 detectados: {len(eventos)}")
print(f"Relatório salvo em: {caminho_relatorio}")