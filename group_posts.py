import requests
import pandas as pd
import time

from dotenv import load_dotenv
import os

from consts import BASE_URL, VERSION
from group_info import get_group_name

load_dotenv()
access_token = os.getenv("TOKEN")

if not access_token:
    raise ValueError("Ошибка: Токен не найден в .env файле.")

group_link = os.getenv("GROUP_URL")
group_domain = get_group_name(group_link)

if group_domain == "":
    raise ValueError("Ошибка: не удалось обнаружить название группы.")

api_url = f"{BASE_URL}wall.get"


def get_text_posts(domain, count, token, limit=None):
    docs = []
    offset = 0

    while True:
        response = requests.get(
            api_url,
            params={
                "access_token": token,
                "v": VERSION,
                "domain": domain,
                "offset": offset,
                "count": count,
                "extended": 1,
            },
        )

        data = response.json()

        if "response" in data:
            posts = data["response"]["items"]
            for post in posts:
                text = post.get("text", "")
                if text == "":
                    continue
                post_data = {
                    "owner_id": post.get("owner_id", ""),
                    "post_id": post.get("id", ""),
                    "text": text,
                    "date": post.get("date", ""),
                    "attachments": post.get("attachments", "Нет данных"),
                    "likes": post.get("likes", {}).get("count", 0),
                    "reposts": post.get("reposts", {}).get("count", 0),
                    "views": post.get("views", {}).get("count", 0),
                }

                attachments = post.get("attachments", [])
                for attachment in attachments:
                    if attachment["type"] == "photo":
                        post_data["image_url"] = attachment["photo"]["sizes"][-1].get(
                            "url", ""
                        )
                    elif attachment["type"] == "doc":
                        post_data["doc_url"] = attachment["doc"].get("url", "")
                        post_data["doc_id"] = attachment["doc"].get("id", "")
                        post_data["doc_title"] = attachment["doc"].get("title", "")
                        post_data["doc_ext"] = attachment["doc"].get("ext", "")
                owner_id = post_data["owner_id"]
                post_id = post_data["post_id"]
                post_data["url"] = f"https://vk.com/wall{owner_id}_{post_id}"
                docs.append(post_data)

            if len(posts) < count:  # Прекращаем, если меньше, чем запрашивали
                break

            offset += count  # Увеличиваем смещение для пагинации
        else:
            print("Ошибка при получении данных:", data)
            break

        time.sleep(2)  # Задержка между запросами, чтобы не превышать лимиты API

        # Если лимит на количество постов превышен, выходим из цикла
        if limit and len(docs) >= limit:
            break

    return docs


all_posts = get_text_posts(group_domain, count=100, token=access_token, limit=None)
raw_df = pd.DataFrame(all_posts)
raw_df.loc[:, "date"] = pd.to_datetime(raw_df["date"], unit="s")
df = raw_df.drop(columns=["owner_id", "attachments"])

df.to_excel("posts.xlsx", index=False)

print("Файл posts.xlsx успешно создан!")
