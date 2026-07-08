from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update
from app.config.configBot import settingsBot
from app.rag_chain import initialize_chain, get_answer

SEGUNDOS_INACTIVO = 300


async def despedida(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    await context.bot.send_message(
        chat_id=chat_id,
        text="Parece que ya no estás por aquí 👋 Si tienes más preguntas sobre StayDesk, "
             "escríbeme cuando quieras. ¡Hasta pronto!"
    )


def reprogramar_despedida(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    jobs_actuales = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs_actuales:
        job.schedule_removal()

    context.job_queue.run_once(
        despedida,
        when=SEGUNDOS_INACTIVO,
        chat_id=chat_id,
        name=str(chat_id),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"¡Hola {nombre}! Soy Desky 👋, encantado de saludarte.\n\n"
        "Estoy aquí para contarte todo sobre StayDesk y resolver cualquier duda que tengas. ¿Por dónde empezamos?"
    )
    reprogramar_despedida(context, update.effective_chat.id)


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        resultado = get_answer(pregunta)
        await update.message.reply_text(resultado["answer"])
    except Exception as e:
        await update.message.reply_text(
            "Ups, tuve un problema procesando tu pregunta. Intenta de nuevo en un momento 🙏"
        )
        print(f"Error en responder(): {e}")

    reprogramar_despedida(context, update.effective_chat.id)


def main():
    print("Inicializando pipeline RAG para el bot...")
    initialize_chain()

    app = ApplicationBuilder().token(settingsBot.TOKEN_TELEGRAM_BOT).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot corriendo con webhook...")
    app.run_webhook(
        listen="127.0.0.1",
        port=8443,
        url_path=settingsBot.TOKEN_TELEGRAM_BOT,
        webhook_url=f"https://staydesk-bot.duckdns.org/{settingsBot.TOKEN_TELEGRAM_BOT}",
    )

if __name__ == "__main__":
    main()