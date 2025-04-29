# utils/validadores/numero_decreto.py

import re

def validar_numero_decreto(numero: str) -> bool:
    """
    Valida se o número do decreto está no formato 000.000 (três dígitos, ponto, três dígitos)
    ou permite que esteja em branco.
    """
    if not numero.strip():
        return True
    pattern = r"^\d{3}\.\d{3}$"
    return re.match(pattern, numero.strip()) is not None

