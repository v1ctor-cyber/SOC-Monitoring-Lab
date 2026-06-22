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
        Id=4720
    } -MaxEvents 10

    $saida = foreach ($evento in $eventos) {
        $props = $evento.Properties

        [PSCustomObject]@{
            UsuarioCriado  = $props[0].Value
            DominioCriado  = $props[1].Value
            UsuarioCriador = $props[4].Value
            DominioCriador = $props[5].Value
            Data           = $evento.TimeCreated
        }
    }

    $saida | ConvertTo-Csv -NoTypeInformation
    """
]

resultado = subprocess.run(comando, capture_output=True, text=True)

csv_texto = resultado.stdout.strip()

if not csv_texto:
    print("Nenhum evento 4720 encontrado.")
    exit()

leitor = csv.DictReader(StringIO(csv_texto))
eventos = list(leitor)

Path("reports").mkdir(exist_ok=True)

caminho_relatorio = "reports/contas_criadas.txt"

with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
    arquivo.write("=== ALERTA SOC - CRIAÇÃO DE USUÁRIO ===\n\n")
    arquivo.write(f"Data do relatório: {datetime.now():%d/%m/%Y %H:%M:%S}\n")
    arquivo.write(f"Total de contas criadas detectadas: {len(eventos)}\n\n")

    for evento in eventos:
        arquivo.write(f"Conta criada : {evento['UsuarioCriado']}\n")
        arquivo.write(f"Domínio      : {evento['DominioCriado']}\n")
        arquivo.write(f"Criada por   : {evento['UsuarioCriador']}\n")
        arquivo.write(f"Data evento  : {evento['Data']}\n")
        arquivo.write("-" * 40 + "\n")

print("=== SOC Monitoring Lab ===\n")
print(f"Eventos 4720 detectados: {len(eventos)}")
print(f"Relatório salvo em: {caminho_relatorio}")