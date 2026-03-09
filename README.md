# API de Verificação de Email

API simples para **verificação de e-mail com código temporário**, desenvolvida com **FastAPI**.  
A aplicação envia um código de verificação por e-mail e utiliza **JWT** para validar o código sem necessidade de banco de dados.

## Funcionalidades

- Envio de código de verificação por e-mail
- Token JWT com expiração automática
- Validação do código enviado
- API REST simples
- Deploy compatível com **Render**

## Como funciona

1. O usuário envia um e-mail para a rota `/enviar-email/`
2. A API:
   - gera um código de 4 dígitos
   - cria um token JWT contendo:
     - email
     - código
     - data de criação
     - data de expiração (1 minuto)
3. O código é enviado para o e-mail do usuário
4. O usuário envia o código e o token para `/verificar-email/`
5. A API valida o código dentro do token

Não é necessário banco de dados porque o código é armazenado dentro do próprio JWT.

---

# Tecnologias utilizadas

- Python
- FastAPI
- JWT (`python-jose`)
- SMTP (Gmail)
- Pydantic
- Uvicorn

---

# Crie Variáveis de Ambiente

- EMAIL_REMETENTE=seu_email@gmail.com
- EMAIL_SENHA_APP=sua_senha_de_app_gmail
- JWT_SECRET=um_segredo_muito_seguro
