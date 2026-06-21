import subprocess
import csv
from io import StringIO
from collections import Counter
from datetime import datetime
from pathlib import Path

comando = [
    "powershell",
    "-Command",
    r"""
    $eventos = Get-WinEvent -FilterHashtable @{
        LogName='Security'
        Id=4625
    } -MaxEvents 20

    $saida = foreach ($evento in $eventos) {
        $props = $evento.Properties

        [PSCustomObject]@{
            Usuario   = $props[5].Value
            Motivo    = $props[8].Value
            LogonType = $props[10].Value
            Processo  = $props[18].Value
            IP        = $props[19].Value
        }
    }

    $saida | ConvertTo-Csv -NoTypeInformation
    """
]

resultado = subprocess.run(
    comando,
    capture_output=True,
    text=True
)

csv_texto = resultado.stdout.strip()

if not csv_texto:
    print("Nenhum evento encontrado.")
    exit()

leitor = csv.DictReader(StringIO(csv_texto))

usuarios = []
ips = []

for linha in leitor:
    usuarios.append(linha["Usuario"])
    ips.append(linha["IP"])

contagem_usuarios = Counter(usuarios)
contagem_ips = Counter(ips)

total_falhas = len(usuarios)

print("=== SOC Monitoring Lab ===")
print(f"Falhas detectadas: {total_falhas}")

Path("reports").mkdir(exist_ok=True)

with open(
    "reports/alerta_bruteforce.txt",
    "w",
    encoding="utf-8"
) as arquivo:

    arquivo.write("=== ALERTA SOC ===\n\n")
    arquivo.write(
        f"Data: {datetime.now():%d/%m/%Y %H:%M:%S}\n"
    )

    arquivo.write(
        f"Total de falhas: {total_falhas}\n\n"
    )

    arquivo.write("Usuários:\n")

    for usuario, qtd in contagem_usuarios.items():
        arquivo.write(
            f"- {usuario}: {qtd}\n"
        )

    arquivo.write("\nIPs:\n")

    for ip, qtd in contagem_ips.items():
        arquivo.write(
            f"- {ip}: {qtd}\n"
        )

print(
    "\nRelatório salvo em:"
)
print(
    "reports/alerta_bruteforce.txt"
)