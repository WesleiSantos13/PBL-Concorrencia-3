# Use a imagem oficial do Python 3.11 como base
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o código fonte da aplicação para o contêiner
COPY . /app

EXPOSE 7798

# Instale as dependências Python
RUN pip install -r requirements.txt

# Comando para executar a aplicação
# CMD ["python", "main.py"]
CMD ["/bin/bash"]