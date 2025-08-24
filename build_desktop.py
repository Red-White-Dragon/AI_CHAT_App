# Импортируем необходимые стандартные библиотеки Python
import os  # Для работы с операционной системой
import sys  # Для доступа к системным параметрам и функциям
import shutil  # Для операций с файлами и директориями
import subprocess  # Для запуска внешних процессов
from pathlib import Path  # Для удобной работы с путями файловой системы
import glob  # Для поиска файлов и папок по шаблону
import argparse


def clean_build():
    """Очищает временные файлы"""
    for folder in ["bin", "build", "dist", "exports", "logs"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    if os.path.exists("chat_cache.db"):
        os.remove("chat_cache.db")
    # Удаляем все .spec файлы в текущей директории
    for spec_file in glob.glob("*.spec"):
        if os.path.exists(spec_file):
            os.remove(spec_file)
    print("Успешно очищено!")


def build_windows():
    """Сборка исполняемого файла для Windows с помощью PyInstaller"""
    if sys.platform.startswith("win"):
        print("Сборка исполняемого файла для Windows...")

        # Устанавливаем зависимости проекта для Windows из файла requirements.txt
        # sys.executable - путь к текущему интерпретатору Python
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )

        # Создаём директорию bin, если она не существует
        # exist_ok=True позволяет не выбрасывать ошибку, если директория уже существует
        bin_dir = Path("bin")
        bin_dir.mkdir(exist_ok=True)

        # Запускаем PyInstaller со следующими параметрами:
        # --onefile: создать один исполняемый файл
        # --windowed: запускать без консольного окна
        # --name: задать имя выходного файла
        # --clean: очистить кэш PyInstaller перед сборкой
        # --noupx: не использовать UPX для сжатия
        # --uac-admin: запрашивать права администратора при запуске
        subprocess.run(
            [
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--name=AI_Chat",
                "--clean",
                "--noupx",
                "--uac-admin",
                "--icon=assets/images/Matrix_blue.ico",
                "--add-data",
                "assets;assets/",
                "--add-data",
                "src;src/",
                "--paths=./src",
                "--hidden-import=api.openrouter",
                "--hidden-import=pages.starting_page",
                "--hidden-import=pages.registration_page",
                "--hidden-import=pages.entrance_page",
                "--hidden-import=pages.interface_page",
                "--hidden-import=ui.app_style",
                "--hidden-import=ui.components",
                "--hidden-import=utils.app_analytics",
                "--hidden-import=utils.app_cache",
                "--hidden-import=utils.app_logger",
                "--hidden-import=utils.app_monitor",
                "--hidden-import=utils.app_tools",
                "main.py",
            ],
            check=True,
        )
    else:
        print("Неподдерживаемая платформа")
        return

    # Перемещаем собранный файл в директорию bin
    # Используем try/except для обработки возможных ошибок при перемещении
    try:
        shutil.move("dist/AI_Chat.exe", "bin/AI_Chat.exe")
        # Удаляем папки dist и build после успешного перемещения
        shutil.rmtree("dist")
        shutil.rmtree("build")
        
        # Удаляем все spec-файлы в текущей директории
        for file in os.listdir("."):
            if file.endswith(".spec"):
                os.remove(file)
        print(
            "Сборка для Windows завершена! Расположение исполняемого файла: bin/AI_Chat.exe"
        )
    except Exception as e:
        print(f"Ошибка при перемещении или очистке: {e}")
        print(
            "Сборка для Windows завершена! Расположение исполняемого файла: dist/AI_Chat.exe"
        )


def build_linux():
    """Сборка исполняемого файла для Linux с помощью PyInstaller"""
    if sys.platform.startswith("linux"):
        print("Сборка исполняемого файла для Linux...")

        # Устанавливаем зависимости проекта
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )

        # Создаём директорию bin, если она не существует
        bin_dir = Path("bin")
        bin_dir.mkdir(exist_ok=True)

        # Запускаем PyInstaller для Linux
        subprocess.run(
            [
                "pyinstaller",
                "--onefile",
                "--name=AI_Chat",
                "--clean",
                "--noupx",
                "--icon=assets/images/Matrix_blue.ico",
                "--add-data=assets:assets",
                "--add-data=src:src",
                "--paths=./src",
                "--hidden-import=api.openrouter",
                "--hidden-import=pages.starting_page",
                "--hidden-import=pages.registration_page",
                "--hidden-import=pages.entrance_page",
                "--hidden-import=pages.interface_page",
                "--hidden-import=ui.app_style",
                "--hidden-import=ui.components",
                "--hidden-import=utils.app_analytics",
                "--hidden-import=utils.app_cache",
                "--hidden-import=utils.app_logger",
                "--hidden-import=utils.app_monitor",
                "--hidden-import=utils.app_tools",
                "main.py",
            ],
            check=True,
        )
    else:
        print("Неподдерживаемая платформа (требуется Linux)")
        return

    # Перемещаем собранный файл и очищаем временные файлы
    try:
        # Для Linux исполняемый файл будет просто AI_Chat (без .exe)
        shutil.move("dist/AI_Chat", "bin/AI_Chat")
        shutil.rmtree("dist", ignore_errors=True)
        shutil.rmtree("build", ignore_errors=True)

        # Удаляем spec-файлы
        for file in os.listdir("."):
            if file.endswith(".spec"):
                os.remove(file)

        print("Сборка для Linux завершена! Расположение исполняемого файла: bin/AI_Chat")
    except Exception as e:
        print(f"Ошибка при перемещении или очистке: {e}")
        print("Сборка для Linux завершена! Расположение исполняемого файла: dist/AI_Chat")


def main():
    """Основная функция сборки

    Определяет операционную систему и запускает соответствующую функцию сборки
    """
    parser = argparse.ArgumentParser(
        description="Скрипт для сборки приложения в исполняемый файл (.exe для Windows, бинарник для Linux).",
        epilog="""
        Примеры использования:
        python build.py --clean                     # Очистить временные файлы и папки
        python build.py --windows                   # Собрать только для Windows (только на Windows)
        python build.py --linux                     # Собрать только для Linux (только на Linux)
        python build.py                             # Очистка + сборка под текущую ОС
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Удалить папки build, dist, bin и временные файлы",
    )
    parser.add_argument(
        "--windows",
        action="store_true",
        help="Собрать исполняемый файл (.exe) только для Windows. Работает только на Windows!",
    )
    parser.add_argument(
        "--linux",
        action="store_true",
        help="Собрать исполняемый файл (бинарник) только для Linux. Работает только на Linux!",
    )
    args = parser.parse_args()

    if args.clean:
        clean_build()
    elif args.windows:
        build_windows()
    elif args.linux:
        build_linux()
    else:
        clean_build()  # Очистка перед сборкой
        # Проверяем тип операционной системы
        if sys.platform.startswith("win"):  # Если Windows
            build_windows()
        elif sys.platform.startswith("linux"):  # Если Linux
            build_linux()
        else:  # Если другая ОС
            print("Неподдерживаемая платформа")


# Точка входа в скрипт
# Если скрипт запущен напрямую (не импортирован как модуль),
# то запускаем основную функцию
if __name__ == "__main__":
    main()
