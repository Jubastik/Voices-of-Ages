# Voices-of-Ages

![Demo GIF](https://github.com/Jubastik/Voices-of-Ages/blob/main/docs/Voices-of-Ages.gif)

### Рабочий бот в TG: [@Voices_of_Ages_bot](https://t.me/VoicesOfAges_bot)

Спасибо Hugging Face) 
## Описание проекта

Voices-of-Ages - инструмент для погружения в историю через речь выдающихся исторических личностей. Бот использует RVC v2 с голосами исторических деятелей, таких как Эйзенхауэр, Горбачев, Ленин и другие. Способен обрабатывать ваши голосовые сообщения, так же есть функция TTS.

## Установка

### Предварительные требования

- Python 3.12
- Docker и Docker Compose

### Клонирование репозитория

```bash
git clone https://github.com/Jubastik/Voices-of-Ages.git
cd Voices-of-Ages
```

### Настройка

1. Создайте и заполните файл `.env` на основе `.env.example`:

```dotenv
BOT_TOKEN=your_bot_token
BOT_ADMIN_ID=your_admin_id
BOT_REDIS_URL=redis://localhost:6363/0
BOT_GRADIO_URL=Jubastik/rvc_zero
```

### Запуск с Docker Compose

```bash
docker-compose up --build
```

### Запуск для разработки с поддержкой перезапуска

Для разработки и тестирования с поддержкой перезапуска при изменении файлов используйте скрипт `dev_start.py`:

```bash
poetry install
```

```
Запустите Redis
```

```bash
python dev_start.py
```

## Использование

После запуска бота, вы можете отправить голосовое сообщение или текст в Telegram, и бот преобразует это в голосовое
сообщение с интонацией выбранного исторического деятеля.

### Доступные голоса

- **Эйзенхауэр**
- **Горбачев**
- **Хрущев**
- **Ленин**
- **Пучков**
- **Сталин (радио версия)**
- **Сталин**
- **Ельцин**
- **Шарль де Голль**

### Модели и файлы

- Файлы моделей хранятся
  отдельно: [Historical Voices on Hugging Face](https://huggingface.co/Jubastik/Historical_voices)
- Модель: [rvc_zero](https://huggingface.co/spaces/Jubastik/rvc_zero)

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной:

- Telegram: [@fohan](https://t.me/fohan)
