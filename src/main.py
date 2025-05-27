import os
from telebot import TeleBot
from config.config import CHAVE_API, logger, bot
from handlers.bot_handlers import *

def main():
    """Função principal que inicia o bot"""
    try:
        logger.info("Iniciando o bot...")
        # Configuração da porta para o Render
        port = int(os.environ.get('PORT', 5000))
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")
        print(f"Erro fatal: {e}")
        raise

if __name__ == "__main__":
    main() 