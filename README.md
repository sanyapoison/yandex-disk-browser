# Яндекс.Диск Браузер

Веб-приложение на Flask для просмотра, фильтрации и скачивания файлов с Яндекс.Диска по публичной ссылке.

---

## Функционал

1. **Просмотр файлов и папок** по публичной ссылке.
2. **Навигация по вложенным папкам.**
3. **Фильтрация файлов по типу:**
    - Документы (`.doc`, `.docx`, `.pdf`, `.txt`).
    - Изображения (`.jpg`, `.jpeg`, `.png`, `.gif`).
4. **Скачивание нескольких файлов одновременно** в виде ZIP-архива.
5. **Кэширование списка файлов** для уменьшения количества запросов к API Яндекс.Диска.

---

## Установка и запуск

### 1. Склонируйте репозиторий

```bash
git clone https://github.com/your-repo/yandex-disk-browser.git
cd yandex-disk-browser
```

### 2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
```

### 2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустите приложение

```bash
python app.py
```

Приложение будет доступно по адресу http://127.0.0.1:5000/.