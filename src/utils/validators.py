import re
from datetime import datetime

def validar_cpf(cpf):
    """Valida um CPF usando o algoritmo oficial"""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if int(cpf[9]) != digito1:
        return False
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if int(cpf[10]) != digito2:
        return False
    
    return True

def validar_data(data_str):
    """Valida uma data de agendamento"""
    try:
        data = datetime.strptime(data_str, '%d/%m/%Y')
        hoje = datetime.now()
        
        # Verifica se a data é futura
        if data.date() < hoje.date():
            return False
        
        # Verifica se é dia útil (segunda a sábado)
        if data.weekday() > 5:  # 5 = sábado, 6 = domingo
            return False
        
        return True
    except:
        return False 