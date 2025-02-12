
import requests
import re
import random
import logging
from faker import Faker
from time import sleep

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
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choices(chars, k=length))

def create_temp_email(domain="ehra.com"):
    """Cria um e-mail temporário usando a API temp-mail.io."""
    name = faker.first_name().lower()
    url = 'https://api.internal.temp-mail.io/api/v3/email/new'
    data = {'name': name, 'domain': domain}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        email = response.json().get('email')
        logging.info(f"E-mail temporário criado: {email}")
        return email
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao criar e-mail: {e}")
        print("Falha ao criar o e-mail.")
        return None

def list_messages(email):
    """Lista as mensagens recebidas no e-mail temporário em um loop contínuo."""
    url = f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages'
    print("\nAguardando mensagens... (Pressione Ctrl + C para sair)\n")
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            messages = response.json()

            if messages:
                for msg in messages:
                    print(f"Assunto: {msg.get('subject', 'Sem assunto')}")
                    print(f"Conteúdo: {msg.get('body_text', 'Sem conteúdo')}")
                    print("---")
            else:
                print("Nenhuma mensagem encontrada.")
            sleep(10)  # Verifica novas mensagens a cada 10 segundos
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao buscar mensagens: {e}")
            print("Falha ao buscar mensagens.")
        except KeyboardInterrupt:
            print("\nSaindo...")
            break

def main():
    """Função principal do script."""
    print("=== Script de E-mail Temporário ===")
    
    # Cria um e-mail temporário
    email = create_temp_email()
    if not email:
        return

    # Gera uma senha aleatória
    password = generate_password()
    print(f"\nSeu e-mail temporário é: {email}")
    print(f"Senha gerada: {password}\n")

    # Inicia o loop para listar mensagens
    list_messages(email)

if __name__ == "__main__":
    main()
