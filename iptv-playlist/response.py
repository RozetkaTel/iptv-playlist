import requests
from urllib.parse import urljoin

# URL основного плейлиста
main_url = "https://tv.balkanweb.com/news24/livestream/playlist.m3u8"

# Получаем основной плейлист
response = requests.get(main_url)
if response.status_code != 200:
    print(f"Ошибка загрузки: {response.status_code}")
    exit()

# Разбиваем на строки
lines = response.text.strip().split('\n')
result = []

# Обрабатываем каждую строку
for line in lines:
    if line.startswith('#') or not line.strip():
        # Комментарии и пустые строки оставляем как есть
        result.append(line)
    elif line.endswith('.m3u8'):
        # Преобразуем относительный путь в абсолютный URL
        absolute_url = urljoin(main_url, line)
        result.append(absolute_url)
    else:
        # Остальные строки оставляем без изменений
        result.append(line)

# Выводим результат
print("\n".join(result))

# Сохраняем в файл (опционально)
with open("complete_playlist.m3u8", "w", encoding="utf-8") as f:
    f.write("\n".join(result))
print("\n\nРезультат сохранен в файл complete_playlist.m3u8")