"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""

from datetime import datetime

import pyfiglet
from prompt_toolkit import PromptSession
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def _build_session():
    """Cria sessão avançada quando houver console compatível."""
    try:
        return PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))
    except (NoConsoleScreenBufferError, OSError):
        return None


def show_banner():
    banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    console.print(Text(banner, style="bold #06B6D4"))
    console.print(
        Panel.fit(
            "Sistema de monitoramento e análise por IA generativa.\n"
            "Trilha ativa: MobilitySat (GNSS e Mobilidade).\n"
            "Use /help para ver os comandos · /exit para sair.\n"
            "Modelo: gpt-oss:120b via Ollama Cloud",
            title="◆ MISSION CONTROL",
            border_style="#06B6D4",
        )
    )


def show_response(text):
    now = datetime.now().strftime("%H:%M")
    console.print(
        Panel(
            text,
            title="◆ Mission Control",
            subtitle=now,
            border_style="#06B6D4",
        )
    )


def run_cli(engine):
    session = _build_session()
    show_banner()
    if session is None:
        console.print(
            "ℹ Ambiente sem console Win32 detectado: usando input básico.",
            style="yellow",
        )
    if not engine.is_ready():
        console.print("⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="yellow")
    while True:
        try:
            if session is not None:
                user_input = session.prompt("❯ ").strip()
            else:
                user_input = input("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not user_input:
            continue

        normalized = user_input.lower()
        command_aliases = {
            "sair": "/exit",
            "exit": "/exit",
            "ajuda": "/help",
            "help": "/help",
            "status": "/status",
            "sobre": "/about",
            "about": "/about",
            "limpar": "/clear",
            "clear": "/clear",
            "cenario normal": "/cenario normal",
            "cenario critico": "/cenario critico_sinal",
            "cenario random": "/cenario random",
        }
        user_input = command_aliases.get(normalized, user_input)

        if user_input == "/exit":
            break
        if user_input == "/help":
            console.print(
                "Comandos: /help /status /about /clear /exit\n"
                "Cenarios para print: /cenario normal | /cenario critico_sinal | /cenario random"
            )
            continue
        if user_input == "/about":
            show_response(
                "MobilitySat monitora sinais GNSS para reduzir riscos operacionais\n"
                "em logística e mobilidade de precisão."
            )
            continue
        if user_input == "/status":
            snapshot = engine.status_snapshot()
            snapshot = f"Modo de cenário: {engine.scenario_mode}\n\n{snapshot}"
            show_response(snapshot)
            continue
        if user_input.startswith("/cenario"):
            partes = user_input.split(maxsplit=1)
            if len(partes) == 1:
                disponiveis = ", ".join(engine.list_scenarios()) or "nenhum"
                show_response(
                    f"Cenário atual: {engine.scenario_mode}\n"
                    f"Disponíveis: {disponiveis}\n"
                    "Use /cenario <nome> ou /cenario random."
                )
                continue

            scenario_name = partes[1].strip().lower()
            if engine.set_scenario_mode(scenario_name):
                show_response(
                    f"Cenário alterado para: {engine.scenario_mode}\n"
                    "Dica: rode /status e tire o print."
                )
            else:
                disponiveis = ", ".join(engine.list_scenarios()) or "nenhum"
                show_response(
                    f"Cenário inválido: {scenario_name}\n"
                    f"Disponíveis: {disponiveis} + random"
                )
            continue
        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        resposta = engine.analyze(user_input)
        show_response(resposta)
