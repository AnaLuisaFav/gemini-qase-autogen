# Gerador de Casos de Teste com Gemini + Qase

Este projeto automatiza a geração e o envio de casos de teste para o [Qase.io](https://qase.io) com base em requisitos informados em linguagem natural, utilizando a IA do Gemini.

## 🚀 Funcionalidades

- ✍️ Geração automática de casos de teste com base em requisitos textuais
- 📤 Envio direto dos casos para o Qase via API
- 🧠 Mapeamento inteligente de campos obrigatórios (prioridade, severidade, tipo etc.)

## 📁 Estrutura do Projeto

```
.
├── .example.env        # Exemplo de variáveis para configuração
├── .gitignore
├── main.py             # Script principal
└── qase/               # Pacote com lógicas auxiliares
    ├── mappings.py     # Mapeamentos texto → ID do Qase
    ├── payload_builder.py  # Função para montar payload da API
    ├── prompt.py       # Prompt para o Gemini
    └── utils.py        # Funções auxiliares
```

## 📊 Requisitos

- Python 3.9+
- Conta e projeto criado no [Qase.io](https://qase.io)

### Instale com:

```
pip install -r requirements.txt
```

## ⚙️ Configuração .env

Preencha o arquivo `.example.env` com as suas credenciais e renomeie-o para `.env`

## ⚡ Uso

1. Execute o script:

`python main.py`

2. Cole o requisito e pressione:

```
Ctrl+Z + Enter (Windows)
```

```
Ctrl+D (Linux/macOS)
```

Os casos de teste serão gerados e enviados ao Qase.

```
📋 Exemplo de requisito

Como usuário, quero poder fazer login usando e-mail e senha, para acessar minha conta com segurança.
```

## 🚜 Futuras melhorias

- Leitura automática dos requisitos através do ticket no Jira.

##

Feito com ❤️ por QA + IA.
