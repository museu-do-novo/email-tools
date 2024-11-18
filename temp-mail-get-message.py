import requests
import re

def validate_email(email):
    """Valida se o formato do e-mail é válido."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def list_messages():
    """Solicita o e-mail e lista todas as mensagens de um e-mail temporário."""
    email = input("Digite o seu e-mail temporário: ")
    
    # Valida o formato do e-mail
    if not validate_email(email):
        print("E-mail inválido. Por favor, insira um e-mail válido.")
        return

    url = f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta exceções para códigos de status HTTP 4xx/5xx
        
        # Tenta converter a resposta em JSON
        try:
            messages = response.json()
        except ValueError:
            print("Resposta inválida. Não foi possível converter os dados para JSON.")
            return

        if messages:
            for msg in messages:
                print(f"Assunto: {msg.get('subject', 'Sem assunto')}")
                print(f"Conteúdo: {msg.get('body_text', 'Sem conteúdo')}")
                print("---")
        else:
            print("Nenhuma mensagem encontrada.")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao listar mensagens: {e}")

# Chama a função para listar as mensagens
list_messages()
