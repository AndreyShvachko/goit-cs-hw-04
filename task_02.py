import os
from multiprocessing import Process, Queue

# Функція для пошуку ключових слів у файлі
def search_keywords(file_list, keywords, results):
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        results.put((file_path, keyword))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# Основна функція
def main():
    # Задати список файлів і ключові слова
    directory = "/Users/andreyshvachko/Woolf/HW/goit-cs/goit-cs-hw-04"
    keywords = ["Peugeot", "Quadrifoglio", "Jeep", "Vectra", "Grand Cherokee", "Sahara", "Berlingo", "C3", "159", "Corsa", "Wagoneer"]
    file_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

    # Черга для результатів
    results = Queue()

    # Кількість процесів
    num_processes = 4
    chunk_size = len(file_list) // num_processes

    # Список процесів
    processes = []
    for i in range(num_processes):
        chunk = file_list[i*chunk_size:(i+1)*chunk_size] if i < num_processes - 1 else file_list[i*chunk_size:]
        process = Process(target=search_keywords, args=(chunk, keywords, results))
        processes.append(process)
        process.start()

    # Чекати завершення всіх процесів
    for process in processes:
        process.join()

    # Вивести результати
    while not results.empty():
        file_path, keyword = results.get()
        print(f"Keyword '{keyword}' found in {file_path}")

if __name__ == "__main__":
    main()
