import requests
import re
import random
import logging
import argparse
import os
from faker import Faker
from time import sleep
from colorama import init, Fore, Style

# Inicializa o colorama
init(autoreset=True)

# Configurar logs
logging.basicConfig(
    filename='automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializa o gerador de dados falsos
faker = Faker()

def install_requirements():
    """Instala as dependências necessárias."""
    print(Fore.YELLOW + "Instalando dependências..." + Style.RESET_ALL)
    os.system("pip install -r requirements.txt")

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
        print(Fore.RED + "Falha ao criar o e-mail." + Style.RESET_ALL)
        return None

def list_messages(email):
    """Lista as mensagens recebidas no e-mail temporário em um loop contínuo."""
    url = f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages'
    print(Fore.CYAN + "\nAguardando mensagens... (Pressione Ctrl + C para sair)\n" + Style.RESET_ALL)
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            messages = response.json()

            if messages:
                os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela
                for msg in messages:
                    print(Fore.GREEN + f"Assunto: {msg.get('subject', 'Sem assunto')}" + Style.RESET_ALL)
                    print(Fore.YELLOW + f"Conteúdo: {msg.get('body_text', 'Sem conteúdo')}" + Style.RESET_ALL)
                    print("---")
            else:
                print(Fore.RED + "Nenhuma mensagem encontrada." + Style.RESET_ALL)
            sleep(10)  # Verifica novas mensagens a cada 10 segundos
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao buscar mensagens: {e}")
            print(Fore.RED + "Falha ao buscar mensagens." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.CYAN + "\nSaindo..." + Style.RESET_ALL)
            break

def main():
    """Função principal do script."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela no início
    print(Fore.BLUE + "=== Script de E-mail Temporário ===" + Style.RESET_ALL)
    
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description="Script para criar e-mails temporários e receber mensagens.")
    parser.add_argument('-c', '--create', action='store_true', help="Cria um e-mail temporário.")
    parser.add_argument('-l', '--list', metavar='EMAIL', help="Lista as mensagens de um e-mail temporário.")
    parser.add_argument('-d', '--domain', default="ehra.com", help="Define o domínio do e-mail temporário.")
    parser.add_argument('-p', '--password-length', type=int, default=8, help="Define o comprimento da senha gerada.")
    parser.add_argument('-i', '--install', action='store_true', help="Instala as dependências necessárias.")
    args = parser.parse_args()

    # Instala as dependências, se solicitado
    if args.install:
        install_requirements()
        return

    # Cria um e-mail temporário
    if args.create:
        email = create_temp_email(args.domain)
        if not email:
            return

        # Gera uma senha aleatória
        password = generate_password(args.password_length)
        print(Fore.GREEN + f"\nSeu e-mail temporário é: {email}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Senha gerada: {password}\n" + Style.RESET_ALL)

        # Inicia o loop para listar mensagens
        list_messages(email)

    # Lista mensagens de um e-mail existente
    elif args.list:
        if not validate_email(args.list):
            print(Fore.RED + "E-mail inválido. Por favor, insira um e-mail válido." + Style.RESET_ALL)
            return
        list_messages(args.list)

    # Exibe a ajuda se nenhum argumento for passado
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
