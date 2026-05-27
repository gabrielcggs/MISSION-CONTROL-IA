# Mission Control AI — MobilitySat Starter Kit

## Integrantes
- Nome Completo — RM: XXXXXX — Turma: XCCXX
- Nome Completo — RM: XXXXXX — Turma: XCCXX

## O que o projeto faz
Este projeto simula uma missão GNSS (MobilitySat), monitora telemetria crítica e gera alertas automáticos em Python. Em seguida, envia os dados para um LLM via Ollama Cloud para produzir diagnóstico técnico com impacto terrestre em mobilidade e logística.

## Persona atendida
Engenheiro de operações de segmento espacial e gestor de frota logística que depende de posicionamento de alta disponibilidade.

## Tecnologias utilizadas
- Python 3.10+
- Ollama Cloud API (`gpt-oss:120b`)
- `ollama`, `python-dotenv`, `rich`, `prompt-toolkit`, `pyfiglet`

## Como executar
1. Abra a pasta do projeto.
2. Crie e ative ambiente virtual:
   - Windows PowerShell: `python -m venv .venv` e `.venv\Scripts\Activate.ps1`
3. Instale dependências: `pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e preencha:
   - `OLLAMA_API_KEY=sua_chave_aqui`
5. Execute: `python main.py`

## Comandos da CLI
- `/help` — lista comandos
- `/status` — mostra snapshot + alertas atuais
- `/about` — contexto da trilha
- `/clear` — limpa terminal
- `/exit` — encerra

## Cenários de teste sugeridos
1. Operação nominal — sem alertas.
2. Drift alto do oscilador + baixa integridade L1/L5.
3. Margem de potência crítica com impacto em continuidade de serviço.

## Limitações conhecidas
- Telemetria ainda é sintética (aleatória), sem histórico temporal persistente.
- Alertas usam thresholds fixos e não aprendizado adaptativo.

## Vídeo de demonstração
🔗 [Assistir demonstração no YouTube](https://www.youtube.com/watch?v=SEU_ID_AQUI)
