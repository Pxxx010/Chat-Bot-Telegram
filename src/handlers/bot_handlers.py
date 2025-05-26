from telebot import types
from config.config import (
    bot, logger, MECANICA_INFO, SERVICOS, ADMIN_ID
)
from utils.validators import validar_cpf, validar_data
from models.agendamento import adicionar_agendamento, carregar_agendamentos
import telebot.apihelper

# Dicionário para armazenar dados temporários do agendamento
agendamentos_temp = {}

def criar_markup_voltar():
    """Cria um markup padrão com botão de voltar"""
    markup = types.InlineKeyboardMarkup()
    btn_voltar = types.InlineKeyboardButton("« Voltar ao Menu", callback_data="voltar_menu")
    markup.add(btn_voltar)
    return markup

def enviar_menu_principal(chat_id, message_id=None):
    """Cria e envia a mensagem do menu principal"""
    try:
        nome_usuario = bot.get_chat(chat_id).first_name
    except Exception as e:
        logger.error(f"Erro ao obter nome do usuário: {e}")
        nome_usuario = "Cliente"

    texto = f"""Olá, {nome_usuario}! 👋

Bem-vindo à *{MECANICA_INFO['nome']}* 🚗
Como posso ajudar você hoje?

Selecione uma opção:"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_agendar = types.InlineKeyboardButton("📅 Agendar Serviço", callback_data="agendar")
    btn_servicos = types.InlineKeyboardButton("🔧 Nossos Serviços", callback_data="servicos")
    btn_horario = types.InlineKeyboardButton("⏰ Horário de Funcionamento", callback_data="horario")
    btn_local = types.InlineKeyboardButton("📍 Localização", callback_data="local")
    btn_contato = types.InlineKeyboardButton("📞 Contato", callback_data="contato")
    
    # Adiciona o botão de logs apenas para o administrador
    if chat_id == ADMIN_ID:
        btn_logs = types.InlineKeyboardButton("📊 Ver Logs", callback_data="ver_logs")
        markup.add(btn_agendar, btn_servicos, btn_horario, btn_local, btn_contato, btn_logs)
    else:
        markup.add(btn_agendar, btn_servicos, btn_horario, btn_local, btn_contato)

    try:
        if message_id:
            bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup)
        else:
            bot.send_message(chat_id, texto, reply_markup=markup)
    except Exception as e:
        logger.error(f"Erro ao enviar menu principal: {e}")
        bot.send_message(chat_id, "Desculpe, ocorreu um erro. Por favor, tente novamente.")

@bot.message_handler(commands=["start", "iniciar"])
def iniciar(mensagem):
    """Inicia o bot e envia o menu principal"""
    try:
        # Limpa qualquer agendamento temporário pendente
        if mensagem.chat.id in agendamentos_temp:
            del agendamentos_temp[mensagem.chat.id]
            
        enviar_menu_principal(mensagem.chat.id)
        logger.info(f"Bot iniciado para o usuário {mensagem.chat.id}")
    except Exception as e:
        logger.error(f"Erro ao iniciar bot: {e}")
        bot.reply_to(mensagem, "Desculpe, ocorreu um erro. Por favor, tente novamente.")

@bot.callback_query_handler(func=lambda call: True)
def responder_callback(call):
    """Processa todos os cliques nos botões inline"""
    try:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        markup_voltar = criar_markup_voltar()

        # Limpa qualquer agendamento temporário pendente ao voltar ao menu
        if call.data == "voltar_menu":
            if chat_id in agendamentos_temp:
                del agendamentos_temp[chat_id]
            try:
                enviar_menu_principal(chat_id, message_id)
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" not in str(e):
                    raise
            bot.answer_callback_query(call.id)
            return

        elif call.data == "agendar":
            # Limpa qualquer agendamento temporário pendente
            if chat_id in agendamentos_temp:
                del agendamentos_temp[chat_id]
                
            markup = types.InlineKeyboardMarkup(row_width=2)
            for servico_id, servico in SERVICOS.items():
                btn = types.InlineKeyboardButton(
                    f"{servico['nome']} - {servico['preco']}", 
                    callback_data=f"agendar_{servico_id}"
                )
                markup.add(btn)
            markup.add(types.InlineKeyboardButton("« Voltar ao Menu", callback_data="voltar_menu"))
            
            texto = "*📅 Agendamento de Serviços*\n\nSelecione o serviço desejado:"
            try:
                bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup)
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" not in str(e):
                    raise

        elif call.data.startswith("agendar_"):
            # Limpa qualquer agendamento temporário pendente
            if chat_id in agendamentos_temp:
                del agendamentos_temp[chat_id]
                
            servico_id = call.data.split("_")[1]
            servico = SERVICOS[servico_id]
            
            # Inicializa o agendamento temporário
            agendamentos_temp[chat_id] = {
                "servico_id": servico_id,
                "servico_nome": servico["nome"],
                "servico_preco": servico["preco"],
                "etapa": "nome"
            }
            
            texto = f"""*Agendamento - {servico['nome']}*

