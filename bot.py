import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================
# НАСТРОЙКИ
# ==================
TOKEN = "8100975204:AAG9qYVWKBlezS4eOZ6FKTfNU4zn0YJx99o"

# Ваш приветственный текст
WELCOME_TEXT = "Привет! 👋 Я задам тебе несколько вопросов. Когда будешь готов — жми 'Начать'."

# Финальный текст после всех вопросов
FINAL_TEXT = "Спасибо за участие! 💙"

# Список вопросов
QUESTIONS = [
    "1. Если бы вы могли пригласить кого-нибудь на ужин (близкого человека, умершего родственника, знаменитость), кого бы вы выбрали?",
    "2. Хотели бы вы быть знаменитым? В чем?",
    "3. Прежде чем сделать звонок, вам случается репетировать свою реплику? Почему?",
    "4. Каким был бы для вас «идеальный день»?",
    "5. Когда вы в последний раз пели в одиночестве? А для кого-нибудь другого?",
    "6. Если бы вы могли прожить до 90 лет и в последние 60 лет сохранить либо разум, либо тело 30-летнего, что бы вы выбрали?",
    "7. У вас есть тайное предчувствие того, как вы умрете?",
    "8. Назовите три черты, которые, по-вашему, есть и у вас, и у вашего партнера.",
    "9. За что вы испытываете наибольшую благодарность?",
    "10. Если бы вы могли, что бы вы изменили в том, как вас воспитывали?",
    "11. За 4 минуты расскажите партнеру историю вашей жизни настолько подробно, насколько это возможно.",
    "12. Если бы вы могли проснуться завтра, обладая каким-то умением или способностью, что бы это было?",
    "13. Если бы магический кристалл мог открыть вам правду, о чем бы вы хотели узнать?",
    "14. Есть ли что-то, что вы уже давно мечтаете сделать? Почему вы еще не сделали этого?",
    "15. Каково наибольшее достижение вашей жизни?",
    "16. Что в дружбе для вас наиболее ценно?",
    "17. Каково ваше самое дорогое воспоминание?",
    "18. Каково ваше самое ужасное воспоминание?",
    "19. Если бы вы знали, что умрете через год, что бы вы изменили в том, как вы живете? Почему?",
    "20. Что для вас значит дружба?",
    "21. Какую роль любовь и нежность играют в вашей жизни?",
    "22. По очереди называйте партнеру его положительные черты (обменяйтесь пятью характеристиками).",
    "23. В вашей семье отношения теплые и близкие?",
    "24. Какие чувства у вас вызывает ваше взаимодействие с матерью?",
    "25. Составьте каждый по три утверждения, верных для вас обоих. Например: «Мы оба сейчас чувствуем…»",
    "26. Продолжите фразу: «Я бы хотел, чтобы был кто-то, с кем можно разделить…»",
    "27. Если бы вы собирались стать близким другом для вашего партнера, что бы вы ему рассказали: что он, по вашему мнению, должен о вас знать?",
    "28. Расскажите партнеру, что вам нравится в нем; говорите прямо, произносите вещи, которые вы не могли бы сказать случайному знакомому.",
    "29. Поделитесь с вашим парт­нером неприятной ситуацией или смущающим моментом из вашей жизни.",
    "30. Когда вы в последний раз плакали при ком-нибудь? А в одиночестве?",
    "31. Расскажите своему партнеру, что вы уже сейчас цените в нем (в ней).",
    "32. По-вашему, какая тема слишком серьезна, чтобы шутить об этом?",
    "33. Если бы вы должны были умереть сегодня до конца дня, ни с кем не поговорив, о чем несказанном вы бы больше всего жалели? Почему вы еще не сказали этого?",
    "34. Ваш дом со всем имуществом загорелся. После спасения ваших близких, а также домашних животных у вас есть время, чтобы забежать в дом и спасти еще что-то от пламени. Что бы вы взяли? Почему?",
    "35. Смерть кого из членов вашей семьи расстроила бы вас больше всего? Почему?",
    "36. Поделитесь личной проблемой и спросите партнера, как он бы справился с ней. Затем спросите, что он думает о ваших чувствах по поводу этой проблемы."
]

# ==================
# ЛОГИ
# ==================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================
# ОБРАБОТЧИКИ
# ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["index"] = 0
    keyboard = [[InlineKeyboardButton("Начать", callback_data="start_questions")]]
    await update.message.reply_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if "index" not in context.user_data:
        context.user_data["index"] = 0

    if query.data == "start_questions":
        await send_question(query, context)

    elif query.data == "next":
        context.user_data["index"] += 1
        await send_question(query, context)

    elif query.data == "prev":
        context.user_data["index"] -= 1
        await send_question(query, context)

    elif query.data == "finish":
        await query.edit_message_text(FINAL_TEXT, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Restart", callback_data="restart")]
        ]))

    elif query.data == "restart":
        context.user_data["index"] = 0
        await query.edit_message_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Начать", callback_data="start_questions")]
        ]))

    elif query.data == "back_to_start":
        context.user_data["index"] = 0
        await send_question(query, context)


async def send_question(query, context):
    index = context.user_data["index"]

    # Если дошли до конца
    if index >= len(QUESTIONS):
        index = len(QUESTIONS) - 1
        context.user_data["index"] = index

    # Если ушли в минус
    if index < 0:
        index = 0
        context.user_data["index"] = index

    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data="prev"))
    if index < len(QUESTIONS) - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data="next"))
    else:
        buttons.append(InlineKeyboardButton("✅ Завершить", callback_data="finish"))

    # Вторая строка кнопок
    extra_buttons = [
        InlineKeyboardButton("🔄 Restart", callback_data="restart"),
        InlineKeyboardButton("🔙 Вернуться в начало", callback_data="back_to_start")
    ]

    await query.edit_message_text(
        text=QUESTIONS[index],
        reply_markup=InlineKeyboardMarkup([buttons, extra_buttons])
    )

# ==================
# ЗАПУСК
# ==================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("Бот запущен...")
    app.run_polling()
