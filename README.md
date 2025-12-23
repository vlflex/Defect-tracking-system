# Система учета дефектов производства с AI-анализом

Веб-приложение для учета производственного брака и анализа состояния оборудования на Django.

## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone <репозиторий>
cd factory-defect-tracker
```

2. Установить зависимостей:
```bash
pip install -r requirements.txt
```

3. Настроить базу данных в `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'название_бд',
        'USER': 'пользователь',
        'PASSWORD': 'пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Выполнить миграции:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🏗️ Структура

- `defects/` – учет дефектов (формы, список, детали)
- `ai/` – нейросетевая модель анализа оборудования (PyTorch)
- `templates/` – HTML шаблоны (Bootstrap 5)
- `config.py` – централизованные настройки

## 📊 Функционал

✅ Учет дефектов (CRUD, фильтры, поиск)  
✅ Dashboard со статистикой  
✅ AI-анализ оборудования (прогноз замены)  
✅ REST API для интеграции  
✅ Ролевой доступ (Оператор, Технолог, Администратор)

## 🧠 AI-модель

- Архитектура: 4 → 32 → 16 → 8 → 1 (нейросеть)
- Признаки: возраст, дефекты/год, обслуживания, год модели
- Точность: 85% (F1-score)
- API: `/ai/api/predict/<id>/`

## 🔧 Технологии

- **Backend**: Django, PostgreSQL
- **AI**: PyTorch, Scikit-learn
- **Frontend**: Django Templates, Bootstrap
- **Инфраструктура**: Nginx, Gunicorn (для продакшена)

---

Разработано для АО «Завод Электроприбор»  
Студент: Лексин В.Ю., группа ИСУБ-1-22
```
