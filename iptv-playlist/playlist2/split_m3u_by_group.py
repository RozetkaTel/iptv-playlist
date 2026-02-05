import os
import re
from pathlib import Path

def sanitize_filename(name):
    """Очищает имя файла от недопустимых символов."""
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

def split_m3u_by_group(input_file='playlist2.m3u', output_dir='split_playlists'):
    # Создаём папку для выходных файлов
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Извлекаем строку #EXTM3U с x-tvg-url (если есть)
    header = '#EXTM3U\n'
    if lines and lines[0].startswith('#EXTM3U'):
        header = lines[0]
        lines = lines[1:]

    # Словарь: group_title -> список строк канала (включая #EXTINF и URL)
    groups = {}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF:'):
            # Извлекаем group-title из строки
            match = re.search(r'group-title="([^"]*)"', line)
            group = match.group(1) if match else 'Uncategorized'
            group = group.strip() or 'Uncategorized'

            # Следующая строка — URL потока
            if i + 1 < len(lines):
                url_line = lines[i + 1].strip()
                # Сохраняем обе строки
                entry = [line + '\n', url_line + '\n']
                groups.setdefault(group, []).extend(entry)
                i += 2
            else:
                # Нет URL — пропускаем
                i += 1
        else:
            # Пропускаем пустые или нерелевантные строки
            i += 1

    # Записываем каждый плейлист в отдельный файл
    for group, entries in groups.items():
        filename = sanitize_filename(group) + '.m3u'
        filepath = out_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header)
            f.writelines(entries)

    print(f"✅ Создано {len(groups)} плейлистов в папке '{output_dir}'.")

if __name__ == '__main__':
    split_m3u_by_group()