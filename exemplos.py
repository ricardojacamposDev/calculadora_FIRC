"""
Exemplos de uso da Calculadora FIRC
"""
from pdf_parser import PDFFinancialParser
from calculator import FinancialCalculator
import json


def exemplo_basico():
    """Exemplo básico de uso."""
    print("=" * 80)
    print("EXEMPLO 1: Processamento básico de PDF")
    print("=" * 80)
    
    pdf_path = "consultarGuiasGeradas_Report.pdf"
    
    # Passo 1: Extrair dados do PDF
    print(f"\n1. Extraindo dados de: {pdf_path}")
    parser = PDFFinancialParser(pdf_path)
    dados = parser.extract_data()
    
    print(f"   - Valores Pago encontrados: {len(dados['valor_pago'])}")
    print(f"   - Valores Cartório encontrados: {len(dados['cartorio'])}")
    
    # Passo 2: Calcular totais
    print("\n2. Calculando totais...")
    calculadora = FinancialCalculator()
    resultado = calculadora.calculate_totals(dados)
    
    # Passo 3: Exibir resultado
    print("\n3. Resultado:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    

def exemplo_detalhado():
    """Exemplo com detalhamento dos valores."""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Processamento detalhado")
    print("=" * 80)
    
    pdf_path = "consultarGuiasGeradas_Report.pdf"
    
    parser = PDFFinancialParser(pdf_path)
    dados = parser.extract_data()
    
    print("\nValores de Valor Pago extraídos:")
    for i, valor in enumerate(dados['valor_pago'][:5], 1):  # Mostra os 5 primeiros
        print(f"  {i}. {valor}")
    if len(dados['valor_pago']) > 5:
        print(f"  ... e mais {len(dados['valor_pago']) - 5} valores")
    
    print("\nValores de Cartório extraídos:")
    for i, valor in enumerate(dados['cartorio'][:5], 1):  # Mostra os 5 primeiros
        print(f"  {i}. {valor}")
    if len(dados['cartorio']) > 5:
        print(f"  ... e mais {len(dados['cartorio']) - 5} valores")
    
    calculadora = FinancialCalculator()
    resultado = calculadora.calculate_totals(dados)
    
    print(f"\n{'─' * 40}")
    print(f"Total Valor Pago:  R$ {resultado['total_valor_pago']:,.2f}")
    print(f"Total Cartório:    R$ {resultado['total_cartorio']:,.2f}")
    print(f"{'─' * 40}")


def exemplo_validacao():
    """Exemplo mostrando validação de dados."""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Validação de dados")
    print("=" * 80)
    
    from data_processor import clean_monetary_value
    
    exemplos = [
        "R$ 1.234,56",
        "234,50",
        None,
        "",
        "abc",
        "R$ 10.000,00"
    ]
    
    print("\nTestando processamento de valores monetários:")
    print(f"{'Entrada':<20} -> {'Saída':<15}")
    print("─" * 40)
    
    for exemplo in exemplos:
        resultado = clean_monetary_value(exemplo)
        entrada_str = repr(exemplo) if exemplo is not None else "None"
        print(f"{entrada_str:<20} -> R$ {resultado:>10.2f}")


if __name__ == "__main__":
    # Executa todos os exemplos
    exemplo_basico()
    exemplo_detalhado()
    exemplo_validacao()
    
    print("\n" + "=" * 80)
    print("Para usar via linha de comando:")
    print("  python main.py consultarGuiasGeradas_Report.pdf")
    print("=" * 80)
