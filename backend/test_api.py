"""
Teste rápido da API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """Testa os endpoints da API"""
    
    print("=" * 60)
    print("TESTE DA API CALCULADORA FIRC")
    print("=" * 60)
    
    # Teste 1: Health check
    print("\n1️⃣  Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Info da API
    print("\n2️⃣  Obtendo informações da API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Upload de PDF
    print("\n3️⃣  Testando upload de PDF...")
    pdf_path = "consultarGuiasGeradas_Report.pdf"
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{BASE_URL}/api/process-pdf",
                files=files
            )
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {json.dumps(response.json(), indent=2)}")
    except FileNotFoundError:
        print(f"   ❌ Arquivo {pdf_path} não encontrado")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⏳ Certifique-se de que o backend está rodando em http://localhost:8000")
    input("\nPressione Enter para continuar...")
    test_api()
