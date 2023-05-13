import json
import requests
from typing import Optional


def generate_chat_completion(
    text: str,
    api_key: Optional[str] = None,
    temperature: float = 0.7,
    humor: bool = False,
    style: bool = False,
) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key,
    }
    if humor:
        text = (
            f"Возьми {text} и перепиши его в шутливой форме."
            "Добавь немного юмора и остроумных выражений. "
        )
    if style:
        if not humor:
            text = f"Возьми {text} и перепиши его в стиле Жириновского."
        else:
            test += "В стиле Жириновского"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": text,
            }
        ],
        "temperature": temperature,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    return result["choices"][0]["message"]["content"]
