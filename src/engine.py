"""Motor de análise da Mission Control AI."""

import os
import json
from pathlib import Path

from dotenv import load_dotenv
from ollama import Client

from src.alertas import avaliar
from src.telemetria import coletar

load_dotenv()

TRILHA = "mobilitysat"

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")},
)


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )["message"]["content"].strip()
    except Exception as e:
        return f"⚠ Erro ao consultar IA: {e}"


def load_system_prompt():
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de missão espacial."


class MissionEngine:
    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.ultimo_snapshot = None
        self.ultimos_alertas = []
        self.scenario_mode = "random"
        self.scenario_data = self._load_scenarios()

    def _load_scenarios(self):
        path = Path("data/cenarios.json")
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def list_scenarios(self):
        if not self.scenario_data:
            return []
        return sorted(self.scenario_data.keys())

    def set_scenario_mode(self, scenario_name):
        if scenario_name == "random":
            self.scenario_mode = "random"
            return True
        if scenario_name in self.scenario_data:
            self.scenario_mode = scenario_name
            return True
        return False

    def is_ready(self):
        return True

    def _coletar_estado(self):
        if self.scenario_mode == "random":
            self.ultimo_snapshot = coletar()
        else:
            self.ultimo_snapshot = dict(self.scenario_data[self.scenario_mode])
        self.ultimos_alertas = avaliar(self.ultimo_snapshot)
        return self.ultimo_snapshot, self.ultimos_alertas

    def status_snapshot(self):
        dados, alertas = self._coletar_estado()
        linhas = [
            "📡 MobilitySat — Snapshot atual",
            f"- Drift oscilador: {dados['drift_oscilador_ns']} ns",
            f"- Sincronização: {dados['sincronizacao_constelacao_pct']}%",
            f"- Integridade L1/L5: {dados['integridade_sinal_l1_l5_pct']}%",
            f"- Precisão efeméride: {dados['precisao_efemeride_m']} m",
            f"- Margem de potência: {dados['margem_potencia_pct']}%",
        ]
        if alertas:
            linhas.append(f"\n⚠ Alertas ativos: {len(alertas)}")
            for a in alertas:
                linhas.append(f"- [{a['severidade'].upper()}] {a['evento']}")
        else:
            linhas.append("\n✅ Operação nominal, sem alertas.")
        return "\n".join(linhas)

    def analyze(self, pergunta_usuario):
        dados, alertas = self._coletar_estado()

        bloco_alertas = "Sem alertas no momento."
        if alertas:
            linhas = []
            for a in alertas:
                linhas.append(
                    f"- Severidade: {a['severidade']} | Evento: {a['evento']} | Ação: {a['acao_automatica']}"
                )
            bloco_alertas = "\n".join(linhas)

        prompt = f"""
Trilha: MobilitySat (GNSS e Mobilidade)

Telemetria atual:
- Drift do oscilador atômico (ns): {dados['drift_oscilador_ns']}
- Sincronização com constelação (%): {dados['sincronizacao_constelacao_pct']}
- Integridade do sinal L1/L5 (%): {dados['integridade_sinal_l1_l5_pct']}
- Precisão da efeméride (m): {dados['precisao_efemeride_m']}
- Margem de potência (%): {dados['margem_potencia_pct']}

Alertas e respostas automáticas:
{bloco_alertas}

Pergunta do operador:
{pergunta_usuario}
"""
        return llm(prompt=prompt, system=self.system_prompt)
