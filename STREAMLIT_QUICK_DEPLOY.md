# Deploy Rápido no Streamlit

Guia rápido para fazer deploy da Calculadora FIRC no Streamlit Cloud em 3 minutos!

## ⚡ 3 Passos para Deploy

### 1️⃣ Preparar Repositório GitHub

```bash
cd calculadora_FIRC

# Adicionar arquivos
git add .
git commit -m "feat: add streamlit app"
git push origin main
```

**Certifique-se que estão no repositório:**
- ✅ `app_streamlit.py`
- ✅ `requirements-streamlit.txt`
- ✅ `pdf_parser.py`
- ✅ `calculator.py`
- ✅ `data_processor.py`

### 2️⃣ Conectar no Streamlit Cloud

1. Acesse: [share.streamlit.io](https://share.streamlit.io)
2. Faça login com GitHub
3. Clique: **"New app"**
4. Preencha:
   - Repository: `seu-usuario/calculadora_FIRC`
   - Branch: `main`
   - Main file: `app_streamlit.py`
5. Click: **"Deploy"** ✨

**Pronto! Sua app estará live em ~2 minutos!**

### 3️⃣ Compartilhar Link

A URL será:
```
https://seu-usuario-calculadora-firc.streamlit.app
```

Compartilhe com anyone!

---

## 🏠 Rodar Localmente Primeiro

Antes de fazer deploy, teste localmente:

```bash
# Instalar Streamlit
pip install streamlit pdfplumber

# Rodar localmente
streamlit run app_streamlit.py
```

Acesse: http://localhost:8501

---

## ✅ Checklist de Deploy

```
☑ Repositório GitHub criado
☑ Arquivos Python no repositório
☑ requirements-streamlit.txt configurado
☑ app_streamlit.py testado localmente
☑ Conta no Streamlit Cloud criada
☑ Conectado via GitHub
☑ App deployada com sucesso
☑ URL compartilhada
```

---

## 🚀 Depois do Deploy

### Monitorar a Aplicação

- Dashboard em [share.streamlit.io](https://share.streamlit.io)
- Logs em tempo real
- Estatísticas de uso

### Atualizar o Código

Simples assim:
```bash
git push origin main
```

Streamlit Cloud faz redeployment automático! ✨

---

## 🔗 Links Úteis

- [Streamlit Cloud Dashboard](https://share.streamlit.io)
- [Documentação Streamlit](https://docs.streamlit.io)
- [GitHub Integration](https://docs.streamlit.io/deploy/streamlit-cloud)

---

## 💡 Dicas

1. **Grátis para sempre** - Streamlit Cloud não cobra nada
2. **Deploy automático** - Cada push faz deploy novo
3. **HTTPS automático** - Seguro por padrão
4. **Sem Docker** - Nenhuma configuração necessária
5. **Mobile-friendly** - Funciona perfeito em phone

---

## 🎉 Parabéns!

Sua aplicação está no ar! 

Acesse: `https://seu-usuario-calculadora-firc.streamlit.app`

**Próximas ideias:**
- Adicionar autenticação
- Histórico de uploads
- Dashboard de estatísticas
- Exportar relatórios
- Integrar com banco de dados

---

**Precisa de ajuda?** Veja [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md) para guias mais completos.
