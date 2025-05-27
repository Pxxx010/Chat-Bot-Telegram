import os
from telebot import TeleBot
from config.config import CHAVE_API, logger, bot
from handlers.bot_handlers import *
from flask import Flask, jsonify
import threading
import time
from datetime import datetime
import sys

app = Flask(__name__)
start_time = datetime.now()
bot_status = {
    "status": "running",
    "start_time": start_time.strftime("%d/%m/%Y %H:%M:%S"),
    "uptime": 0
}

@app.route('/')
def status():
    """Endpoint para verificar o status do bot"""
    uptime_seconds = (datetime.now() - start_time).total_seconds()
    uptime_hours = round(uptime_seconds / 3600, 2)  # Converte para horas com 2 casas decimais
    bot_status["uptime"] = f"{uptime_hours} horas"
    return jsonify(bot_status)

def run_flask():
    """Inicia o servidor Flask"""
    app.run(host='0.0.0.0', port=8080)

def main():
    """Função principal que inicia o bot e o servidor web"""
    try:
        logger.info("Iniciando o bot...")
        
        # Inicia o servidor Flask em uma thread separada
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        
        # Inicia o bot com configurações específicas
        bot.remove_webhook()  # Remove webhook anterior se existir
        time.sleep(1)  # Pequena pausa para garantir que o webhook foi removido
        
        # Configura o polling com parâmetros específicos
        bot.polling(none_stop=True, interval=0, timeout=20, allowed_updates=[])
        
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {e}")
        print(f"Erro fatal: {e}")
        sys.exit(1)  # Força a saída do programa em caso de erro

if __name__ == "__main__":
    main() 