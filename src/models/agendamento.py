import json
import os
from config.config import AGENDAMENTOS_FILE, logger

def carregar_agendamentos():
    """Carrega os agendamentos do arquivo JSON"""
    try:
        if os.path.exists(AGENDAMENTOS_FILE):
            with open(AGENDAMENTOS_FILE, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error("Erro ao decodificar o arquivo de agendamentos. Criando novo arquivo.")
                    return {}
        return {}
    except Exception as e:
        logger.error(f"Erro ao carregar agendamentos: {e}")
        return {}

def salvar_agendamentos(agendamentos):
    """Salva os agendamentos no arquivo JSON"""
    try:
        with open(AGENDAMENTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(agendamentos, f, ensure_ascii=False, indent=4)
        logger.info("Agendamentos salvos com sucesso")
    except Exception as e:
        logger.error(f"Erro ao salvar agendamentos: {e}")
        raise

def adicionar_agendamento(chat_id, agendamento):
    """Adiciona um novo agendamento"""
    try:
        agendamentos = carregar_agendamentos()
        if str(chat_id) not in agendamentos:
            agendamentos[str(chat_id)] = []
        agendamentos[str(chat_id)].append(agendamento)
        salvar_agendamentos(agendamentos)
        logger.info(f"Novo agendamento adicionado para o chat_id {chat_id}")
        return agendamentos
    except Exception as e:
        logger.error(f"Erro ao adicionar agendamento: {e}")
        raise 