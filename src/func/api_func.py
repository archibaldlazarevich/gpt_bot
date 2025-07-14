import urllib

import requests

from src.config.config import POLLINATIONS_TOKEN

urls = {
    "picture": "https://image.pollinations.ai/models",
    "text": "https://text.pollinations.ai/models",
}


async def get_all_picture_models(model_data: str) -> list | None:
    """
    Функция по получению данный от API по всем доступным
    моделям для генерации изображнеий
    :param model_data: тип моделей text для текстовых, picture для изображний
    :return:
    """

    url = urls[model_data]

    try:
        response = requests.get(url)
        response.raise_for_status()
        models_data = response.json()
        if isinstance(models_data, list):
            if model_data == "text":
                data = [i["name"] for i in models_data]
            else:
                data = [i for i in models_data]
            return data
        else:
            return None
    except Exception:
        return None


async def create_new_picture(user_id: int, text: str, res: tuple, model: str):
    """
    Функция для генерации изображения по промпту

    :param model: тип модели
    :param res: тип экрана
    :param user_id: id пользователя в телеграмм
    :param text: текст промпта
    :return:
    """
    params = {
        "width": res[0],
        "height": res[1],
        "seed": 42,
        "model": model,
        "nologo": "true",
        "token": POLLINATIONS_TOKEN,
    }
    encoded_prompt = urllib.parse.quote(text)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    try:
        response = requests.get(url, params=params, timeout=300)
        response.raise_for_status()
        with open(f"{user_id}.png", "wb") as f:
            f.write(response.content)
        return True

    except requests.exceptions.RequestException:
        return False


async def create_new_text(text: str, model: str) -> str:
    """
    Функция для создания текста исходя из промпта (text)
    :param model: модель AI
    :param text: текст промпта
    :return:
    """

    params: dict = {
        "model": model,
        "seed": 42,
        "token": POLLINATIONS_TOKEN,
    }
    encoded_prompt = urllib.parse.quote(text)

    url = f"https://text.pollinations.ai/{encoded_prompt}"
    query_params = {k: v for k, v in params.items() if k != "system"}

    try:
        response = requests.get(url, params=query_params)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException:
        return "Выберите другую модель ИИ, с текущей возникли проблемы."


async def create_new_audio(user_id, text: str):
    """
    Модель для создания аудиопроизведений по тексту
    :param user_id: id телеграма
    :param text: текстовый запрос к api для формирования аудиозаписи
    :return:
    """
    output_filename = f"{user_id}.mp3"

    encoded_text = urllib.parse.quote(text)
    url = f"https://text.pollinations.ai/{encoded_text}"
    params = {
        "model": "openai-audio",
        "voice": "echo",
        "token": POLLINATIONS_TOKEN,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        if "audio/mpeg" in response.headers.get("Content-Type", ""):
            with open(output_filename, "wb") as f:
                f.write(response.content)
            return True

        else:
            return False

    except requests.exceptions.RequestException:
        return False
