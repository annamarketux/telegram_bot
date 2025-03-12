import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Логирование (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Создаем объект бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Вопросы теста (полный список)
questions = [
    "Какой у тебя сейчас уровень усталости и стресса?\n\n"
    "1️⃣ Спокойствие, ресурсное состояние\n"
    "2️⃣ Умеренный стресс, но держусь\n"
    "3️⃣ Усталость и напряжение, срочно нужен отдых",

    "Какой у тебя ведущий сенсорный канал удовольствия?\n\n"
    "1️⃣ Визуальный (красивые интерьеры, природа, эстетика)\n"
    "2️⃣ Аудиальный (музыка, ASMR, звуки природы)\n"
    "3️⃣ Тактильный (теплые пледы, массаж, шелковые простыни)\n"
    "4️⃣ Обонятельный (ароматы, парфюмы, благовония)\n"
    "5️⃣ Вкусовой (изысканная еда, кофе, вино)",

    "Где ты чаще всего черпаешь ресурс?\n\n"
    "1️⃣ В уединении, тишине и природе\n"
    "2️⃣ В компании интересных людей и событий\n"
    "3️⃣ В новых знаниях, обучении, развитии\n"
    "4️⃣ В движении, спорте, активности\n"
    "5️⃣ В творчестве и креативности",

    "Какой формат расслабления тебе больше подходит?\n\n"
    "1️⃣ Медленный, глубокий релакс (ванны, йога, медитации)\n"
    "2️⃣ Динамичный (спорт, прогулки, танцы)\n"
    "3️⃣ Эмоциональный (театр, музыка, кино)\n"
    "4️⃣ Социальный (общение, вечеринки, поездки)",

    "Как ты предпочитаешь начинать утро?\n\n"
    "1️⃣ Медленно и осознанно, с чашкой чая/кофе\n"
    "2️⃣ С музыкой, подкастами или книгой\n"
    "3️⃣ С зарядки, прогулки или растяжки\n"
    "4️⃣ Утро? Я не жаворонок!",

    "Как ты чаще всего снимаешь стресс?\n\n"
    "1️⃣ Вкусной едой или напитками\n"
    "2️⃣ Уходом за телом (ванны, маски, массаж)\n"
    "3️⃣ Музыкой, книгами или кино\n"
    "4️⃣ Разговорами с друзьями или близкими\n"
    "5️⃣ Физической активностью",

    "Какие эмоции у тебя сейчас преобладают?\n\n"
    "1️⃣ Любовь, благодарность, спокойствие\n"
    "2️⃣ Вдохновение, мотивация, азарт\n"
    "3️⃣ Легкая грусть, апатия\n"
    "4️⃣ Напряжение, тревожность",

    "Какой фразой ты бы хотела себя поддержать сейчас?\n\n"
    "1️⃣ Я достойна наслаждения и легкости\n"
    "2️⃣ Я в ресурсе, все сложится наилучшим образом\n"
    "3️⃣ Я позволяю себе заботиться о себе\n"
    "4️⃣ Мне можно расслабиться и отпустить",

    "Какой ритуал ты хотела бы добавить в свою жизнь?\n\n"
    "1️⃣ Утренние и вечерние ритуалы для настроя\n"
    "2️⃣ Время для чтения и саморефлексии\n"
    "3️⃣ Практики расслабления и заботы о теле\n"
    "4️⃣ Развлекательные и творческие активности",

    "Какое удовольствие ты чаще всего запрещаешь себе?\n\n"
    "1️⃣ Полноценный отдых без чувства вины\n"
    "2️⃣ Покупки и баловство без оправданий\n"
    "3️⃣ Время для себя, без заботы о других\n"
    "4️⃣ Дурость, спонтанность, хаос",

    "Представь, что через 30 минут ты получишь свой 'Код наслаждения'. Какой эффект тебе важнее всего?\n\n"
    "1️⃣ Глубокий релакс и перезагрузка\n"
    "2️⃣ Вдохновение и мотивация\n"
    "3️⃣ Чувственность и пробуждение энергии\n"
    "4️⃣ Спокойствие и ощущение заботы"
]

# Хранение ответов пользователей
user_answers = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_answers[user_id] = []
    
    await message.answer("Привет! Давай определим твой Код наслаждения 🌟\nОтвечай на вопросы, выбирая цифры.")
    await ask_question(user_id, 0)

async def ask_question(user_id, index):
    if index < len(questions):
        await bot.send_message(user_id, questions[index])
    else:
        profile = analyze_answers(user_answers[user_id])
        await bot.send_message(user_id, f"✨ Твой Код наслаждения: {profile} ✨")

def analyze_answers(user_answers):
    scores = {"Эстет": 0, "Чувствующий": 0, "Исследователь": 0, "Душа компании": 0, "Создатель баланса": 0}
    
    for answer in user_answers:
        if answer == "1":
            scores["Эстет"] += 1
        elif answer == "2":
            scores["Чувствующий"] += 1
        elif answer == "3":
            scores["Исследователь"] += 1
        elif answer == "4":
            scores["Душа компании"] += 1
        elif answer == "5":
            scores["Создатель баланса"] += 1

    dominant_profile = max(scores, key=scores.get)
    return dominant_profile

@dp.message_handler()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_answers:
        if message.text in ["1", "2", "3", "4", "5"]:
            user_answers[user_id].append(message.text)
            await ask_question(user_id, len(user_answers[user_id]))
        else:
            await message.answer("Пожалуйста, выбери цифру 1-5 для ответа 😉")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
