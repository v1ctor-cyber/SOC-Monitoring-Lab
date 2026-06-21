# SOC Monitoring Lab

Laboratório prático de monitoramento de segurança baseado em logs do Windows.

## Objetivo

Este projeto simula atividades realizadas por um analista SOC L1, usando logs reais do Windows para identificar falhas de autenticação, possíveis tentativas de brute force e gerar relatórios de alerta.

## Funcionalidades

- Análise de eventos do Windows Security Log
- Detecção de falhas de login
- Monitoramento do Event ID 4625
- Identificação de usuários envolvidos
- Identificação de IPs de origem
- Geração automática de relatório de alerta

## Tecnologias utilizadas

- Python
- PowerShell
- Windows Event Viewer
- Windows Security Logs

## Estrutura do projeto

```text
SOC-Monitoring-Lab/
├── logs/
├── reports/
│   └── alerta_bruteforce.txt
├── screenshots/
├── scripts/
│   └── detector_bruteforce.py
└── README.md