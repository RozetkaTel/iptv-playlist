import requests
import urllib.parse
import subprocess
import sys

def test_stream(url):
    """Проверяет доступность потока"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def get_full_stream_url():
    """Получает полный URL потока"""
    base = "https://tv.balkanweb.com/news24/livestream/"
    relative = "chunks.m3u8?nimblesessionid=507040511"
    full_url = urllib.parse.urljoin(base, relative)
    return full_url

def main():
    full_url = get_full_stream_url()
    print(f"URL потока: {full_url}")
    
    # Проверяем доступность
    print("Проверяем доступность...")
    if test_stream(full_url):
        print("✓ Поток доступен")
    else:
        # Пробуем получить через основной плейлист
        print("Пробуем получить через основной плейлист...")
        try:
            main_playlist = requests.get("https://tv.balkanweb.com/news24/livestream/playlist.m3u8")
            if main_playlist.status_code == 200:
                lines = main_playlist.text.split('\n')
                for line in lines:
                    if line.endswith('.m3u8'):
                        new_url = urllib.parse.urljoin("https://tv.balkanweb.com/news24/livestream/", line)
                        print(f"Найден альтернативный поток: {new_url}")
                        full_url = new_url
                        break
        except:
            pass
    
    # Спрашиваем пользователя
    choice = input("\nВыберите действие:\n1. Воспроизвести (требуется VLC)\n2. Сохранить в файл (требуется ffmpeg)\n3. Создать M3U файл\nВаш выбор: ")
    
    if choice == "1":
        # Воспроизведение через VLC
        try:
            subprocess.run(['vlc', full_url])
        except:
            print("VLC не найден. Установите VLC Player")
    elif choice == "2":
        # Сохранение через ffmpeg
        try:
            subprocess.run(['ffmpeg', '-i', full_url, '-c', 'copy', 'news24_output.mp4'])
        except:
            print("ffmpeg не найден")
    elif choice == "3":
        # Создание M3U файла
        m3u_content = f"""#EXTM3U
#EXTINF:-1,News 24 Albania
{full_url}"""
        with open("news24.m3u", "w") as f:
            f.write(m3u_content)
        print("Файл news24.m3u создан")

if __name__ == "__main__":
    main()