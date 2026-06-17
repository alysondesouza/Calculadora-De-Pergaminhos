# Publicando no GitHub

1. Abra o GitHub e crie um novo repositório.
2. No terminal, dentro da pasta do projeto, execute:

   ```bash
   git init
   git add .
   git commit -m "Primeiro commit"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   git push -u origin main
   ```

3. Depois, no Streamlit Cloud:
   - clique em "New app";
   - conecte o repositório;
   - escolha a branch `main`;
   - defina o arquivo principal como `CalculadoradePergaminho/app.py`;
   - confirme que o `requirements.txt` está em `CalculadoradePergaminho/requirements.txt`.

4. Se o Streamlit Cloud pedir versão do Python, use 3.12.
