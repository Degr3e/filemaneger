import eel, json
from fs import open_fs
from fs.opener.errors import UnsupportedProtocol
from fs.errors import CreateFailed
import os, sys, shutil
from back.cache_cleaner import WindowsCacheCleaner


@eel.expose    
def get_files(directory):
    fs = open_fs(directory)
    try:
        files = json.dumps([fs.getinfo(f.name, namespaces=['details', 'basic']).raw for f in list(fs.scandir("/"))])
    except (UnsupportedProtocol, CreateFailed) as e:
        return False
    except e:
        print("Произошла ошибка доступа")
        print(e)
        return False
    return files

# unused
def get_all_files(directory):
    fs = open_fs(directory)
    tree = {directory : []}
    for path in list(fs.scandir("/")):
        if path.is_file:
            tree[directory].append(path)
        else:
            tree[directory].append(get_all_files(path.make_path(directory) + "/"))
    return tree

# unused
def get_all_files_from_home(directory):
    fs = open_fs(directory)
    tree = {directory : []}
    for path in fs.walk.files(filter=['*.py']):
        print(path)


# удаляем файлы и папки
@eel.expose
def remove(folder):
    if os.path.isfile(folder):
        os.unlink(folder)
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                return False
        shutil.rmtree(folder)
    return True


@eel.expose
def clear_all_cache():
    print("Начало очистки всего кэша...")
    # Очистка системного кэша
    WindowsCacheCleaner.clear_system_cache()
    print("Системный кэш очищен.")
    # Очистка кэша браузеров
    WindowsCacheCleaner.clear_browser_cache()
    print("Кэш браузеров очищен.")
    # Очистка кэша программ (путь к config_file можно настроить)
    # WindowsCacheCleaner.clear_program_cache(config_file='programs.json')
    # print("Кэш программ очищен.")
    # Очистка корзины
    # WindowsCacheCleaner.clear_recycle_bin()
    # print("Корзина очищена.")
    # Поиск и удаление временных файлов в системной папке Temp
    WindowsCacheCleaner.find_and_remove_temp_files(os.getenv('TEMP'))
    print("Временные файлы удалены.")
    # Поиск и удаление старых медиафайлов (можно настроить число дней)
    WindowsCacheCleaner.find_and_remove_old_media_files(directory="C:\\", days=360)
    print("Старые медиафайлы удалены.")
    # Удаление старых пустых директорий
    WindowsCacheCleaner.clear_old_empty_dirs(path="C:\\", days=180)
    print("Старые пустые директории удалены.")
    print("Очистка всего кэша завершена.")
