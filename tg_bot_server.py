#!/usr/bin/env python

# -*- coding: utf-8 -*-
import json
import telegram
import config
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler
from telegram.bot import Bot

chat_ids_ = {}


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
    try:
        chat_ids_[update.message.chat_id] = update.message.from_user.id
        update.message.reply_text('''
恭喜订阅成功(chatid: %(chat_id)s)
使用方法：您只需要/start我，或者把我拉到您的群中，并/start即可。''' % {'chat_id' : update.message.chat_id})
        save_chat_ids_to_file()
    except:
        pass


def stop_callback(bot, update):
    global chat_ids_
    try:
        chat_ids_.pop(update.message.chat_id)
        update.message.reply_text('谢谢您的使用，再见')
        save_chat_ids_to_file()
    except:
        pass


def help_callback(bot, update):
    update.message.reply_text('''坐和放宽联盟SitandRelax Union消息聚合机器人
功能介绍：此机器人为坐和放宽联盟（SitandRelax Union）频道消息整合服务。
您可以不必分别关注联盟的许多channel，一样可以畅快的阅读联盟提供的各种资讯。
使用方法：您只需要/start我，或者把我拉到您的群中，并/start即可。''')


def msg_callback(bot, update):
    global chat_ids_
    if update.channel_post is not None:
        for key,val in chat_ids_.items():
            try:
                update.channel_post.forward(key, disable_notification=False)
                print('forward msg: ', update.channel_post.text, ' from: ', update.chanel_post.chat_id, ' to: ', val)
            except:
                print('forward msg failed: chat_id: %(chat_id)s' % {'chat_id' : key})


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

    print("Main exit")

