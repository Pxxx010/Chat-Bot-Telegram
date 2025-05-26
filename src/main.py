from telebot import TeleBot
from config.config import CHAVE_API, logger, bot
from handlers.bot_handlers import *

def main():
    """Função principal que inicia o bot"""
    try:
        logger.info("Iniciando o bot...")
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")
        raise

if __name__ == "__main__":
    main() 