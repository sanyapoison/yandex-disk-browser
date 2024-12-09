from flask import Flask, render_template, request, send_file, redirect, url_for
import requests
import os
from io import BytesIO
import zipfile
from typing import List

app = Flask(__name__)

# Кэш для хранения списка файлов
file_cache = {}

YANDEX_DISK_PUBLIC_API_URL = "https://cloud-api.yandex.net/v1/disk/public/resources"

def fetch_files_from_yandex(public_key: str, path: str = '') -> List[dict]:
    """Получить список файлов по публичной ссылке."""
    cache_key = (public_key, path)
    if cache_key in file_cache:
        return file_cache[cache_key]

    params = {
        "public_key": public_key,
        "path": path
    }
    response = requests.get(YANDEX_DISK_PUBLIC_API_URL, params=params)

    if response.status_code == 200:
        items = response.json().get('_embedded', {}).get('items', [])
        file_cache[cache_key] = items
        return items
    else:
        response.raise_for_status()

def filter_files(files: List[dict], file_type: str) -> List[dict]:
    """Фильтрует файлы по указанному типу."""
    if file_type == "documents":
        extensions = ['.doc', '.docx', '.pdf', '.txt']
    elif file_type == "images":
        extensions = ['.jpg', '.jpeg', '.png', '.gif']
    else:
        return files  # Без фильтрации
    return [file for file in files if any(file['name'].lower().endswith(ext) for ext in extensions)]

@app.route('/', methods=['GET', 'POST'])
def index():
    public_key = request.args.get('public_key', '')
    path = request.args.get('path', '')
    file_type = request.args.get('file_type', '')
    files = []

    if public_key:
        try:
            files = fetch_files_from_yandex(public_key, path)
            if file_type:
                files = filter_files(files, file_type)
        except Exception as e:
            return f"Ошибка: {e}", 400

    return render_template('index.html', files=files, public_key=public_key, current_path=path, file_type=file_type)

@app.route('/download', methods=['GET'])
def download_file():
    public_key = request.args.get('public_key')
    file_path = request.args.get('file_path')

    params = {
        "public_key": public_key,
        "path": file_path,
    }
    response = requests.get(YANDEX_DISK_PUBLIC_API_URL, params=params)

    if response.status_code == 200:
        download_url = response.json().get('file')
        file_response = requests.get(download_url)
        return send_file(BytesIO(file_response.content), download_name=os.path.basename(file_path), as_attachment=True)
    else:
        return f"Ошибка загрузки файла: {response.status_code}", 400

@app.route('/download-multiple', methods=['POST'])
def download_multiple():
    public_key = request.form.get('public_key')
    file_paths = request.form.getlist('file_paths')

    if not file_paths:
        return "Выберите файлы для загрузки", 400

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in file_paths:
            params = {
                "public_key": public_key,
                "path": file_path,
            }
            response = requests.get(YANDEX_DISK_PUBLIC_API_URL, params=params)
            if response.status_code == 200:
                download_url = response.json().get('file')
                file_response = requests.get(download_url)
                zip_file.writestr(os.path.basename(file_path), file_response.content)
            else:
                return f"Ошибка загрузки файла: {file_path}", 400

    zip_buffer.seek(0)
    return send_file(zip_buffer, download_name="selected_files.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
