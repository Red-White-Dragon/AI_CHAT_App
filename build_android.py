import subprocess
import sys
import json
from pathlib import Path

def build_apk():
    """Сборка APK для Android с помощью Flet"""
    print("Установка зависимостей из requirements.txt...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке зависимостей: {e}")
        return

    # Создаём файл конфигурации
    config = {
        "project_name": "AIChat",
        "package_name": "com.example.aichat",
        "version": "1.0.0",
        "build_number": 1,
        "android_min_sdk": 21,
        "assets_dir": "assets",
        "icon": "assets/images/Matrix_blue.png",
        "android_arch": "arm64",
    }
    with open("flet.build.config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("Сборка APK для Android...")
    try:
        subprocess.run(
            ["flet", "build", "apk"],
            check=True,
        )
        print(
            "Сборка APK завершена!\n"
            "Файл находится в директории: build/apk/app-release.apk"
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при сборке APK: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    build_apk()