📋 *Detalhes do Serviço:*
- Descrição: {servico['descricao']}
- Tempo Estimado: {servico['tempo_estimado']}
- Preço: {servico['preco']}

Por favor, digite seu *nome completo*:"""
            
            try:
                bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup_voltar)
                # Remove qualquer handler anterior antes de registrar o novo
                bot.clear_step_handler(call.message)
                bot.register_next_step_handler(call.message, processar_nome)
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" not in str(e):
                    raise

        elif call.data == "servicos":
            texto = "*🔧 Nossos Serviços*\n\n"
            for servico in SERVICOS.values():
                texto += f"*{servico['nome']}*\n"
                texto += f"📝 {servico['descricao']}\n"
                texto += f"⏱ Tempo: {servico['tempo_estimado']}\n"
                texto += f"💰 Preço: {servico['preco']}\n\n"
            
            try:
                bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup_voltar)
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" not in str(e):
                    raise

        elif call.data == "horario":
            texto = f"""*⏰ Horário de Funcionamento*

{MECANICA_INFO['horario']}

Para agendamentos fora do horário, entre em contato pelo WhatsApp:
{MECANICA_INFO['whatsapp']}"""
            
            try:
                bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup_voltar)
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" not in str(e):
                    raise

        elif call.data == "local":
            texto = f"""*📍 Localização*

{MECANICA_INFO['nome']}
Endereço: {MECANICA_INFO['endereco']}

