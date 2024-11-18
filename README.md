# email-tools
# temp-mail-generator.py
	# Automação de Criação de Contas com E-mails Temporários
	
	Este projeto em Python permite a criação de e-mails temporários, captura de mensagens para códigos OTP e registro automático de contas. Pode ser configurado para criar **uma única conta** ou **várias contas automaticamente**.
	
	---
	
	## **Funcionalidades**
	- Gera e-mails temporários utilizando a API `temp-mail.io`.
	- Captura mensagens e extrai códigos OTP automaticamente.
	- Registra contas em uma plataforma com autenticação OTP.
	- Salva tokens gerados em um arquivo para uso futuro.
	
	---
	
	## **Instalação no Termux**
	
	Siga os passos abaixo para configurar e executar o projeto no Termux:
	
	### **1. Atualizar pacotes**
	Execute os seguintes comandos:
	```bash
	pkg update -y && pkg upgrade -y
	pkg install python git -y
 	git clone https://github.com/museu-do-novo/email-tools.git
	cd email-tools
	pip install -r requirements.txt
# temp-mail-get-message.py
	script simples para vizualizar as mensagens que chegam no seu email temporario
 
