import threading
import os
from queue import Queue

# Функція для пошуку ключових слів у файлі
def search_keywords(file_path, keywords, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    print(f"Ключове слово '{keyword}' знайдено у файлі {file_path}")
                    results.put((file_path, keyword))
                    
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Функція-потік
def worker(file_list, keywords, results):
    for file_path in file_list:
        search_keywords(file_path, keywords, results)

# Основна функція
def main():
    # Задати список файлів і ключові слова
    directory = "/Users/andreyshvachko/Woolf/HW/goit-cs/goit-cs-hw-04" 
    keywords = ["Peugeot", "Quadrifoglio", "Jeep", "Wrangler", "Sahara", "Grand Cherokee", "opel", "Vectra", "Berlingo"]
    file_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

    # Створити чергу для результатів
    results = Queue()

    # Кількість потоків
    num_threads = 4
    chunk_size = len(file_list) // num_threads

    # Список потоків
    threads = []
    for i in range(num_threads):
        chunk = file_list[i*chunk_size:(i+1)*chunk_size] if i < num_threads - 1 else file_list[i*chunk_size:]
        thread = threading.Thread(target=worker, args=(chunk, keywords, results))
        threads.append(thread)
        thread.start()

    # Чекати завершення всіх потоків
    for thread in threads:
        thread.join()

    # Вивести результати
    while not results.empty():
        file_path, keyword = results.get()
        print(f"Keyword '{keyword}' found in {file_path}")

if __name__ == "__main__":
    main()