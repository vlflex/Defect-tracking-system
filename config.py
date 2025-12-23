from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@dataclass(frozen=True)
class ServerSetting:
    IP = "127.0.0.1"
    PORT = 8000
    DEBUG = True
    COMPANY_WEBSITE = "https://www.elpri-rele.ru/"
    COMPANY_NAME = "АО «Завод Электроприбор»"
    
@dataclass(frozen=True)
class WebsiteSettings:
    SITE_NAME = "Система учета производственных дефектов"
    VERSION = "2.0"
    DESCRIPTION = "Автоматизированная система анализа оборудования и учета дефектов"
    
    @dataclass(frozen=True)
    class Navbar:
        HOME = "Главная"
        DEFECTS = "Учет дефектов"
        AI = "AI Анализ"
        ADMIN = "Администрирование"
        
    @dataclass(frozen=True)
    class Pages:
        MAIN_TITLE = "Система учета дефектов производства"
        DEFECTS_TITLE = "Учет и анализ производственных дефектов"
        AI_TITLE = "AI-анализ состояния оборудования"
        
    @dataclass(frozen=True)
    class Footer:
        COPYRIGHT = "© 2025 АО «Завод Электроприбор». Все права защищены."
        CONTACT_EMAIL = "info@elpri-rele.ru"
        CONTACT_PHONE = "+7 (XXX) XXX-XX-XX"

@dataclass(frozen=True)
class DatabaseSettings:
    @dataclass(frozen=True)
    class Generation:
        # МИНИМАЛЬНЫЕ значения для быстрой генерации
        EQUIPMENT_COUNT = 30
        BATCH_COUNT = 50
        DEFECT_COUNT = 5000
        MAINTENANCE_MIN = 1
        MAINTENANCE_MAX = 3
        PRODUCTION_YEARS = 2
        
        # Вероятности дефекта по годам (реалистично)
        DEFECT_PROB_BY_YEAR = {
            (2000, 2005): (0.35, 0.40),
            (2005, 2010): (0.25, 0.30),
            (2010, 2015): (0.15, 0.20),
            (2015, 2020): (0.05, 0.10)
        }

@dataclass(frozen=True)
class AISettings:
    @dataclass(frozen=True)
    class Paths:
        AI_DIR = BASE_DIR / "ai"
        MODELS_DIR = AI_DIR / "models"
        DATA_DIR = AI_DIR / "data"
        
        MODEL_FILE = MODELS_DIR / "perfect_model_enhanced.pth"
        DATASET_FILE = DATA_DIR / "dataset.csv"
        FEATURES_FILE = DATA_DIR / "features.csv"
    
    @dataclass(frozen=True)
    class Training:
        EPOCHS = 20
        BATCH_SIZE = 32
        LEARNING_RATE = 0.001
        HIDDEN_SIZE = 16
        DROPOUT = 0.2
        DECISION_THRESHOLD = 0.5
        
    @dataclass(frozen=True)
    class Features:
        PRIMARY = ['age_years', 'model_year', 'defect_count_last_year', 'maintenance_count_last_year']
        SECONDARY = ['production_rate', 'downtime_hours', 'repair_cost']
        
    @dataclass(frozen=True)
    class Pages:
        MAIN_TITLE = "AI Анализ состояния оборудования"
        CHECK_EQUIP_TITLE = "Проверка оборудования"
        MODEL_INFO_TITLE = "Информация о модели"

@dataclass(frozen=True)
class DefectsSettings:
    @dataclass(frozen=True)
    class Pages:
        MAIN_TITLE = "Учет производственных дефектов"
        FORM_TITLE = "Форма ввода дефекта"
        LIST_TITLE = "Список дефектов"
        
    @dataclass(frozen=True)
    class Validation:
        MAX_COMMENT_LENGTH = 1000
        MIN_WORKER_TAB_LENGTH = 3
        MAX_WORKER_TAB_LENGTH = 20

@dataclass(frozen=True)
class PathSettings:
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_ROOT = BASE_DIR / "media"
    TEMPLATES_DIR = BASE_DIR / "templates"
    LOGS_DIR = BASE_DIR / "logs"
    
@dataclass(frozen=True)
class SecuritySettings:
    SESSION_TIMEOUT = 3600  # 1 час
    MAX_LOGIN_ATTEMPTS = 5
    PASSWORD_MIN_LENGTH = 8
    REQUIRE_HTTPS = False  # Для разработки
    
@dataclass(frozen=True)
class UIConfig:
    PRIMARY_COLOR = "#007bff"
    SECONDARY_COLOR = "#6c757d"
    SUCCESS_COLOR = "#28a745"
    DANGER_COLOR = "#dc3545"
    WARNING_COLOR = "#ffc107"
    INFO_COLOR = "#17a2b8"
    
    CARD_BORDER_RADIUS = "12px"
    BUTTON_BORDER_RADIUS = "8px"
    NAVBAR_HEIGHT = "70px"
    FOOTER_HEIGHT = "60px"
    
    @dataclass(frozen=True)
    class Fonts:
        PRIMARY = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        SECONDARY = "Arial, Helvetica, sans-serif"
        SIZE_BASE = "16px"
        SIZE_SMALL = "14px"
        SIZE_LARGE = "18px"
        
@dataclass(frozen=True)
class DashboardSettings:
    @dataclass(frozen=True)
    class Charts:
        WORKSHOP_STATS_LIMIT = 5
        DEFECT_TYPE_STATS_LIMIT = 5
        EQUIPMENT_STATS_LIMIT = 5
        DAYS_HISTORY = 7
        
    @dataclass(frozen=True)
    class Colors:
        PRIMARY = "#007bff"
        SUCCESS = "#28a745"
        WARNING = "#ffc107"
        DANGER = "#dc3545"
        INFO = "#17a2b8"
        
    @dataclass(frozen=True)
    class Cache:
        DASHBOARD_CACHE_TIMEOUT = 300