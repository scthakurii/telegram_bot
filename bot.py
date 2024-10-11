import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from chat_responses import get_response, get_topics
from utils import load_passcode

TOKEN = '7867669215:AAHLcZlSIEhYBfaNqWaM82ad4i1kkTP-wzE'
PASSCODE = load_passcode()

PASSCODE_CHECK, CHATTING, TOPIC_SELECTION = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Welcome! Please enter the passcode to start chatting.")
    return PASSCODE_CHECK

async def check_passcode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == PASSCODE:
        topics = get_topics()
        keyboard = [[KeyboardButton(topic)] for topic in topics]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            "Passcode correct! What would you like to talk about?",
            reply_markup=reply_markup
        )
        return TOPIC_SELECTION
    else:
        await update.message.reply_text("Incorrect passcode. Please try again or use /start to restart.")
        return PASSCODE_CHECK

async def select_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_topic = update.message.text
    context.user_data['current_topic'] = user_topic
    await update.message.reply_text(f"Great! Let's talk about {user_topic}. What would you like to know?")
    return CHATTING

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_message = update.message.text
    current_topic = context.user_data.get('current_topic', 'general')
    
    response = get_response(current_topic, user_message)
    
    if response == "TOPIC_CHANGE":
        return await select_topic(update, context)
    elif response == "END_CHAT":
        await update.message.reply_text("Goodbye! It was nice chatting with you. Use /start if you want to chat again.")
        return ConversationHandler.END
    else:
        await update.message.reply_text(response)
        return CHATTING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Chat ended. Use /start to begin again.")
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PASSCODE_CHECK: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_passcode)],
            TOPIC_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_topic)],
            CHATTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()