[Ver no Google Maps](https://maps.google.com/?q={MECANICA_INFO['endereco'].replace(' ', '+')})"""
            
            try:
                bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup_voltar)
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" not in str(e):
                    raise

        elif call.data == "contato":
            texto = f"""*📞 Contato*

📱 WhatsApp: {MECANICA_INFO['whatsapp']}
📞 Telefone: {MECANICA_INFO['telefone']}
📍 Endereço: {MECANICA_INFO['endereco']}

Horário de Atendimento:
{MECANICA_INFO['horario']}"""
            
            try:
                bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup_voltar)
            except telebot.apihelper.ApiTelegramException as e:
                if "message is not modified" not in str(e):
                    raise

        elif call.data == "ver_logs":
            if chat_id != ADMIN_ID:
                try:
                    bot.answer_callback_query(call.id, "❌ Acesso Negado", show_alert=True)
                    bot.edit_message_text(
                        "⚠️ *Você não tem permissão para acessar os logs do sistema.*\n\n"
                        "Esta função é restrita apenas para administradores.",
                        chat_id, 
                        message_id, 
                        reply_markup=markup_voltar,
                        parse_mode="Markdown"
                    )
                except telebot.apihelper.ApiTelegramException as e:
                    if "message is not modified" not in str(e):
                        raise
                return
                
            try:
                with open('bot_mecanica.log', 'r', encoding='latin-1') as arquivo:
                    logs = arquivo.readlines()
                    ultimos_logs = logs[-50:] if len(logs) > 50 else logs
                    texto_logs = "".join(ultimos_logs)
                    
                    if len(texto_logs) > 4000:
                        texto_logs = texto_logs[-4000:]
                    
                    bot.edit_message_text(
                        f"📊 *Últimos Logs do Sistema*\n\n```\n{texto_logs}\n```",
                        chat_id,
                        message_id,
                        reply_markup=markup_voltar,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                logger.error(f"Erro ao ler logs: {str(e)}")
                try:
                    bot.edit_message_text(
                        "❌ Erro ao ler os logs. Por favor, tente novamente mais tarde.",
                        chat_id,
                        message_id,
                        reply_markup=markup_voltar,
                        parse_mode="Markdown"
                    )
                except telebot.apihelper.ApiTelegramException as e:
                    if "message is not modified" not in str(e):
                        raise

        try:
            bot.answer_callback_query(call.id)
        except telebot.apihelper.ApiTelegramException as e:
            if "query is too old" not in str(e):
                raise

    except Exception as e:
        logger.error(f"Erro ao processar callback: {e}")
        try:
            bot.answer_callback_query(call.id, "Desculpe, ocorreu um erro. Por favor, tente novamente.")
        except:
            pass

def processar_nome(mensagem):
    """Processa o nome do cliente"""
    chat_id = mensagem.chat.id
    if chat_id not in agendamentos_temp:
        bot.reply_to(mensagem, "Sessão de agendamento expirada. Por favor, inicie novamente.")
        return

    nome = mensagem.text.strip()
    if len(nome) < 3:
        bot.reply_to(mensagem, "Por favor, digite seu nome completo (mínimo 3 caracteres).")
        bot.register_next_step_handler(mensagem, processar_nome)
        return

    agendamentos_temp[chat_id]["nome"] = nome
    agendamentos_temp[chat_id]["etapa"] = "cpf"
    
    bot.reply_to(mensagem, "Por favor, digite seu *CPF* (apenas números):")
    bot.register_next_step_handler(mensagem, processar_cpf)

def processar_cpf(mensagem):
    """Processa o CPF do cliente"""
    chat_id = mensagem.chat.id
    if chat_id not in agendamentos_temp:
        bot.reply_to(mensagem, "Sessão de agendamento expirada. Por favor, inicie novamente.")
        return

    cpf = mensagem.text.strip()
    if not validar_cpf(cpf):
        bot.reply_to(mensagem, "CPF inválido. Por favor, digite um CPF válido (apenas números):")
        bot.register_next_step_handler(mensagem, processar_cpf)
        return

    agendamentos_temp[chat_id]["cpf"] = cpf
    agendamentos_temp[chat_id]["etapa"] = "data"
    
    bot.reply_to(mensagem, "Por favor, digite a *data do agendamento* (formato DD/MM/AAAA):")
    bot.register_next_step_handler(mensagem, processar_data)

def processar_data(mensagem):
    """Processa a data do agendamento"""
    chat_id = mensagem.chat.id
    if chat_id not in agendamentos_temp:
        bot.reply_to(mensagem, "Sessão de agendamento expirada. Por favor, inicie novamente.")
        return

    data = mensagem.text.strip()
    if not validar_data(data):
        bot.reply_to(mensagem, "Data inválida. Por favor, digite uma data válida no formato DD/MM/AAAA (apenas dias úteis):")
        bot.register_next_step_handler(mensagem, processar_data)
        return

    agendamento = agendamentos_temp[chat_id]
    agendamento["data"] = data
    
    # Salva o agendamento
    adicionar_agendamento(chat_id, agendamento)
    
    # Envia confirmação para o cliente
    texto = f"""✅ *Agendamento Confirmado!*

📋 *Detalhes do Agendamento:*
- Nome: {agendamento['nome']}
- CPF: {agendamento['cpf']}
- Serviço: {agendamento['servico_nome']}
- Data: {agendamento['data']}
- Preço: {agendamento['servico_preco']}

Para mais informações, entre em contato:
📱 WhatsApp: {MECANICA_INFO['whatsapp']}
📞 Telefone: {MECANICA_INFO['telefone']}"""
    
    markup = types.InlineKeyboardMarkup()
    btn_voltar = types.InlineKeyboardButton("« Voltar ao Menu", callback_data="voltar_menu")
    markup.add(btn_voltar)
    
    # Limpa os dados temporários antes de enviar a mensagem
    try:
        del agendamentos_temp[chat_id]
    except KeyError:
        pass
    
    bot.send_message(chat_id, texto, reply_markup=markup, parse_mode="Markdown")
    
    # Envia notificação para o administrador
    try:
        texto_admin = f"""🔔 *Novo Agendamento!*

📋 *Detalhes do Cliente:*
- Nome: {agendamento['nome']}
- CPF: {agendamento['cpf']}
- ID do Chat: `{chat_id}`

📅 *Detalhes do Serviço:*
- Serviço: {agendamento['servico_nome']}
- Data: {agendamento['data']}
- Preço: {agendamento['servico_preco']}

Para ver todos os agendamentos, use o comando /agendamentos"""
        
        bot.send_message(ADMIN_ID, texto_admin, parse_mode="Markdown")
        logger.info(f"Notificação de novo agendamento enviada para o administrador (ID: {ADMIN_ID})")
    except Exception as e:
        logger.error(f"Erro ao enviar notificação para o administrador: {e}")

@bot.message_handler(commands=["agendamentos"])
def listar_agendamentos(mensagem):
    """Lista todos os agendamentos (apenas para administrador)"""
    if mensagem.chat.id != ADMIN_ID:
        bot.reply_to(mensagem, "⚠️ *Você não tem permissão para acessar os agendamentos.*\n\nEsta função é restrita apenas para administradores.")
        return

    try:
        agendamentos = carregar_agendamentos()
        if not agendamentos:
            bot.reply_to(mensagem, "📅 *Não há agendamentos registrados.*")
            return

        texto = "📅 *Lista de Agendamentos*\n\n"
        for chat_id, agendamentos_cliente in agendamentos.items():
            texto += f"👤 *Cliente ID:* `{chat_id}`\n"
            for agendamento in agendamentos_cliente:
                texto += f"""
📋 *Detalhes:*
- Nome: {agendamento['nome']}
- CPF: {agendamento['cpf']}
- Serviço: {agendamento['servico_nome']}
- Data: {agendamento['data']}
- Preço: {agendamento['servico_preco']}
-------------------\n"""
            texto += "\n"

        # Se o texto for muito grande, divide em partes
        if len(texto) > 4000:
            partes = [texto[i:i+4000] for i in range(0, len(texto), 4000)]
            for parte in partes:
                bot.send_message(mensagem.chat.id, parte, parse_mode="Markdown")
        else:
            bot.reply_to(mensagem, texto, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Erro ao listar agendamentos: {e}")
        bot.reply_to(mensagem, "❌ Ocorreu um erro ao listar os agendamentos. Por favor, tente novamente mais tarde.")

@bot.message_handler(func=lambda mensagem: True)
def responder_padrao(mensagem):
    """Responde a qualquer mensagem que não seja um comando conhecido"""
    try:
        texto = "Não compreendi sua mensagem. Por favor, utilize o comando /iniciar para ver as opções disponíveis."
        bot.reply_to(mensagem, texto)
        logger.info(f"Mensagem não reconhecida de {mensagem.chat.id}: {mensagem.text}")
    except Exception as e:
        logger.error(f"Erro ao responder mensagem padrão: {e}") 