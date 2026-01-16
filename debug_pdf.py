"""
Script de debug para visualizar o conteúdo extraído do PDF.
"""
import pdfplumber
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "consultarGuiasGeradas_Report.pdf"

print(f"Analisando PDF: {pdf_path}\n")
print("=" * 80)

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total de páginas: {len(pdf.pages)}\n")
    
    for page_num, page in enumerate(pdf.pages, start=1):
        print(f"\n{'='*80}")
        print(f"PÁGINA {page_num}")
        print('='*80)
        
        # Extrai texto
        text = page.extract_text()
        print(f"\n--- TEXTO DA PÁGINA ---")
        print(text[:1000] if text else "Nenhum texto extraído")
        
        # Extrai tabelas
        tables = page.extract_tables()
        print(f"\n--- TABELAS ENCONTRADAS: {len(tables) if tables else 0} ---")
        
        if tables:
            for table_idx, table in enumerate(tables):
                print(f"\nTabela {table_idx + 1}:")
                print(f"  Linhas: {len(table)}")
                print(f"  Colunas: {len(table[0]) if table else 0}")
                
                # Mostra header se existir
                if table:
                    print(f"\n  Cabeçalho (primeira linha):")
                    print(f"  {table[0]}")
                    
                    # Mostra algumas linhas de dados
                    print(f"\n  Primeiras linhas de dados:")
                    for row_idx, row in enumerate(table[1:4], start=2):
                        print(f"  Linha {row_idx}: {row}")
