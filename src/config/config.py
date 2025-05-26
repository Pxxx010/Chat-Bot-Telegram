import logging
from telebot import TeleBot
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração do Bot
CHAVE_API = os.getenv('TELEGRAM_API_KEY')
if not CHAVE_API:
    raise ValueError("TELEGRAM_API_KEY não encontrada no arquivo .env")

ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
if not ADMIN_ID:
    raise ValueError("ADMIN_ID não encontrado no arquivo .env")

# Inicialização do bot
bot = TeleBot(CHAVE_API, parse_mode="Markdown")

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot_mecanica.log',
    encoding='latin-1'
)
logger = logging.getLogger(__name__)

# Dados da Mecânica
MECANICA_INFO = {
    "nome": "Auto Center Express",
    "telefone": "(11) 99999-9999",
    "endereco": "Rua das Oficinas, 123",
    "horario": "Seg-Sex: 8h às 18h, Sáb: 8h às 12h",
    "whatsapp": "https://wa.me/5511999999999"
}

# Serviços Disponíveis
SERVICOS = {
    "revisao": {
        "nome": "Revisão Completa",
        "descricao": "Verificação completa do veículo",
        "tempo_estimado": "2-3 horas",
        "preco": "R$ 250,00"
    },
    "oleo": {
        "nome": "Troca de Óleo",
        "descricao": "Troca de óleo e filtros",
        "tempo_estimado": "1 hora",
        "preco": "R$ 150,00"
    },
    "freios": {
        "nome": "Revisão de Freios",
        "descricao": "Verificação e troca de pastilhas",
        "tempo_estimado": "1-2 horas",
        "preco": "R$ 200,00"
    },
    "pneus": {
        "nome": "Alinhamento e Balanceamento",
        "descricao": "Alinhamento, balanceamento e calibragem",
        "tempo_estimado": "1 hora",
        "preco": "R$ 120,00"
    }
}

# Arquivos
AGENDAMENTOS_FILE = 'agendamentos.json' 