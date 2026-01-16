"""
Módulo de cálculo para somar valores extraídos do PDF.
Realiza somas independentes com validação silenciosa.
"""
from typing import List, Dict
from data_processor import clean_monetary_value, validate_decimal


class FinancialCalculator:
    """Calculadora para totalizar valores financeiros extraídos de PDFs."""
    
    def __init__(self):
        """Inicializa a calculadora."""
        self.total_valor_pago: float = 0.0
        self.total_cartorio: float = 0.0
    
    def calculate_totals(self, extracted_data: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Calcula os totais de Valor Pago e Cartório.
        
        Args:
            extracted_data: Dicionário com listas de valores extraídos
                {
                    "cartorio": [...],
                    "valor_pago": [...]
                }
        
        Returns:
            Dict com os totais calculados:
            {
                "total_valor_pago": float,
                "total_cartorio": float
            }
        """
        # Calcula total de Valor Pago
        self.total_valor_pago = self._sum_values(
            extracted_data.get("valor_pago", [])
        )
        
        # Calcula total de Cartório
        self.total_cartorio = self._sum_values(
            extracted_data.get("cartorio", [])
        )
        
        # Validação silenciosa
        self._validate_totals()
        
        return {
            "total_valor_pago": self.total_valor_pago,
            "total_cartorio": self.total_cartorio
        }
    
    def _sum_values(self, values: List[str]) -> float:
        """
        Soma uma lista de valores monetários (strings).
        
        Args:
            values: Lista de valores como strings
            
        Returns:
            float: Soma total
        """
        total = 0.0
        
        for value in values:
            cleaned_value = clean_monetary_value(value)
            if validate_decimal(cleaned_value):
                total += cleaned_value
        
        # Arredonda para 2 casas decimais (precisão monetária)
        return round(total, 2)
    
    def _validate_totals(self) -> None:
        """
        Validação silenciosa dos totais calculados.
        Garante que os valores são números válidos.
        """
        # Valida total_valor_pago
        if not validate_decimal(self.total_valor_pago):
            self.total_valor_pago = 0.0
        
        # Valida total_cartorio
        if not validate_decimal(self.total_cartorio):
            self.total_cartorio = 0.0
        
        # Garante que não são negativos
        self.total_valor_pago = max(0.0, self.total_valor_pago)
        self.total_cartorio = max(0.0, self.total_cartorio)
