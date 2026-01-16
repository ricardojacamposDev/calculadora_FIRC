"""
Módulo para processar dados monetários extraídos de PDFs.
Converte strings monetárias em valores decimais.
"""
import re
from typing import Union


def clean_monetary_value(value: Union[str, float, int, None]) -> float:
    """
    Converte um valor monetário (string ou numérico) em float decimal.
    
    Remove símbolos de moeda (R$), separadores de milhar, e converte
    vírgula decimal em ponto. Valores ausentes, vazios ou ilegíveis
    retornam 0.0.
    
    Args:
        value: Valor monetário como string, número ou None
        
    Returns:
        float: Valor decimal limpo
        
    Examples:
        >>> clean_monetary_value("R$ 1.234,56")
        1234.56
        >>> clean_monetary_value("234,50")
        234.5
        >>> clean_monetary_value(None)
        0.0
        >>> clean_monetary_value("")
        0.0
    """
    # Valores ausentes, None ou vazios retornam 0.0
    if value is None or value == "":
        return 0.0
    
    # Se já é número, retorna como float
    if isinstance(value, (int, float)):
        return float(value)
    
    # Converte para string e processa
    value_str = str(value).strip()
    
    # String vazia após strip retorna 0.0
    if not value_str:
        return 0.0
    
    try:
        # Remove símbolo de moeda (R$, US$, etc)
        value_str = re.sub(r'[R$US$€£¥]+', '', value_str)
        
        # Remove espaços
        value_str = value_str.strip()
        
        # Remove separadores de milhar (pontos)
        # Identifica padrão brasileiro: 1.234,56
        if ',' in value_str and '.' in value_str:
            # Formato brasileiro: remove pontos, troca vírgula por ponto
            value_str = value_str.replace('.', '')
            value_str = value_str.replace(',', '.')
        elif ',' in value_str:
            # Apenas vírgula: assume decimal brasileiro
            value_str = value_str.replace(',', '.')
        # Se apenas ponto, assume já está no formato correto
        
        # Converte para float
        return float(value_str)
        
    except (ValueError, AttributeError):
        # Em caso de erro na conversão, retorna 0.0 conforme especificação
        return 0.0


def validate_decimal(value: float) -> bool:
    """
    Valida se um valor é um número decimal válido.
    
    Args:
        value: Valor a validar
        
    Returns:
        bool: True se válido, False caso contrário
    """
    return isinstance(value, (int, float)) and not (value != value)  # Check for NaN
