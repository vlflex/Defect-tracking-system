import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from pathlib import Path
from datetime import datetime

print("🧪 РАСШИРЕННОЕ ТЕСТИРОВАНИЕ МОДЕЛИ С ПОДРОБНОЙ АНАЛИТИКОЙ")
print("=" * 60)

# 1. Загружаем модель
checkpoint = torch.load('ai/models/dataset_640/perfect_model.pth', map_location='cpu')

# 2. НОВАЯ АРХИТЕКТУРА — ТОЧНО ТАКАЯ ЖЕ, КАК В perfect_train.py!
class PerfectModel(torch.nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(input_size, 32),
            torch.nn.BatchNorm1d(32),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.2),
            
            torch.nn.Linear(32, 16),
            torch.nn.BatchNorm1d(16),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.2),
            
            torch.nn.Linear(16, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 1),
            torch.nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.net(x)

# 3. Создаем модель и загружаем веса
model = PerfectModel(checkpoint['input_size'])
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# ВАЖНО: Загружаем scaler из checkpoint
scaler = checkpoint['scaler']
feature_names = checkpoint.get('feature_names', 
    ['age_years', 'model_year', 'defect_count_last_year', 'maintenance_count_last_year'])

print(f"✅ Модель загружена успешно!")
print(f"   • Accuracy: {checkpoint.get('accuracy', 'N/A'):.4f}")
print(f"   • F1 Score: {checkpoint.get('f1_score', 'N/A'):.4f}")
print(f"   • Признаки: {feature_names}")

# 4. РАСШИРЕННЫЕ ТЕСТОВЫЕ СЦЕНАРИИ (с реальной статистикой)
print("\n📋 РАСШИРЕННЫЕ ТЕСТОВЫЕ СЦЕНАРИИ:")
print("=" * 60)

# Создаем более разнообразные тестовые данные
test_cases_extended = []

# 4.1. Сценарии основанные на реальных статистических распределениях
age_groups = [
    ("НОВОЕ (1-3 года)", lambda: np.random.uniform(1, 3)),
    ("СРЕДНЕЕ (4-8 лет)", lambda: np.random.uniform(4, 8)),
    ("СТАРОЕ (9-15 лет)", lambda: np.random.uniform(9, 15)),
    ("ОЧЕНЬ СТАРОЕ (16-25 лет)", lambda: np.random.uniform(16, 25))
]

for age_name, age_func in age_groups:
    for _ in range(5):  # по 5 примеров для каждой возрастной группы
        age = age_func()
        model_year = 2024 - int(age) + np.random.randint(-2, 3)
        
        # Дефекты зависят от возраста
        base_defects = age * np.random.uniform(0.5, 2.0)
        defect_count = max(0, int(base_defects + np.random.normal(0, 5)))
        
        # Обслуживания обратно пропорциональны дефектам
        maintenance_count = max(0, int(np.random.uniform(0, 6) - defect_count/15))
        
        test_cases_extended.append({
            'description': f"{age_name} - Пример {_+1}",
            'features': [age, model_year, defect_count, maintenance_count],
            'age_group': age_name,
            'age': age,
            'defects': defect_count,
            'maintenance': maintenance_count,
            'model_year': model_year
        })

# 4.2. Крайние случаи и граничные условия
edge_cases = [
    ("ИДЕАЛЬНЫЙ СЛУЧАЙ", [2.0, 2022, 1, 4]),
    ("КАМЕННЫЙ ВЕК", [25.0, 1995, 60, 0]),
    ("ПРОБЛЕМНОЕ НОВОЕ", [1.5, 2023, 40, 2]),
    ("СТАРОЕ НО УХОЖЕННОЕ", [20.0, 2000, 10, 6]),
    ("НОВОЕ БЕЗ ОБСЛУЖИВАНИЯ", [3.0, 2021, 25, 0]),
    ("СРЕДНЕЕ СРЕДНЕЕ", [10.0, 2014, 15, 2]),
    ("ВЫСОКИЙ РИСК", [12.0, 2012, 38, 1]),
    ("НИЗКИЙ РИСК", [8.0, 2016, 5, 3])
]

for desc, features in edge_cases:
    test_cases_extended.append({
        'description': desc,
        'features': features,
        'age_group': 'ГРАНИЧНЫЕ',
        'age': features[0],
        'defects': features[2],
        'maintenance': features[3],
        'model_year': features[1]
    })

# 5. МАССОВОЕ ТЕСТИРОВАНИЕ
print(f"\n🧮 Тестируем {len(test_cases_extended)} разнообразных сценариев...")
results_extended = []

