import requests
import json
import random
import re
from faker import Faker
from time import sleep
import logging

# Configurações
MULTIPLE_ACCOUNTS = False  # True para criar múltiplos e-mails, False para apenas um

# Configurar logs
logging.basicConfig(
    filename='automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializa o gerador de dados falsos
faker = Faker()

def generate_password(length=8):
    """Gera uma senha alfanumérica aleatória."""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def create_temp_email():
    """Cria um e-mail temporário usando a API temp-mail.io."""
    name = faker.first_name()
    url = 'https://api.internal.temp-mail.io/api/v3/email/new'
    data = {'name': name, 'domain': 'ehra.com'}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        email = response.json().get('email')
        logging.info(f"E-mail temporário criado: {email}")
        print(f"Seu e-mail é: {email}")
        return email
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao criar e-mail: {e}")
        print("Falha ao criar o e-mail.")
        return None

def get_messages(email):
    """Captura mensagens do e-mail temporário."""
    url = f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages'
    while True:
        sleep(5)
        try:
            response = requests.get(url)
            response.raise_for_status()
            messages = response.json()

            if messages:
                for msg in messages:
                    subject = msg.get('subject', 'Sem assunto')
                    body_text = msg.get('body_text', '')
                    print(f"Assunto: {subject}")
                    match = re.search(r'\b\d{4}\b', body_text)
                    if match:
                        code = match.group(0)
                        print(f"Seu código OTP é: {code}")
                        logging.info(f"OTP recebido: {code}")
                        return code
            else:
                print("Nenhuma mensagem encontrada.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao capturar mensagens: {e}")
            print("Falha ao buscar mensagens.")

def verify_otp(email, code):
    """Verifica o código OTP na API."""
    url = "https://v1.prd.socket.araby.ai/otp/verify"
    payload = {
        "otp": code,
        "email": email
    }
    headers = {
        'User-Agent': "Dart/3.2 (dart:io)",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        if "Authentication successful" in response.text:
            token = response.json().get("token")
            logging.info(f"Autenticação bem-sucedida. Token: {token}")
            print(f"Autenticação bem-sucedida. Token: {token}")
            with open("Ai Tokens.txt", "a") as f:
                f.write(token + '\n')
            return token
        else:
            print("Falha ao verificar o código OTP.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na verificação do OTP: {e}")
    return None

def register_account(email, password):
    """Registra uma nova conta usando e-mail e senha."""
    url = "https://v1.prd.socket.araby.ai/register"
    payload = {
        "email": email,
        "password": password,
        "method": "OTP",
        "is_mobile": True
    }
    headers = {
        'User-Agent': "Dart/3.2 (dart:io)",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        if "User registered successfully! Please verify your email." in response.text:
            print("Usuário registrado com sucesso. Verifique seu e-mail.")
            code = get_messages(email)
            if code:
                return verify_otp(email, code)
        else:
            print("Falha ao registrar usuário.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro no registro de conta: {e}")
    return None

def main():
    """Função principal para criar contas."""
    if MULTIPLE_ACCOUNTS:
        while True:
            email = create_temp_email()
            if email:
                password = generate_password()
                print(f"Senha gerada: {password}")
                token = register_account(email, password)
                if token:
                    print(f"Registro concluído. Token: {token}")
    else:
        email = create_temp_email()
        if email:
            password = generate_password()
            print(f"Senha gerada: {password}")
            token = register_account(email, password)
            if token:
                print(f"Registro concluído. Token: {token}")

if __name__ == "__main__":
    main()
