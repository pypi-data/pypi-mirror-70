from functools import partial

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from quiz_bots import settings
from quiz_bots.bots_helpers import send_message_to_tg_chat
from quiz_bots.quiz_helpers import get_clean_text_of_answer
from quiz_bots.redis_utils import (
    get_answer_to_last_question_of_user,
    get_last_asked_question_from_redis,
    get_random_question,
    save_last_asked_question_to_redis,
)

BUTTON_NEW_QUESTION = 'Новый вопрос'
BUTTON_GIVE_IN = 'Сдаться'
BUTTON_SCORE = 'Мой счет'
BUTTON_QUESTION_IS_MADE_INCORRECTLY = 'Вопрос составлен неверно'

CHOOSING, WAIT_ANSWER = range(2)


def welcome_message(update, context):
    """Sends a welcome message to the chat when the bot starts."""
    first_name = update.message.from_user.first_name
    message_text = f'Приветствую, {first_name}! Для старта нажмите кнопку "Новый вопрос"'
    custom_keyboard = [[BUTTON_NEW_QUESTION]]
    send_message_to_tg_chat(
        update,
        message_text,
        custom_keyboard,
    )

    return CHOOSING


def handle_new_question_request(redis_client, update, context) -> int:
    """Sends a random question to the user."""
    question = get_random_question(redis_client)

    if context.user_data.get('button_give_in_flag'):
        custom_keyboard = [
            [BUTTON_GIVE_IN, BUTTON_SCORE],
            [BUTTON_QUESTION_IS_MADE_INCORRECTLY],
        ]
    else:
        custom_keyboard = [
            [BUTTON_GIVE_IN, BUTTON_SCORE],
        ]
    send_message_to_tg_chat(
        update,
        question.replace('\n', ' '),
        custom_keyboard,
    )

    save_last_asked_question_to_redis(
        question=question,
        user_id=update.message.from_user.id,
        redis_client=redis_client,
        social_network='tg',
    )

    return WAIT_ANSWER


def handle_solution_attempt(redis_client, update, context):
    """Checks answer of user."""
    last_asked_question = get_last_asked_question_from_redis(
        redis_client=redis_client,
        user_id=update.message.from_user.id,
        social_network='tg',
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_client=redis_client,
        last_asked_question=last_asked_question,
    )
    clean_answer = get_clean_text_of_answer(answer_to_last_question_of_user)
    if update.message.text.lower() == clean_answer:
        message_text = 'Правильно! Для следующего вопроса нажми «Новый вопрос»'
        custom_keyboard = [[BUTTON_NEW_QUESTION]]
    else:
        message_text = 'Неправильно... Попробуешь ещё раз?'
        custom_keyboard = [[BUTTON_GIVE_IN, BUTTON_SCORE]]

    send_message_to_tg_chat(
        update,
        message_text,
        custom_keyboard,
    )

    return CHOOSING


def handle_opportunity_to_give_in(redis_client, update, context):
    """Handles clicking the "Give in" button.

    The bot sends the user an answer to the question
    and sends the next question with the next message.
    """
    last_asked_question = get_last_asked_question_from_redis(
        redis_client=redis_client,
        user_id=update.message.from_user.id,
        social_network='tg',
    )
    answer_to_last_question_of_user = get_answer_to_last_question_of_user(
        redis_client=redis_client,
        last_asked_question=last_asked_question,
    )
    send_message_to_tg_chat(
        update,
        answer_to_last_question_of_user,
    )
    context.user_data['button_give_in_flag'] = True

    handle_new_question_request(redis_client, update, context)

    return WAIT_ANSWER


def handler_question_is_incorrect(update, context):  # noqa: WPS226
    """Handles clicking the button 'The question is incorrect'."""
    custom_keyboard = [[BUTTON_GIVE_IN, BUTTON_SCORE]]
    send_message_to_tg_chat(
        update,
        'Спасибо за фидбек! Ждем ответ на предыдущий вопрос!',
        custom_keyboard,
    )
    return WAIT_ANSWER


def cancel(update, context):
    """Sends a message to the chat when the bot finish work."""
    first_name = update.message.from_user.first_name
    message_text = f'Спасибо за участие в викторине, {first_name}!'
    custom_keyboard = [[BUTTON_NEW_QUESTION]]
    send_message_to_tg_chat(
        update,
        message_text,
        custom_keyboard,
    )
    return ConversationHandler.END


def start_tg_bot(args, redis_client):
    """Launch the TG bot."""
    updater = Updater(settings.tg_token, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', welcome_message)],

        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^Новый вопрос$'),
                    partial(handle_new_question_request, redis_client),
                ),
                MessageHandler(
                    Filters.regex('^Сдаться$'),
                    partial(handle_opportunity_to_give_in, redis_client),
                ),
            ],
            WAIT_ANSWER: [
                MessageHandler(
                    Filters.regex('^Сдаться$'),
                    partial(handle_opportunity_to_give_in, redis_client),
                ),
                MessageHandler(
                    Filters.regex('^Вопрос составлен неверно$'),
                    handler_question_is_incorrect,
                ),
                MessageHandler(
                    Filters.text,
                    partial(handle_solution_attempt, redis_client),
                ),
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
