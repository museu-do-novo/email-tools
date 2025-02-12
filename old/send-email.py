from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email, subject, content):
    """
    Envia um e-mail usando a API do SendGrid.
    
    Parâmetros:
        to_email (str): Endereço do destinatário.
        subject (str): Assunto do e-mail.
        content (str): Conteúdo do e-mail.
    """
    try:
        # Configure os detalhes do e-mail
        message = Mail(
            from_email='from_email@example.com',  # Altere para seu e-mail
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )

        # Inicialize o cliente SendGrid
        sg = SendGridAPIClient('YOUR_API_KEY')  # Substitua pela sua chave API
        response = sg.send(message)

        # Verifica o status do envio
        if response.status_code == 202:
            print("E-mail enviado com sucesso!")
        else:
            print(f"Falha ao enviar e-mail. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def main():
    """
    Função principal para capturar dados do usuário e enviar o e-mail.
    """
    print("### Envio de E-mail com SendGrid ###")

    # Captura os dados de entrada
    from_email = input("Digite o seu endereço de e-mail (remetente): ").strip()
    to_email = input("Digite o endereço de e-mail do destinatário: ").strip()
    subject = input("Digite o assunto do e-mail: ").strip()
    content = input("Digite o conteúdo do e-mail: ").strip()

    # Validação básica das entradas
    if not from_email or not to_email or not subject or not content:
        print("Erro: Todos os campos são obrigatórios.")
        return

    if "@" not in from_email or "@" not in to_email:
        print("Erro: Insira endereços de e-mail válidos.")
        return

    # Envio do e-mail
    try:
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )
        sg = SendGridAPIClient('YOUR_API_KEY')  # Substitua pela sua chave API
        response = sg.send(message)

        # Retorna o status
        if response.status_code == 202:
            print("E-mail enviado com sucesso!")
        else:
            print(f"Falha ao enviar e-mail. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    main()
