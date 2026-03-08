import os
from groq import Groq
from dotenv import load_dotenv
from config import LANGS

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
client = Groq(api_key=API_KEY)


def translate(
    text: str,
) -> str:
    system_message = {
        "role": "system",
        "content": (
            f"You are a translation assistant. Translate the following from "
            f"{LANGS[0]} to {LANGS[1]} or vice versa. Respond **only** "
            "with the translated text—no notes, explanations, examples, or formatting."
        ),
    }
    user_message = {"role": "user", "content": text}
    chat_completion = client.chat.completions.create(
        messages=[system_message, user_message],
        model=LLM_MODEL,
    )
    translation = chat_completion.choices[0].message.content
    return translation


if __name__ == "__main__":
    sample_en = "Hello, how are you today?"
    sample_de = "Hallo, wie geht's dir heute?"
    print("Test (EN -> DE):\t", translate(sample_en))
    print("Test (DE -> EN):\t", translate(sample_de))
