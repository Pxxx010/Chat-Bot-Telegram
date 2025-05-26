# Bot de Agendamento para Mecânica 🚗

Este é um bot do Telegram desenvolvido para automatizar o processo de agendamento de serviços em uma oficina mecânica.

[![Bot no Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram)](https://t.me/afnproject_bot)

## Demonstração

[![Demonstração do Bot](https://img.youtube.com/vi/gKHHa84-Sp8/maxresdefault.jpg)](https://youtube.com/shorts/gKHHa84-Sp8)

## Funcionalidades

### Para Clientes
- 📅 Agendamento de serviços
- 🔧 Listagem de serviços disponíveis
- ⏰ Horário de funcionamento
- 📍 Localização da oficina
- 📞 Informações de contato

### Para Administradores
- 📊 Sistema de logs
- 🔔 Notificações de novos agendamentos
- 📋 Lista completa de agendamentos
- 👤 Acesso aos dados dos clientes

## Requisitos

- Python 3.7+
- pyTelegramBotAPI
- python-dotenv
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd chat-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
- Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```
- Edite o arquivo `.env` e adicione suas configurações:
```
TELEGRAM_API_KEY=sua_chave_api_aqui
ADMIN_ID=seu_id_do_telegram_aqui
```

## Estrutura do Projeto

```
chat-bot/
├── src/
│   ├── config/
│   │   └── config.py      # Configurações do bot
│   ├── handlers/
│   │   └── bot_handlers.py # Handlers do bot
│   ├── models/
│   │   └── agendamento.py # Gerenciamento de agendamentos
│   ├── utils/
│   │   └── validators.py  # Funções de validação
│   └── main.py           # Arquivo principal
├── .env                  # Variáveis de ambiente (não versionado)
├── .env.example         # Template para variáveis de ambiente
├── requirements.txt
└── README.md
```

## Executando o Bot

Para iniciar o bot, execute:

```bash
python src/main.py
```

## Configuração

### Variáveis de Ambiente
O bot utiliza as seguintes variáveis de ambiente (definidas no arquivo `.env`):

- `TELEGRAM_API_KEY`: Chave de API do seu bot do Telegram
- `ADMIN_ID`: ID do Telegram do administrador do bot

### Outras Configurações
As demais configurações podem ser ajustadas no arquivo `src/config/config.py`:

- Informações da mecânica
- Lista de serviços
- Configurações de logging

## Comandos Disponíveis

### Para Todos os Usuários
- `/start` ou `/iniciar` - Inicia o bot e mostra o menu principal

### Apenas para Administradores
- `/agendamentos` - Lista todos os agendamentos registrados
- Botão "📊 Ver Logs" - Mostra os últimos logs do sistema

## Funcionalidades de Agendamento

1. O cliente seleciona um serviço
2. Fornece nome completo
3. Informa CPF
4. Escolhe a data do agendamento
5. Recebe confirmação do agendamento

O administrador recebe uma notificação com todos os detalhes do agendamento.

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes. 