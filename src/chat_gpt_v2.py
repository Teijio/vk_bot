import json
import requests


class ChatGenerator:
    def __init__(self, api_key: str = None):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": api_key,
        }

    def generate_completion(
        self,
        text: str,
        temperature: float = 0.7,
        humor: bool = False,
        style: bool = False,
    ) -> str:
        """Generation a completion based on the provided text.

        Args:
            text (str): The input text to be completed.
            temperature (float, optional): Controls the randomness of the output.
            humor (bool, optional): Specifies whether to add humor to the completion.
            style (bool, optional): Specifies whether to rewrite text in specific style.

        Returns:
            str: The generated completion.
        """
        if humor and not style:
            text = (
                f"Возьми {text} и перепиши его в шутливой форме. "
                "Добавь немного юмора и остроумных выражений."
            )
        if style and not humor:
            text = f"Возьми {text} и перепиши его в стиле Жириновского."
        if style and humor:
            text += " В стиле Жириновского."

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
        response = requests.post(
            self.url,
            headers=self.headers,
            data=json.dumps(data),
            timeout=10,
        )
        result = self.extract_result(response)
        return result

    def extract_result(self, response):
        """Extracting result from response."""
        try:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError) as error:
            raise ValueError(
                "Failed to extract result from response."
            ) from error
