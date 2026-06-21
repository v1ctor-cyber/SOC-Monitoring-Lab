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
```

## Evidências

### 1. Eventos 4625 detectados

![Eventos 4625](screenshots/01_event_overview.png)

### 2. Investigação detalhada do evento

![Detalhes do Evento](screenshots/02_event_details.png)

### 3. Execução do detector

![Detector](screenshots/03_detector_execution.png)

### 4. Relatório gerado automaticamente

![Relatório](screenshots/04_alert_report.png)

## Resultados

Durante os testes foram geradas múltiplas tentativas de autenticação inválidas para produzir eventos 4625 no Windows Security Log.

O detector identificou:

* 7 falhas de login
* Origem: 127.0.0.1
* Tipo de logon: 2 (logon local)

Após a análise dos eventos, foi gerado automaticamente um relatório contendo os indicadores observados.