for case in test_cases_extended:
    features = case['features']
    
    # Масштабируем
    test_scaled = scaler.transform([features])  # Теперь scaler определен!
    
    # Предсказание
    with torch.no_grad():
        tensor = torch.tensor(test_scaled, dtype=torch.float32)
        prediction = model(tensor).item()
    
    decision = "ЗАМЕНИТЬ" if prediction > 0.5 else "НЕ МЕНЯТЬ"
    confidence = prediction * 100 if decision == "ЗАМЕНИТЬ" else (1 - prediction) * 100
    
    results_extended.append({
        **case,
        'decision': decision,
        'confidence': confidence,
        'probability': prediction,
        'risk_level': 'ВЫСОКИЙ' if prediction > 0.7 else 
                     'СРЕДНИЙ' if prediction > 0.3 else 'НИЗКИЙ'
    })

# 6. РАСШИРЕННЫЙ АНАЛИЗ
print("\n" + "=" * 60)
print("📊 РАСШИРЕННЫЙ АНАЛИЗ РЕШЕНИЙ МОДЕЛИ:")
print("=" * 60)

# Статистика по решениям
results_df = pd.DataFrame(results_extended)
replace_count = (results_df['decision'] == 'ЗАМЕНИТЬ').sum()
keep_count = len(results_df) - replace_count

print(f"Всего протестировано: {len(results_df)} сценариев")
print(f"Рекомендовано заменить: {replace_count} ({replace_count/len(results_df)*100:.1f}%)")
print(f"Рекомендовано оставить: {keep_count} ({keep_count/len(results_df)*100:.1f}%)")

# Анализ по возрастным группам
print("\n📈 АНАЛИЗ ПО ВОЗРАСТНЫМ ГРУППАМ:")
age_analysis = results_df.groupby('age_group').agg({
    'probability': 'mean',
    'decision': lambda x: (x == 'ЗАМЕНИТЬ').sum(),
    'age': 'mean',
    'defects': 'mean'
}).round(2)

print(age_analysis.to_string())

# 7. РАСШИРЕННАЯ ВИЗУАЛИЗАЦИЯ
print("\n🎨 СОЗДАНИЕ РАСШИРЕННЫХ ГРАФИКОВ...")
os.makedirs('ai/results', exist_ok=True)

# Создаем папку для графиков если её нет
os.makedirs('ai/results', exist_ok=True)

# Упрощенная визуализация для начала
fig = plt.figure(figsize=(15, 10))

# 7.1. Основная диаграмма рассеяния
ax1 = fig.add_subplot(2, 2, 1)
scatter = ax1.scatter(
    results_df['age'], 
    results_df['defects'], 
    c=results_df['probability'],
    cmap='RdYlGn_r',
    s=100,
    alpha=0.8,
    edgecolor='black'
)
ax1.set_xlabel('Возраст (лет)')
ax1.set_ylabel('Дефекты за год')
ax1.set_title('Возраст vs Дефекты (цвет - вероятность замены)')
plt.colorbar(scatter, ax=ax1, label='Вероятность замены')
ax1.grid(True, alpha=0.3)

# 7.2. Распределение вероятностей
ax2 = fig.add_subplot(2, 2, 2)
ax2.hist(results_df['probability'], bins=15, alpha=0.7, color='steelblue', edgecolor='black')
ax2.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Порог решения (0.5)')
ax2.set_xlabel('Вероятность замены')
ax2.set_ylabel('Количество сценариев')
ax2.set_title('Распределение вероятностей модели')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 7.3. Анализ решений по возрастным группам
ax3 = fig.add_subplot(2, 2, 3)
age_groups_plot = results_df.groupby('age_group')['probability'].mean()
x = range(len(age_groups_plot))
bars = ax3.bar(x, age_groups_plot.values, alpha=0.7, color='lightcoral', edgecolor='black')
ax3.set_xticks(x)
ax3.set_xticklabels(age_groups_plot.index, rotation=45, ha='right')
ax3.set_ylabel('Средняя вероятность замены')
ax3.set_title('Вероятность замены по возрастным группам')
ax3.axhline(0.5, color='red', linestyle='--', alpha=0.5)

# Добавляем значения на столбцы
for i, v in enumerate(age_groups_plot.values):
    ax3.text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=10)

# 7.4. Влияние обслуживания
ax4 = fig.add_subplot(2, 2, 4)
scatter4 = ax4.scatter(
    results_df['maintenance'], 
    results_df['probability'],
    c=results_df['age'],
    cmap='viridis',
    s=80,
    alpha=0.7
)
ax4.set_xlabel('Количество обслуживаний')
ax4.set_ylabel('Вероятность замены')
ax4.set_title('Влияние обслуживания на решение')
plt.colorbar(scatter4, ax=ax4, label='Возраст (лет)')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ai/results/extended_model_analysis.png', dpi=150, bbox_inches='tight')
print("✅ Расширенные графики сохранены: ai/results/extended_model_analysis.png")

