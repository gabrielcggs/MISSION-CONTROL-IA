"""Regras de alerta e respostas automáticas da missão MobilitySat."""


def avaliar(dados: dict) -> list[dict]:
    alertas = []

    if dados["drift_oscilador_ns"] > 6.5:
        alertas.append(
            {
                "severidade": "alta",
                "evento": "Drift elevado do oscilador atômico",
                "acao_automatica": "Aplicar correção de clock e recalibrar sincronismo.",
            }
        )

    if dados["sincronizacao_constelacao_pct"] < 90:
        alertas.append(
            {
                "severidade": "media",
                "evento": "Sincronização abaixo do nível nominal",
                "acao_automatica": "Priorizar enlace com satélites de referência da constelação.",
            }
        )

    if dados["integridade_sinal_l1_l5_pct"] < 88:
        alertas.append(
            {
                "severidade": "alta",
                "evento": "Queda de integridade dos sinais L1/L5",
                "acao_automatica": "Acionar redundância de transmissão e ampliar checagem de erro.",
            }
        )

    if dados["precisao_efemeride_m"] > 3.0:
        alertas.append(
            {
                "severidade": "media",
                "evento": "Precisão de efeméride degradada",
                "acao_automatica": "Executar atualização orbital e revalidar parâmetros de navegação.",
            }
        )

    if dados["margem_potencia_pct"] < 25:
        alertas.append(
            {
                "severidade": "alta",
                "evento": "Margem de potência crítica",
                "acao_automatica": "Entrar em modo economia e priorizar subsistemas essenciais.",
            }
        )

    return alertas
