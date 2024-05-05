import os
import sys
import time
from subprocess import Popen
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    """ Обработчик событий, который перезапускает приложение при изменении файлов Python. """

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'File {event.src_path} has changed, restarting the app...')
            if hasattr(self, 'process') and self.process:
                self.process.kill()  # Завершаем старый процесс перед запуском нового
            self.process = Popen([sys.executable, '-m', 'src'], stdout=sys.stdout, stderr=sys.stderr)


if __name__ == "__main__":
    path = '.'  # Путь к директории, за которой нужно наблюдать
    observer = Observer()
    event_handler = Handler()
    event_handler.process = Popen([sys.executable, '-m', 'src'], stdout=sys.stdout,
                                  stderr=sys.stderr)  # Запуск начального процесса
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("Starting the observer. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.kill()
    observer.join()
