from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
import logging


# Функция для обработки команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет, отправь свои результаты через запятую так: 'минуты:секунды:миллисекунды', 'минуты:секунды:миллисекунды', \n'целое_число'. \nСначала плавание, потом бег, а потом стрельба. Все через запятую и через двоеточия. \nК примеру так: \n2:20:0,\n2:10:0,\n86")


# Функция для обработки входящих сообщений
def calculate_score(update, context):
    data = update.message.text.split(",")

    if len(data) != 3:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Отправь свои результаты через запятую так: 'минуты:секунды:миллисекунды', 'минуты:секунды:миллисекунды', \n'целое_число'. \nСначала плавание, потом бег, а потом стрельба. Все через запятую и через двоеточия. К примеру так: \n2:20:0,\n2:10:0,\n86")
        return

    total_score = 0
    individual_scores = []

    for idx, time_str in enumerate(data):
        time_values = [int(value) for value in time_str.split(":")]

        if len(time_values) == 3:
            seconds = time_values[0] * 60 + time_values[1] + time_values[2]*10 / 1000
            score = 0
            if idx == 0:
                score = 1000 - (seconds - 140) * 10
            elif idx == 1:
                score = 1000 - (seconds - 130) * 15
        else:
            score = 1000 - (86 - time_values[0]) * 24

        total_score += score
        individual_scores.append(score)

    message = f"Твои общие очки: {round(total_score,1)}\n"

    for i, score in enumerate(individual_scores):
        message += f"Значение {data[i].strip()}: {round(score,1)} очков\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


# Функция main, инициализация бота
def main():
    # Токен бота
    token = "7066512281:AAGS92f_7glR00HaST5Grf7E8cqx30bUS6g"

    # Создание экземпляра Updater и передача токена бота
    updater = Updater(token, use_context=True)

    # Получение диспетчера бота
    dp = updater.dispatcher

    # Добавление обработчиков команд и сообщений
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, calculate_score))

    # Старт бота
    updater.start_polling()

    # Ждем завершения работы бота
    updater.idle()
    


# Вызов функции main
if __name__ == '__main__':
    main()
