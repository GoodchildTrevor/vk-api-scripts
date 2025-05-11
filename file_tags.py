import requests
import pandas as pd
import time

from dotenv import load_dotenv
import os

from consts import BASE_URL, VERSION
from group_info import get_group_id

load_dotenv()
access_token = os.getenv("TOKEN")
group_link = os.getenv("GROUP_URL")

if not access_token:
    raise ValueError("Ошибка: Токен не найден в .env файле.")

api_url = f"{BASE_URL}docs.get"
group_id = get_group_id(group_link, access_token)

if group_id == 0:
    raise ValueError("Ошибка: не удалось обнаружить id группы.")


def get_file_list_with_tags(group_id, count, access_token, limit=None):
    docs = []
    offset = 0
    while True:
        response = requests.get(
            api_url,
            params={
                "access_token": access_token,
                "v": VERSION,
                "owner_id": -group_id,
                "offset": offset,
                "count": count,
                "return_tags": 1,
            },
        )
        data = response.json()

        if "response" in data:
            docs_batch = data["response"]["items"]
            docs.extend(docs_batch)
            if len(docs_batch) < count:  # Прекращаем, если меньше, чем запрашивали
                break
            offset += count
        else:
            print("Ошибка при получении данных:", data)
            break
        # Кулдаун
        time.sleep(2)
        # Если поставили лимит, то обрываем цикл на его достижении
        if limit and len(docs) >= limit:
            break

    return docs


documents = get_file_list_with_tags(group_id, count=1000, access_token=access_token)

raw_df = pd.DataFrame(documents)
df = raw_df[["id", "title", "ext", "date", "url", "tags"]]

for line in range(len(df)):
    # Приводим даты и тэги в нормальный вид
    df.loc[line, "date"] = pd.to_datetime(df.loc[line, "date"], unit="s")

    if isinstance(df.loc[line, "tags"], list):
        df.loc[line, "tags"] = ", ".join(df.loc[line, "tags"])
    else:
        df.loc[line, "tags"] = str(df.loc[line, "tags"])

df.to_excel("documents.xlsx", index=False)

print("Файл documents.xlsx успешно создан!")
