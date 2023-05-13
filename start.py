import os
import logging
import sys
import time
from typing import Tuple

from dotenv import load_dotenv

from pars_habr import rss_parse_feed
from chat_gpt import generate_chat_completion
from vk_api import vk_wall_post
from tel_bot_error import send_telegram_message

load_dotenv()
api_key: str = os.getenv("AI_TOKEN")
vk_token: str = os.getenv("VK_TOKEN")
group_id: int = int(os.getenv("GROUP_ID"))
bot_token: str = os.getenv("BOT_TOKEN")
chat_id: str = os.getenv("CHAT_ID")

# Отправит сообщение через get запрос в телеграмм
RETRY_PERIOD: int = 30


def check_tokens() -> None:
    """Проверяем наличие токенов."""
    tokens = {
        "api_key": api_key,
        "vk_token": vk_token,
        "group_id": group_id,
        "bot_token": bot_token,
        "chat_id": chat_id,
    }
    missing_tokens = [k for k, v in tokens.items() if not v]
    if missing_tokens:
        logging.critical("Проверьте наличие токенов.")
        sys.exit(f"Проверьте корректность введённых токенов: {missing_tokens}")


def get_post() -> Tuple[str, str]:
    """Получение поста."""
    logging.info("Попытка получение поста.")
    try:
        text = rss_parse_feed()
        logging.debug(f"Пост успешно получен.")
        return text
    except Exception as error:
        logging.error(f"Произошла ошибка при получении поста {error}")
        raise


def text_to_ai(
    text: str,
    api_key: str = api_key,
    humor: bool = True,
    style: bool = False,
) -> str:
    """Преобразование текста."""
    logging.info("Попытка преобразования текста.")
    try:
        modified_text = generate_chat_completion(
            text,
            api_key=api_key,
            humor=humor,
            style=style,
        )
        logging.debug(f"Текст успешно изменен.")
        return modified_text
    except Exception as error:
        logging.error(f"Произошла ошибка при преобразовании текста {error}")
        raise


def post_to_vk(
    message: str,
    vk_token: str = vk_token,
    group_id: int = group_id,
) -> int:
    """Публикация поста."""
    logging.info("Попытка публикации поста.")
    try:
        response = vk_wall_post(
            token=vk_token, message=message, group_id=int(group_id)
        )
        logging.debug(f"Пост успешно опубликован.")
        return response
    except Exception as error:
        logging.error(f"Произошла ошибка при публикации поста {error}")
        raise
def main():
    """Основная логика работы бота."""
    check_tokens()
    post_titles = []
    while True:
        try:
            title, post = get_post()
            if title not in post_titles:
                post_titles.append(title)
                text = text_to_ai(post)
                post_to_vk(text)
            else:
                logging.info("Новые посты не найдены.")
        except Exception as error:
            logging.exception(error)
            message = f"Сбой в работе программы: {error}"
            send_telegram_message(
                bot_token=bot_token, chat_id=chat_id, message=message
            )
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="logging.log",
        format="%(asctime)s, %(levelname)s, %(message)s, %(name)s",
    )
    main()
