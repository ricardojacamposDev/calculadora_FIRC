"""
Módulo para extração de dados de PDFs financeiros.
Identifica e extrai valores da coluna Cartório (8ª coluna) e campo Valor Pago.
"""
import pdfplumber
from typing import List, Dict, Any, Optional
import re


class PDFFinancialParser:
    """Parser especializado para documentos PDF financeiros (Guias Geradas)."""
    
    def __init__(self, pdf_path: str):
        """
        Inicializa o parser com o caminho do PDF.
        
        Args:
            pdf_path: Caminho completo para o arquivo PDF
        """
        self.pdf_path = pdf_path
        self.cartorio_values: List[str] = []
        self.valor_pago_values: List[str] = []
    
    def extract_data(self) -> Dict[str, List[str]]:
        """
        Extrai dados de todas as páginas do PDF.
        
        Returns:
            Dict com listas de valores extraídos:
            {
                "cartorio": [...],
                "valor_pago": [...]
            }
        """
        self.cartorio_values = []
        self.valor_pago_values = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    self._extract_from_page(page, page_num)
        except Exception as e:
            # Em caso de erro, retorna listas vazias (soma será 0.0)
            print(f"Erro ao processar PDF: {e}", file=__import__('sys').stderr)
        
        return {
            "cartorio": self.cartorio_values,
            "valor_pago": self.valor_pago_values
        }
    
    def _extract_from_page(self, page: Any, page_num: int) -> None:
        """
        Extrai dados de uma página específica do PDF.
        
        Args:
            page: Objeto página do pdfplumber
            page_num: Número da página
        """
        # Extrai tabelas da página
        tables = page.extract_tables()
        
        if tables:
            for table in tables:
                self._extract_from_table(table)
        
        # Extrai texto para buscar dados em formato não-tabular
        text = page.extract_text()
        if text:
            self._extract_from_text(text)
    
    def _extract_from_table(self, table: List[List[str]]) -> None:
        """
        Extrai valores da 8ª coluna (Cartório) de uma tabela.
        
        Args:
            table: Tabela extraída (lista de listas)
        """
        if not table:
            return
        
        # Processa cada linha da tabela
        for row_idx, row in enumerate(table):
            if not row:
                continue
            
            # Extrai 8ª coluna (índice 7) se existir
            if len(row) >= 8:
                cartorio_value = row[7]
                if cartorio_value:
                    # Verifica se parece um valor monetário
                    if self._is_monetary_value(cartorio_value):
                        self.cartorio_values.append(cartorio_value)
    
    def _extract_valor_pago_from_text(self, text: str) -> None:
        """
        Busca e extrai valores do campo "Valor Pago" no texto.
        
        Args:
            text: Texto extraído da página
        """
        # Padrões para identificar "Valor Pago"
        patterns = [
            r'Valor\s+Pago[:\s]+([R$\s]*[\d.,]+)',
            r'VALOR\s+PAGO[:\s]+([R$\s]*[\d.,]+)',
            r'Valor Pago[:\s]+([R$\s]*[\d.,]+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                valor = match.group(1).strip()
                if self._is_monetary_value(valor):
                    self.valor_pago_values.append(valor)
    
    def _extract_from_text(self, text: str) -> None:
        """
        Extrai dados de texto formatado (sem tabela estruturada).
        Processa linhas de dados procurando valores de Cartório e Valor Pago.
        
        Args:
            text: Texto completo da página
        """
        lines = text.split('\n')
        
        for line in lines:
            # Ignora linhas de cabeçalho
            if 'Guias Geradas' in line or 'Rateios' in line or 'Guia Cartório Cidade' in line:
                continue
            
            # Procura por linhas de dados com valores monetários
            # Formato esperado: código, texto, valores...
            # Exemplo: "0024102419 Serventia... Geral R$ 301,61 R$ 301,61 R$ 0,00 R$ 215,44..."
            
            # Extrai todos os valores monetários da linha
            valores = re.findall(r'R\$\s*([\d.,]+)', line)
            
            if valores and len(valores) >= 4:
                # Posições esperadas:
                # 0: Valor da Guia
                # 1: Valor Pago
                # 2: Tarifa
                # 3: Cartório (8ª coluna quando contamos do início)
                
                # Valor Pago é a 2ª ocorrência de valor (índice 1)
                if len(valores) > 1:
                    valor_pago = valores[1]
                    if self._is_monetary_value(valor_pago):
                        self.valor_pago_values.append(valor_pago)
                
                # Cartório é a 4ª ocorrência de valor (índice 3)
                # Isso corresponde à coluna "Cartório" nos rateios
                if len(valores) > 3:
                    cartorio = valores[3]
                    if self._is_monetary_value(cartorio):
                        self.cartorio_values.append(cartorio)
    
    def _is_monetary_value(self, value: str) -> bool:
        """
        Verifica se uma string parece um valor monetário.
        
        Args:
            value: String a verificar
            
        Returns:
            bool: True se parece valor monetário
        """
        if not value or not isinstance(value, str):
            return False
        
        # Remove espaços e símbolos de moeda
        cleaned = value.strip().replace('R$', '').replace('$', '').strip()
        
        # Verifica se contém números e separadores válidos
        return bool(re.match(r'^[\d.,]+$', cleaned))
