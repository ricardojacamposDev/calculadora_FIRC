"""
API REST para a Calculadora FIRC
FastAPI backend para processar PDFs financeiros
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import tempfile
import os
from typing import Dict
import logging

from pdf_parser import PDFFinancialParser
from calculator import FinancialCalculator

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="Calculadora FIRC API",
    description="API REST para processar PDFs financeiros e calcular totais",
    version="1.0.0"
)

# Configuração CORS para permitir requisições do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint raiz - informações da API."""
    return {
        "name": "Calculadora FIRC API",
        "version": "1.0.0",
        "description": "API para processar PDFs financeiros (Guias Geradas)",
        "endpoints": {
            "POST /api/process-pdf": "Processa PDF e retorna totais calculados",
            "GET /api/health": "Verifica status da API"
        }
    }


@app.get("/api/health")
async def health_check():
    """Verifica o status da API."""
    return {
        "status": "healthy",
        "service": "Calculadora FIRC API"
    }


@app.post("/api/process-pdf")
async def process_pdf(file: UploadFile = File(...)) -> JSONResponse:
    """
    Processa um PDF financeiro e retorna os totais calculados.
    
    Args:
        file: Arquivo PDF enviado via multipart/form-data
        
    Returns:
        JSONResponse com:
        {
            "success": true,
            "data": {
                "total_valor_pago": float,
                "total_cartorio": float,
                "filename": string,
                "total_values_found": int
            }
        }
        
    Raises:
        HTTPException: Se houver erro no processamento
    """
    # Validação do arquivo
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Formato inválido. Apenas arquivos PDF são aceitos."
        )
    
    # Cria arquivo temporário para processar o PDF
    temp_file = None
    try:
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        logger.info(f"Processando PDF: {file.filename}")
        
        # Processa o PDF usando a lógica existente
        parser = PDFFinancialParser(temp_file_path)
        extracted_data = parser.extract_data()
        
        # Calcula os totais
        calculator = FinancialCalculator()
        result = calculator.calculate_totals(extracted_data)
        
        # Conta total de valores encontrados
        total_values_found = (
            len(extracted_data.get("valor_pago", [])) + 
            len(extracted_data.get("cartorio", []))
        )
        
        logger.info(
            f"PDF processado com sucesso: {file.filename} "
            f"(Valor Pago: R$ {result['total_valor_pago']:.2f}, "
            f"Cartório: R$ {result['total_cartorio']:.2f})"
        )
        
        # Retorna resultado
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "total_valor_pago": result["total_valor_pago"],
                    "total_cartorio": result["total_cartorio"],
                    "filename": file.filename,
                    "total_values_found": total_values_found,
                    "details": {
                        "valores_pago_count": len(extracted_data.get("valor_pago", [])),
                        "cartorio_count": len(extracted_data.get("cartorio", []))
                    }
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao processar PDF {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar PDF: {str(e)}"
        )
        
    finally:
        # Remove arquivo temporário
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Erro ao remover arquivo temporário: {e}")


@app.post("/api/process-pdf/simple")
async def process_pdf_simple(file: UploadFile = File(...)) -> Dict:
    """
    Versão simplificada que retorna apenas os totais (compatível com CLI).
    
    Returns:
        {
            "total_valor_pago": float,
            "total_cartorio": float
        }
    """
    response = await process_pdf(file)
    data = response.body.decode()
    
    import json
    result = json.loads(data)
    
    if result.get("success"):
        return {
            "total_valor_pago": result["data"]["total_valor_pago"],
            "total_cartorio": result["data"]["total_cartorio"]
        }
    else:
        raise HTTPException(status_code=500, detail="Erro ao processar PDF")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
