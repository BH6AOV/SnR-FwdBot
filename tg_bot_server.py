#!/usr/bin/env python

# -*- coding: utf-8 -*-
import json
import telegram
import config
import os
import logger
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler
from telegram.bot import Bot

bot_ = None
chat_ids_ = {}
logger_ = logger.create_logger("snr_bot_logs")


def save_chat_ids_to_file():
    global chat_ids_
    file_str = json.dumps(chat_ids_)
    with open("chat_ids.dat", "w") as rf:
        rf.write(file_str)
        rf.close()


def load_chat_ids_from_file():
    global chat_ids_
    if os.path.exists("chat_ids.dat"):
        with open("chat_ids.dat", "r") as rf:
            file_str = rf.read()
            chat_ids_ = json.loads(file_str)
            rf.close()


def start_callback(bot, update):
    global chat_ids_
    global logger_
    try:
        chat_ids_[update.message.chat_id] = update.message.from_user.id
        logger_.info('/start chat_id: ' + str(update.message.chat_id))
        update.message.reply_text('''
恭喜订阅成功(chatid: %(chat_id)s)
使用方法：您只需要/start我，或者把我拉到您的群中，并/start即可。''' % {'chat_id' : update.message.chat_id})
        save_chat_ids_to_file()
    except:
        pass


def stop_callback(bot, update):
    global chat_ids_
    global logger_
    try:
        chat_ids_.pop(update.message.chat_id)
        logger_.info('/stop chat_id: ' + str(update.message.chat_id))
        update.message.reply_text('谢谢您的使用，再见')
        save_chat_ids_to_file()
    except:
        pass


def help_callback(bot, update):
    update.message.reply_text('''坐和放宽联盟SitandRelax Union消息聚合机器人
功能介绍：此机器人为坐和放宽联盟（SitandRelax Union）频道消息整合服务。
您可以不必分别关注联盟的许多channel，一样可以畅快的阅读联盟提供的各种资讯。
使用方法：您只需要/start我，或者把 @snr_union_bot 拉到您的群中并/start，或者关注 @sitandrelaxunionint 均可。''')


def msg_callback(bot, update):
    global chat_ids_
    global logger_
    if update.channel_post is not None:
        logger_.info('recvice from: ' + str(update.channel_post.chat.username) + ' chat_id: ' + str(update.channel_post.chat.id) + '  msg: ' + update.channel_post.text)
        if str(update.channel_post.chat.id) not in config.auth_channel_id:
            logger_.info('recvice from username: ' + str(update.channel_post.chat.username) + ' chat_id: ' + str(update.channel_post.chat.id) + ' unauth channel msg ' + update.channel_post.text)
            return
        for key,val in chat_ids_.items():
            try:
                update.channel_post.forward(key, disable_notification=False)
                logger_.info('forward from: ' + str(update.channel_post.chat.username) + ' to: ' + key + ' msg: ' + update.channel_post.text)
            except:
                logger_.error('forward msg failed: chat_id: %(chat_id)s' % {'chat_id' : key})
        try:
            bot.forwardMessage('@sitandrelaxunionint', from_chat_id=update.channel_post.chat_id, disable_notification=False, message_id=update.channel_post.message_id)
        except:
            logger_.error('forward msg to @sitandrelaxunionint failed')

if __name__ == "__main__":

    print("Main start")
    load_chat_ids_from_file()

    updater = Updater(config.bot_token)

    updater.dispatcher.add_handler(CommandHandler('start', start_callback))
    updater.dispatcher.add_handler(CommandHandler('stop', stop_callback))
    updater.dispatcher.add_handler(CommandHandler('help', help_callback))
    updater.dispatcher.add_handler(MessageHandler(None, msg_callback))

    bot_ = updater.bot

    updater.start_polling()
    updater.idle()

    logger.shutdown_logger(logger_)
    print("Main exit")