# 8. ДЕТАЛЬНЫЙ ТЕКСТОВЫЙ ОТЧЕТ
report_path = 'ai/results/detailed_test_report.txt'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("ДЕТАЛЬНЫЙ ОТЧЕТ ПО ТЕСТИРОВАНИЮ МОДЕЛИ ИИ\n")
    f.write("="*70 + "\n\n")
    f.write(f"Дата тестирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Модель: perfect_model.pth\n")
    f.write(f"Точность модели: {checkpoint.get('accuracy', 'N/A'):.4f}\n")
    f.write(f"F1 Score модели: {checkpoint.get('f1_score', 'N/A'):.4f}\n\n")
    
    f.write("СТАТИСТИКА ТЕСТИРОВАНИЯ:\n")
    f.write("-"*50 + "\n")
    f.write(f"Всего сценариев: {len(results_df)}\n")
    f.write(f"Рекомендовано к замене: {replace_count} ({replace_count/len(results_df)*100:.1f}%)\n")
    f.write(f"Рекомендовано оставить: {keep_count} ({keep_count/len(results_df)*100:.1f}%)\n\n")
    
    f.write("АНАЛИЗ ПО ВОЗРАСТНЫМ ГРУППАМ:\n")
    f.write("-"*50 + "\n")
    f.write(age_analysis.to_string() + "\n\n")
    
    f.write("ТОП-5 САМЫХ РИСКОВАННЫХ СЦЕНАРИЕВ:\n")
    f.write("-"*50 + "\n")
    top_risky = results_df.nlargest(5, 'probability')
    for idx, row in top_risky.iterrows():
        f.write(f"{row['description']}:\n")
        f.write(f"  Вероятность: {row['probability']:.4f} | ")
        f.write(f"Возраст: {row['age']:.1f} лет | ")
        f.write(f"Дефекты: {row['defects']} | ")
        f.write(f"Обслуживания: {row['maintenance']}\n")
    
    f.write("\nТОП-5 САМЫХ НАДЕЖНЫХ СЦЕНАРИЕВ:\n")
    f.write("-"*50 + "\n")
    top_safe = results_df.nsmallest(5, 'probability')
    for idx, row in top_safe.iterrows():
        f.write(f"{row['description']}:\n")
        f.write(f"  Вероятность: {row['probability']:.4f} | ")
        f.write(f"Возраст: {row['age']:.1f} лет | ")
        f.write(f"Дефекты: {row['defects']} | ")
        f.write(f"Обслуживания: {row['maintenance']}\n")
    
    f.write("\nВЫВОДЫ И РЕКОМЕНДАЦИИ:\n")
    f.write("-"*50 + "\n")
    
    # Автоматические выводы
    avg_prob = results_df['probability'].mean()
    std_prob = results_df['probability'].std()
    
    f.write(f"• Средняя вероятность замены: {avg_prob:.2f}\n")
    f.write(f"• Стандартное отклонение: {std_prob:.2f}\n")
    
    if avg_prob > 0.5:
        f.write("• Модель в среднем СКЛОННА рекомендовать замену оборудования\n")
    else:
        f.write("• Модель в среднем СКЛОННА рекомендовать продолжение эксплуатации\n")
    
    if std_prob > 0.3:
        f.write("• Модель показывает ВЫСОКУЮ вариативность решений\n")
    else:
        f.write("• Модель показывает УМЕРЕННУЮ вариативность решений\n")
    
    # Анализ возрастной зависимости
    young_mask = results_df['age'] < 5
    old_mask = results_df['age'] > 15
    
    if young_mask.any():
        young_avg = results_df[young_mask]['probability'].mean()
        f.write(f"• Для молодого оборудования (<5 лет) средняя вероятность: {young_avg:.2f}\n")
    
    if old_mask.any():
        old_avg = results_df[old_mask]['probability'].mean()
        f.write(f"• Для старого оборудования (>15 лет) средняя вероятность: {old_avg:.2f}\n")

print(f"✅ Детальный отчет сохранён: {report_path}")

# 9. КРАТКИЙ СВОДНЫЙ ОТЧЕТ НА ЭКРАН
print("\n" + "=" * 60)
print("📋 СВОДНЫЙ ОТЧЕТ:")
print("=" * 60)
print(f"Всего протестировано сценариев: {len(results_df)}")
print(f"К замене: {replace_count} ({replace_count/len(results_df)*100:.1f}%)")
print(f"К эксплуатации: {keep_count} ({keep_count/len(results_df)*100:.1f}%)")
print(f"\nСредняя вероятность замены: {results_df['probability'].mean():.2f}")
print(f"Стандартное отклонение: {results_df['probability'].std():.2f}")

print("\n🎯 РАСПРЕДЕЛЕНИЕ ПО РИСКОВЫМ УРОВНЯМ:")
risk_dist = results_df['risk_level'].value_counts()
for level, count in risk_dist.items():
    print(f"  {level}: {count} ({count/len(results_df)*100:.1f}%)")

print("\n📊 СОЗДАННЫЕ ФАЙЛЫ:")
print(f"  • Графики: ai/results/extended_model_analysis.png")
print(f"  • Отчет: {report_path}")

print("\n" + "=" * 60)
print("🎉 РАСШИРЕННОЕ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
print("=" * 60)