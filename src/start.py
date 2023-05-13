import os
import logging
import sys
import time
from typing import Tuple

from dotenv import load_dotenv

import exceptions
from pars_habr import rss_parse_feed
from chat_gpt_v2 import ChatGenerator
from vk_api import vk_wall_post
from telegram_message import send_telegram_message

load_dotenv()
api_key: str = os.getenv("AI_TOKEN")
vk_token: str = os.getenv("VK_TOKEN")
group_id: str = os.getenv("GROUP_ID")
bot_token: str = os.getenv("BOT_TOKEN")
chat_id: str = os.getenv("CHAT_ID")

RETRY_PERIOD: int = 1800


def check_tokens() -> None:
    """Tokens check."""
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
    """Getting post."""
    logging.info("Trying to get post.")
    try:
        text = rss_parse_feed()
        logging.debug(f"Post is changed successfully.")
        return text
    except exceptions.PostGettingException as error:
        logging.error(f"An error occurred while receiving post {error}")
        raise


def text_to_ai(
    text: str,
    api_key: str = api_key,
    humor: bool = True,
    style: bool = True,
) -> str:
    """Text transformation."""
    logging.info("Trying to convert text.")
    try:
        generator = ChatGenerator(api_key=api_key)
        modified_text = generator.generate_completion(
            text,
            humor=humor,
            style=style,
        )
        logging.debug(f"Text is converted successfully.")
        return modified_text
    except exceptions.TextConvertException as error:
        logging.error(f"An error occurred while converting text {error}")
        raise


def post_to_vk(
    message: str,
    vk_token: str = vk_token,
    group_id: int = int(group_id),
) -> int:
    """Publish a post."""
    logging.info("Trying to publish a post.")
    try:
        response = vk_wall_post(
            token=vk_token, message=message, group_id=int(group_id)
        )
        logging.debug(f"Post successfully published.")
        return response
    except exceptions.PostException as error:
        logging.error(f"An error occurred while publishing post{error}")
        raise


def main():
    """Base logic."""
    check_tokens()
    post_titles = set()
    while True:
        try:
            item_data = get_post()
            title, post = item_data.title, item_data.data
            if title not in post_titles:
                post_titles.add(title)
                text = text_to_ai(post)
                post_to_vk(text)
            else:
                logging.info("New posts are not found.")
        except Exception as error:
            logging.exception(error)
            message = f"Program crash: {error}"
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
