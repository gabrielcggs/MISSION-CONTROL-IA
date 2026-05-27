"""Geração de telemetria simulada para a trilha MobilitySat."""

from random import uniform


def coletar() -> dict:
    """Retorna snapshot da missão com parâmetros de navegação GNSS."""
    return {
        "drift_oscilador_ns": round(uniform(0.5, 9.0), 2),
        "sincronizacao_constelacao_pct": round(uniform(82.0, 100.0), 2),
        "integridade_sinal_l1_l5_pct": round(uniform(80.0, 100.0), 2),
        "precisao_efemeride_m": round(uniform(0.4, 4.2), 2),
        "margem_potencia_pct": round(uniform(15.0, 95.0), 2),
    }
