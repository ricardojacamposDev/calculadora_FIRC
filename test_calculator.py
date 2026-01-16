"""
Testes unitários para os módulos da Calculadora FIRC.
"""
import unittest
from data_processor import clean_monetary_value, validate_decimal
from calculator import FinancialCalculator


class TestDataProcessor(unittest.TestCase):
    """Testes para o processador de dados monetários."""
    
    def test_clean_monetary_value_with_rs_symbol(self):
        """Testa remoção do símbolo R$."""
        self.assertEqual(clean_monetary_value("R$ 1.234,56"), 1234.56)
        self.assertEqual(clean_monetary_value("R$234,50"), 234.50)
    
    def test_clean_monetary_value_without_symbol(self):
        """Testa valores sem símbolo de moeda."""
        self.assertEqual(clean_monetary_value("1.234,56"), 1234.56)
        self.assertEqual(clean_monetary_value("234,50"), 234.50)
    
    def test_clean_monetary_value_only_comma(self):
        """Testa valores com apenas vírgula decimal."""
        self.assertEqual(clean_monetary_value("234,50"), 234.50)
        self.assertEqual(clean_monetary_value("10,00"), 10.00)
    
    def test_clean_monetary_value_only_dot(self):
        """Testa valores com apenas ponto (formato US)."""
        self.assertEqual(clean_monetary_value("234.50"), 234.50)
        self.assertEqual(clean_monetary_value("1234.56"), 1234.56)
    
    def test_clean_monetary_value_none_and_empty(self):
        """Testa valores None e vazios retornam 0.0."""
        self.assertEqual(clean_monetary_value(None), 0.0)
        self.assertEqual(clean_monetary_value(""), 0.0)
        self.assertEqual(clean_monetary_value("   "), 0.0)
    
    def test_clean_monetary_value_numeric(self):
        """Testa valores já numéricos."""
        self.assertEqual(clean_monetary_value(1234.56), 1234.56)
        self.assertEqual(clean_monetary_value(100), 100.0)
    
    def test_clean_monetary_value_invalid(self):
        """Testa valores inválidos retornam 0.0."""
        self.assertEqual(clean_monetary_value("abc"), 0.0)
        self.assertEqual(clean_monetary_value("R$ xyz"), 0.0)
    
    def test_validate_decimal(self):
        """Testa validação de decimais."""
        self.assertTrue(validate_decimal(123.45))
        self.assertTrue(validate_decimal(0))
        self.assertTrue(validate_decimal(0.0))
        self.assertFalse(validate_decimal("123"))


class TestFinancialCalculator(unittest.TestCase):
    """Testes para a calculadora financeira."""
    
    def test_calculate_totals_with_valid_data(self):
        """Testa cálculo com dados válidos."""
        calculator = FinancialCalculator()
        data = {
            "valor_pago": ["301,61", "985,92", "9.151,22"],
            "cartorio": ["215,44", "713,27", "6.605,64"]
        }
        
        result = calculator.calculate_totals(data)
        
        self.assertAlmostEqual(result["total_valor_pago"], 10438.75, places=2)
        self.assertAlmostEqual(result["total_cartorio"], 7534.35, places=2)
    
    def test_calculate_totals_with_empty_data(self):
        """Testa cálculo com dados vazios."""
        calculator = FinancialCalculator()
        data = {
            "valor_pago": [],
            "cartorio": []
        }
        
        result = calculator.calculate_totals(data)
        
        self.assertEqual(result["total_valor_pago"], 0.0)
        self.assertEqual(result["total_cartorio"], 0.0)
    
    def test_calculate_totals_with_mixed_data(self):
        """Testa cálculo com dados mistos (válidos e inválidos)."""
        calculator = FinancialCalculator()
        data = {
            "valor_pago": ["301,61", None, "985,92", "", "100,00"],
            "cartorio": ["215,44", "abc", "713,27"]
        }
        
        result = calculator.calculate_totals(data)
        
        self.assertAlmostEqual(result["total_valor_pago"], 1387.53, places=2)
        self.assertAlmostEqual(result["total_cartorio"], 928.71, places=2)
    
    def test_calculate_totals_ensures_non_negative(self):
        """Testa que totais não podem ser negativos."""
        calculator = FinancialCalculator()
        # Força valores negativos internamente
        calculator.total_valor_pago = -100.0
        calculator.total_cartorio = -50.0
        
        calculator._validate_totals()
        
        self.assertEqual(calculator.total_valor_pago, 0.0)
        self.assertEqual(calculator.total_cartorio, 0.0)


if __name__ == "__main__":
    unittest.main()
