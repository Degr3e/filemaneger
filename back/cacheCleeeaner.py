import os
import shutil
import json
import glob
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime, timedelta
from hashlib import md5

class CacheCleaner(ABC):
    @abstractmethod
    def clear_system_cache(self):
        pass

    @abstractmethod
    def clear_browser_cache(self):
        pass

    @abstractmethod
    def clear_program_cache(self, config_file):
        pass

    @abstractmethod
    def clear_recycle_bin(self):
        pass

    @abstractmethod
    def find_and_remove_duplicates(self, directory):
        pass

    @abstractmethod
    def find_and_remove_temp_files(self, directory):
        pass

    @abstractmethod
    def find_and_remove_old_media_files(self, directory, days):
        pass


class WindowsCacheCleaner(CacheCleaner):
    def __init__(self):
        self.system_cache_paths = [os.path.join(os.getenv('LOCALAPPDATA'), 'Temp')]
        self.browser_cache_paths = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Mozilla', 'Firefox', 'Profiles')
        ]

    def clear_cache(self, paths):
        for path in paths:
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                    print(f"Кэш очищен: {path}")
                except Exception as e:
                    print(f"Ошибка при очистке кэша {path}: {e}")
            else:
                print(f"Путь {path} не найден.")

    def clear_system_cache(self):
        """Очистка системного кэша."""
        self.clear_cache(self.system_cache_paths)

    def clear_browser_cache(self):
        """Очистка кэша браузеров."""
        self.clear_cache(self.browser_cache_paths)

    def clear_program_cache(self, config_file='programs.json'):
        """Очистка кэша программ из файла конфигурации."""
        if not os.path.exists(config_file):
            print(f"Файл конфигурации {config_file} не найден.")
            return

        with open(config_file, 'r') as f:
            program_paths = json.load(f)

        for program, paths in program_paths.items():
            print(f"Очистка кэша программы: {program}")
            self.clear_cache(paths)

    def clear_recycle_bin(self):
        """Очистка корзины (только для Windows)."""
        try:
            os.system("rd /s /q %systemdrive%\\$Recycle.Bin")
            print("Корзина очищена.")
        except Exception as e:
            print(f"Ошибка при очистке корзины: {e}")

    def find_and_remove_duplicates(self, directory):
        """Поиск и удаление дубликатов файлов в указанной папке."""
        file_hashes = {}
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.get_file_hash(file_path)
                if file_hash in file_hashes:
                    os.remove(file_path)
                    print(f"Удален дубликат: {file_path}")
                else:
                    file_hashes[file_hash] = file_path

    @staticmethod
    def get_file_hash(file_path):
        hash_md5 = md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def find_and_remove_temp_files(self, directory):
        """Поиск и удаление временных файлов, например, text (1).txt."""
        temp_files = glob.glob(os.path.join(directory, '*(*).txt'))
        for file_path in temp_files:
            os.remove(file_path)
            print(f"Удален временный файл: {file_path}")

    def find_and_remove_old_media_files(self, directory, days=180):
        """Поиск и удаление старых медиафайлов (по умолчанию старше 180 дней)."""
        threshold_date = datetime.now() - timedelta(days=days)
        media_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mp3', '.mov']
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in media_extensions):
                    file_path = os.path.join(root, file)
                    file_age = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_age < threshold_date:
                        os.remove(file_path)
                        print(f"Удален старый медиа-файл: {file_path}")

    def clear_cache(self, paths):
        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    # Удаление файлов
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            os.remove(file_path)
                            print(f"Файл удален: {file_path}")
                        except PermissionError:
                            print(f"Файл занят и не может быть удален: {file_path}")
                        except Exception as e:
                            print(f"Ошибка при удалении файла {file_path}: {e}")
                    # Удаление пустых директорий
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        try:
                            os.rmdir(dir_path)
                            print(f"Директория удалена: {dir_path}")
                        except OSError:  # Если папка не пустая
                            pass
                        except Exception as e:
                            print(f"Ошибка при удалении директории {dir_path}: {e}")
            else:
                print(f"Путь {path} не найден или еще не создан.")

    def clear_old_empty_dirs(self, path, days=30):
        """Удаление пустых директорий старше определенного количества дней."""
        dirs_deleted = 0
        threshold_date = datetime.now() - timedelta(days=days)

        for root, dirs, _ in os.walk(path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    if os.path.isdir(dir_path) and not os.listdir(dir_path):  # Проверяем, что папка пустая
                        creation_time = datetime.fromtimestamp(os.path.getctime(dir_path))
                        if creation_time < threshold_date:
                            os.rmdir(dir_path)
                            dirs_deleted += 1
                            print(f"Старая пустая папка удалена: {dir_path}")
                except Exception as e:
                    print(f"Ошибка при удалении директории {dir_path}: {e}")

        print(f"Общее количество удаленных старых пустых директорий: {dirs_deleted}")


    def clear_system_cache(self):
        """Очистка системного кэша."""
        self.clear_cache(self.system_cache_paths)
        
if __name__ == "__main__":
    cleaner = WindowsCacheCleaner()
    cleaner.find_and_remove_duplicates("C:/Users/Gleb77/Downloads")