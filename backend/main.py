"""
Calculadora FIRC - Financial Invoice Receipt Calculator

Script principal para processar PDFs financeiros e calcular totais.
Saída em formato JSON puro.
"""
import sys
import json
from pathlib import Path
from pdf_parser import PDFFinancialParser
from calculator import FinancialCalculator


def process_pdf(pdf_path: str) -> dict:
    """
    Processa um PDF financeiro e retorna os totais calculados.
    
    Args:
        pdf_path: Caminho para o arquivo PDF
        
    Returns:
        Dict com totais no formato:
        {
            "total_valor_pago": float,
            "total_cartorio": float
        }
    """
    # Verifica se o arquivo existe
    if not Path(pdf_path).exists():
        return {
            "total_valor_pago": 0.0,
            "total_cartorio": 0.0
        }
    
    # Extrai dados do PDF
    parser = PDFFinancialParser(pdf_path)
    extracted_data = parser.extract_data()
    
    # Calcula totais
    calculator = FinancialCalculator()
    totals = calculator.calculate_totals(extracted_data)
    
    return totals


def main():
    """Função principal - interface de linha de comando."""
    # Verifica argumentos
    if len(sys.argv) < 2:
        # Sem argumentos, retorna JSON vazio
        result = {
            "total_valor_pago": 0.0,
            "total_cartorio": 0.0
        }
    else:
        pdf_path = sys.argv[1]
        result = process_pdf(pdf_path)
    
    # Saída ESTRITA em JSON - sem texto adicional
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
