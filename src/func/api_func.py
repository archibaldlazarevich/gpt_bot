import asyncio
import urllib

screen_data = {
    'samsung_a40': [1080, 2340],
    '1280_1024': [1280, 1024],
    '1366_768': [1366, 768],
    '1440_900': [1440, 900],
    '1600_900': [1600, 900],
    '1680_1050': [1680, 1050],
    '1920_1080': [1920, 1200],
    '1920_1200': [1920, 1200],
    '2560_1080': [2560, 1080],
    '2560_1440': [2560, 1440],
    '3440_1440': [3440, 1440],
    '3840_2160': [3840, 2160],
    '4096_2160': [4096, 2160],
    '5120_2880': [5120, 2880],
}
urls = {
    'picture': 'https://image.pollinations.ai/models',
    'text': 'https://text.pollinations.ai/models',
}

async def get_all_picture_models(model_data: str) -> list | None:

    url = urls[model_data]

    try:
        response = requests.get(url)
        response.raise_for_status()
        models_data = response.json()
        if isinstance(models_data, list):
            if model_data == 'text':
                data = [i['name'] for i in models_data]
            else:
                data = [i for i in models_data]
            return data
        else:
            return None
    except Exception:
        return None


    except requests.exceptions.RequestException as e:
        print(f"Error fetching text models: {e}")

asyncio.run(get_all_picture_models('picture'))

async def create_new_picture(user_id : int, text: str, res: str):
    """
    Функция для генерации изображения по промпту

    :param res: тип экрана
    :param user_id: id пользователя в телеграмм
    :param text: текст промпта
    :return:
    """

    monitor_data = screen_data[res]

    # "width": 1280,
    # "height": 720,
    # "seed": 42,
    # "model": "flux",
    # "nologo": "false",
    # "transparent": "true", # Optional - generates transparent background (gptimage model only)
    # "image": "https://example.com/input-image.jpg", # Optional - for image-to-image generation (kontext & gptimage)
    # "referrer": "MyPythonApp" # Optional for referrer-based authentication

    params = {
        "width": monitor_data[0],
        "height": monitor_data[1],
        "seed": 42,
        "model": "flux",
        "nologo": 'true',
    }
    encoded_prompt = urllib.parse.quote(text)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    try:
        response = requests.get(url, params=params, timeout=300)
        response.raise_for_status()

        with open(f'{user_id}.png', 'wb') as f:
            f.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")

async def create_new_text(user_id, text: str):
    """
    Функция для создания текста исходя из промпта (text)
    :param user_id: id пользователя в телеграмм
    :param text: текст промпта
    :return:
    """

    params = {

    }

import requests

