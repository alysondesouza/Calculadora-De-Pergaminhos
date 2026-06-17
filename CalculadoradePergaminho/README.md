# Calculadora de Pergaminhos

Aplicação Streamlit para calcular o custo total de pergaminhos, segredo, soro e ryos.

## Como executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no GitHub / Streamlit Cloud

1. Crie um repositório no GitHub.
2. Envie este projeto para o repositório.
3. No Streamlit Cloud, escolha "Deploy an app" e conecte o repositório.
4. Defina o arquivo principal como `app.py`.
5. O app usará `requirements.txt` automaticamente.

Se quiser publicar em outras plataformas, o arquivo `Procfile` já está preparado para o comando:

```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```
