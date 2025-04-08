def formatar_numero_decreto(numero: str) -> str:
    """
    Transforma o número do decreto em inteiro e o formata de acordo com as regras de validar_numero_decreto.
    """
    # Remove espaços em branco
    numero = numero.strip()
    
    # Se o número estiver vazio, retorna uma string vazia
    if not numero:
        return ""
    
    # Remove o ponto, converte para inteiro e depois formata novamente
    try:
        numero_inteiro = int(numero.replace(".", ""))
        numero_formatado = f"{numero_inteiro // 1000:03}.{numero_inteiro % 1000:03}"
        return numero_formatado
    except ValueError:
        raise ValueError("O número fornecido não está em um formato válido para conversão.")
