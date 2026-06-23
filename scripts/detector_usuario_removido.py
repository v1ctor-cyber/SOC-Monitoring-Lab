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
        Id=4726
    } -MaxEvents 10

    $saida = foreach ($evento in $eventos) {
        $props = $evento.Properties

        [PSCustomObject]@{
            UsuarioRemovido = $props[0].Value
            DominioRemovido = $props[1].Value
            SIDRemovido     = $props[2].Value
            ExecutadoPor    = $props[4].Value
            DominioExecutor = $props[5].Value
            Data            = $evento.TimeCreated
        }
    }

    $saida | ConvertTo-Csv -NoTypeInformation
    """
]

resultado = subprocess.run(comando, capture_output=True, text=True)
csv_texto = resultado.stdout.strip()

if not csv_texto:
    print("Nenhum evento 4726 encontrado.")
    exit()

eventos = list(csv.DictReader(StringIO(csv_texto)))

Path("reports").mkdir(exist_ok=True)
caminho_relatorio = "reports/contas_removidas.txt"

with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
    arquivo.write("=== ALERTA SOC - CONTA DE USUÁRIO REMOVIDA ===\n\n")
    arquivo.write(f"Data do relatório: {datetime.now():%d/%m/%Y %H:%M:%S}\n")
    arquivo.write(f"Total de contas removidas detectadas: {len(eventos)}\n\n")

    for evento in eventos:
        arquivo.write(f"Conta removida    : {evento['UsuarioRemovido']}\n")
        arquivo.write(f"Domínio           : {evento['DominioRemovido']}\n")
        arquivo.write(f"SID removido      : {evento['SIDRemovido']}\n")
        arquivo.write(f"Executado por     : {evento['ExecutadoPor']}\n")
        arquivo.write(f"Domínio executor  : {evento['DominioExecutor']}\n")
        arquivo.write(f"Data evento       : {evento['Data']}\n")
        arquivo.write("-" * 40 + "\n")

print("=== SOC Monitoring Lab ===\n")
print(f"Eventos 4726 detectados: {len(eventos)}")
print(f"Relatório salvo em: {caminho_relatorio}")