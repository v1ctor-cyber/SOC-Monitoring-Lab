import subprocess
import csv
from io import StringIO
from datetime import datetime
from pathlib import Path

TIPOS_HUMANOS = {"2", "7", "10", "11"}

comando = [
    "powershell",
    "-Command",
    r"""
    $eventos = Get-WinEvent -FilterHashtable @{
        LogName='Security'
        Id=4624
    } -MaxEvents 50

    $saida = foreach ($evento in $eventos) {
        $props = $evento.Properties

        [PSCustomObject]@{
            Usuario   = $props[5].Value
            Dominio   = $props[6].Value
            LogonType = $props[8].Value
            Processo  = $props[17].Value
            IP        = $props[18].Value
            Data      = $evento.TimeCreated
        }
    }

    $saida | ConvertTo-Csv -NoTypeInformation
    """
]

resultado = subprocess.run(comando, capture_output=True, text=True)
csv_texto = resultado.stdout.strip()

if not csv_texto:
    print("Nenhum evento 4624 encontrado.")
    exit()

eventos = list(csv.DictReader(StringIO(csv_texto)))

logons_humanos = [
    evento for evento in eventos
    if evento["LogonType"] in TIPOS_HUMANOS
    and evento["Usuario"].upper() not in ["SISTEMA", "SYSTEM"]
]

Path("reports").mkdir(exist_ok=True)
caminho_relatorio = "reports/logons_sucesso.txt"

with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
    arquivo.write("=== RELATÓRIO SOC - LOGONS BEM-SUCEDIDOS ===\n\n")
    arquivo.write(f"Data do relatório: {datetime.now():%d/%m/%Y %H:%M:%S}\n")
    arquivo.write(f"Total de logons humanos detectados: {len(logons_humanos)}\n\n")

    for evento in logons_humanos:
        arquivo.write(f"Usuário     : {evento['Usuario']}\n")
        arquivo.write(f"Domínio     : {evento['Dominio']}\n")
        arquivo.write(f"Logon Type  : {evento['LogonType']}\n")
        arquivo.write(f"Processo    : {evento['Processo']}\n")
        arquivo.write(f"IP          : {evento['IP']}\n")
        arquivo.write(f"Data evento : {evento['Data']}\n")
        arquivo.write("-" * 40 + "\n")

print("=== SOC Monitoring Lab ===\n")
print(f"Logons humanos detectados: {len(logons_humanos)}")
print(f"Relatório salvo em: {caminho_relatorio}")