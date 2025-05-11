import requests
import re

from consts import BASE_URL, VERSION

api_url = f"{BASE_URL}groups.getById"


def get_group_name(group_link: str) -> str:
    match = re.search(r"[^/]+$", group_link)
    if match:
        return match.group(0)
    return ""


def get_group_id(group_link: str, access_token: str) -> int:
    group_name = get_group_name(group_link)
    params = {"group_ids": group_name, "access_token": access_token, "v": VERSION}

    response = requests.get(api_url, params=params)
    data = response.json()

    if "response" in data:
        group_id = data["response"]["groups"][0]["id"]
        return int(group_id)
    else:
        print("Ошибка при получении ID группы:", data)
        return int(0)
