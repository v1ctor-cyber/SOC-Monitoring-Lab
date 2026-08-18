"""
Roda todos os detectores em sequência.

Antes da refatoração, executar o laboratório inteiro exigia chamar 7
comandos separados (ver README). Como agora cada detector expõe uma
função `main()`, dá pra orquestrar todos em um único lugar — e é aqui
que entraria, no futuro, agendamento via Task Scheduler/cron.

Uso: python run_all.py   (a partir da raiz do projeto)
"""

import sys

from scripts import (
    detector_admin_group,
    detector_bruteforce,
    detector_grupo_privilegiado,
    detector_log_cleared,
    detector_logon_sucesso,
    detector_usuario_criado,
    detector_usuario_removido,
)

DETECTORES = [
    detector_bruteforce,
    detector_logon_sucesso,
    detector_usuario_criado,
    detector_usuario_removido,
    detector_grupo_privilegiado,
    detector_admin_group,
    detector_log_cleared,
]


def main() -> int:
    codigo_saida = 0
    for detector in DETECTORES:
        print(f"\n--- {detector.__name__} ---")
        resultado = detector.main()
        if resultado != 0:
            codigo_saida = resultado
    return codigo_saida


if __name__ == "__main__":
    sys.exit(main())
