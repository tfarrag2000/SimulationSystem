"""
إعدادات تجريبية سريعة لاختبار النظام
Quick Test Settings for Dr. Tamer
"""

# إعدادات مضمونة للعمل
QUICK_TEST_SETTINGS = {
    "environment": {
        "width": 100,
        "height": 100,
        "num_drones": 20,
        "sensing_radius": 20,
        "num_parking_spots": 50,
        "num_disabled_spots": 5
    },
    
    "algorithms": {
        "greedy": {
            "desired_coverage": 0.8,
            "overlap_weight": 0.1,
            "energy_weight": 0.1
        },
        
        "ga": {
            "population_size": 30,
            "num_generations": 50,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "elitism": 5,
            "desired_coverage": 0.9
        },
        
        "pso": {
            "swarm_size": 25,
            "iterations": 100,
            "inertia": 0.9,
            "cognitive_weight": 2.0,
            "social_weight": 2.0,
            "desired_coverage": 0.9
        }
    },
    
    "stopping_criteria": {
        "target_coverage": 85,  # 85% بدلاً من 95%
        "max_iterations": 100,  # مهم: 100 بدلاً من 5
        "time_limit": 120       # دقيقتين
    }
}

# خطوات الاستخدام المضمونة
USAGE_STEPS = [
    "1. شغل: python run.py",
    "2. افتح: http://127.0.0.1:8050",
    "3. اضبط Environment Settings حسب القيم أعلاه",
    "4. اختر Algorithm: Greedy (للاختبار السريع)",
    "5. اضبط Stopping Criteria: Target=85%, Max Iterations=100",
    "6. اضغط Initialize وانتظر رسالة النجاح",
    "7. اضغط Start وراقب النتائج"
]

print("إعدادات الاختبار السريع جاهزة!")
print("استخدم QUICK_TEST_SETTINGS للحصول على نتائج مضمونة")
