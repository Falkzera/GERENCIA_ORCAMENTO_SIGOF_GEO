def formatar_valor(valor, casas_decimais=2):
    negativo = valor < 0  
    valor = abs(valor)  
    
    if valor >= 1_000_000_000 and valor < 1_000_000_000_000:
        valor_formatado = valor 
    elif valor >= 1_000_000 and valor < 1_000_000_000:
        valor_formatado = valor 
    elif valor >= 1_000 and valor < 1_000_000:
        valor_formatado = valor 
    else:
        valor_formatado = valor

    numero_formatado = f"{valor_formatado:.{casas_decimais}f}"
    parte_inteira, parte_decimal = numero_formatado.split(".")
    parte_inteira_formatada = ".".join([parte_inteira[max(i - 3, 0):i] for i in range(len(parte_inteira) % 3, len(parte_inteira) + 1, 3) if i])

    resultado = f"R$ {'-' if negativo else ''}{parte_inteira_formatada},{parte_decimal}".strip()

    return resultado


def formatar_valor_arredondado(valor, casas_decimais=2):
    negativo = valor < 0  
    valor = abs(valor)  
    
    if valor >= 1_000_000_000 and valor < 1_000_000_000_000:
        valor_formatado = valor / 1_000_000_000
        sufixo = "Bi"
    elif valor >= 1_000_000 and valor < 1_000_000_000:
        valor_formatado = valor / 1_000_000
        sufixo = "Mi"
    elif valor >= 1_000 and valor < 1_000_000:
        valor_formatado = valor / 1_000
        sufixo = "mil"
    else:
        valor_formatado = valor
        sufixo = ""

    numero_formatado = f"{valor_formatado:.{casas_decimais}f}"
    parte_inteira, parte_decimal = numero_formatado.split(".")
    parte_inteira_formatada = ".".join([parte_inteira[max(i - 3, 0):i] for i in range(len(parte_inteira) % 3, len(parte_inteira) + 1, 3) if i])

    resultado = f"R$ {'-' if negativo else ''}{parte_inteira_formatada},{parte_decimal} {sufixo}".strip()

    return resultado

def formatar_valor2(valor):
    return f"{valor:.2f}".replace(".", ",") + "%"


def formatar_valor_sem_cifrao(valor, casas_decimais=2):
    negativo = valor < 0  
    valor = abs(valor)  
    
    if valor >= 1_000_000_000 and valor < 1_000_000_000_000:
        valor_formatado = valor 
    elif valor >= 1_000_000 and valor < 1_000_000_000:
        valor_formatado = valor 
    elif valor >= 1_000 and valor < 1_000_000:
        valor_formatado = valor 
    else:
        valor_formatado = valor

    numero_formatado = f"{valor_formatado:.{casas_decimais}f}"
    parte_inteira, parte_decimal = numero_formatado.split(".")
    parte_inteira_formatada = ".".join([parte_inteira[max(i - 3, 0):i] for i in range(len(parte_inteira) % 3, len(parte_inteira) + 1, 3) if i])

    resultado = f"{'-' if negativo else ''}{parte_inteira_formatada},{parte_decimal}".strip()

    return resultado