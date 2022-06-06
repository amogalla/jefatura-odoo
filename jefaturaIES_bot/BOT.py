#!/usr/bin/env python
import requests 
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import *
import json
from funciones_postgres import insertar_expulsion, insertar_chat_id, chats_telegram_profesores, get_nombre_completo_alumno
from acceso_postgres import conectar_psql
from info_bot import TOKEN

def start(update: Update, context: CallbackContext):

    usuario = update.message.from_user
    if insertar_chat_id(conectar_psql(), usuario['id'], usuario['username']):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='''Bienvenido al Sistema de Gestión de Expulsiones.\nSi tiene alguna duda sobre su funcionamiento, contacte con @Sr_Holmes. id = ''' + str(update.effective_chat.id)
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Su usuario de Telegram no está dado de alta correctamente en el sistema. Si cree que es un error, contacte con @Sr_Holmes."
        )


def help(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='''Estos son los comandos disponibles:
        /start: Comando inicial, necesario para comenzara a utilizar el bot.
        /help: Muestra la ayuda'''
    )

def respuestaBotonExpulsar(update: Update, context: CallbackContext):
    call_back_data = update.callback_query.data
    call_back_data = call_back_data.replace("'", "\"")
    datos_expulsion = json.loads(call_back_data)

    if datos_expulsion['alumno'] != "0":  # Expulsión
        context.bot.editMessageReplyMarkup(
            chat_id=update.effective_chat.id,
            message_id=datos_expulsion['msg']
            #text=call_back_data#.split()[0] + "-" + call_back_data.split()[1]
         )

        insertar_expulsion(conectar_psql(), datos_expulsion['alumno'], datos_expulsion['amonestaciones'])

        context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            reply_to_message_id=datos_expulsion['msg'],
            text=str("Se ha generado una expulsión en borrador. Recuerde validarla en el ERP para que se haga efectiva.")
            #text=call_back_data#.split()[0] + "-" + call_back_data.split()[1]
         )

        chats_profesores = chats_telegram_profesores(conectar_psql(), str(datos_expulsion['alumno']))

        for chat in chats_profesores:
            context.bot.sendMessage(
                chat_id=chat,
                text=str("Se ha propuesto una expulsión al alumno " + get_nombre_completo_alumno(conectar_psql(), str(datos_expulsion['alumno'])) + ". Recuerde indicar la tarea correspondiente a su asignatura.")
            )

    else:  # Indulto
        context.bot.editMessageReplyMarkup(
            chat_id=update.effective_chat.id,
            message_id=datos_expulsion['msg']
         )
        context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            reply_to_message_id=datos_expulsion['msg'],
            text=str("Se ha decidido indultar al alumno y no se ha generado ninguna expulsión. Si cambia de idea, deberá generarla desde el ERP.")
            #text=call_back_data#.split()[0] + "-" + call_back_data.split()[1]
         )


def main():
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CallbackQueryHandler(respuestaBotonExpulsar))
    
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
