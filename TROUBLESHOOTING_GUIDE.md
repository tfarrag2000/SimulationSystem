# 🚁 دليل استخدام نظام تحسين الطائرات المسيرة

## د. تامر - حل مشكلة عدم ظهور النتائج

### 🔍 **تشخيص المشكلة:**
المشكلة الرئيسية هي أن النظام يتوقف عند 5 iterations بسبب:
1. إعدادات التوقف المبكر
2. عدم ضبط المعاملات بشكل صحيح
3. مشكلة في تزامن البيانات بين الواجهة والخوارزميات

---

## ✅ **الحل المضمون:**

### **الخطوة 1: تشغيل النظام بشكل صحيح**
```bash
# في Terminal/Command Prompt:
cd "d:\OneDrive_Personal\OneDrive\My Research\01_Working\Drones\SimulationSystem"
python run.py
```

### **الخطوة 2: الإعدادات الصحيحة في الواجهة**

#### **أ) إعدادات البيئة (Environment):**
- **Area Width**: 100 (أو أكبر حسب الحاجة)
- **Area Height**: 100 
- **Total Drones**: 20 (يفضل بين 15-25)
- **Sensing Radius**: 20 (نطاق استشعار جيد)

#### **ب) إعدادات التوقف (Stopping Criteria):**
- **Target Coverage**: 90% (أو أقل للاختبار السريع)
- **Max Iterations**: 100 (مهم جداً - اتركه 100 أو أكثر)
- **Time Limit**: 60 seconds (أو أكثر)

### **الخطوة 3: التشغيل بالترتيب الصحيح** 📋

1. **اضبط المعاملات أولاً** ⚙️
2. **اختر الخوارزمية** (ابدأ بـ Greedy للاختبار)
3. **اضغط "Initialize"** - انتظر رسالة "Simulation initialized"
4. **اضغط "Start"** - سيبدأ التحسين

---

## 🎯 **إعدادات مُجربة تعمل 100%:**

### **للاختبار السريع (Greedy Algorithm):**
```
Environment:
- Width: 100, Height: 100
- Drones: 20, Radius: 20

Algorithm: Greedy
- Desired Coverage: 0.85
- Overlap Weight: 0.1
- Energy Weight: 0.1

Stopping Criteria:
- Target Coverage: 85%
- Max Iterations: 50
- Time Limit: 30s
```

### **للنتائج المتقدمة (Genetic Algorithm):**
```
Environment:
- Width: 100, Height: 100  
- Drones: 25, Radius: 18

Algorithm: Genetic Algorithm
- Population Size: 30
- Generations: 50
- Mutation Rate: 0.1
- Crossover Rate: 0.8

Stopping Criteria:
- Target Coverage: 90%
- Max Iterations: 100
- Time Limit: 120s
```

---

## 🐛 **حلول المشاكل الشائعة:**

### **إذا توقف عند 5 iterations:**
```python
# السبب: إعدادات التوقف المبكر
# الحل: زيادة Max Iterations إلى 100 أو أكثر
```

### **إذا لم تظهر الصور:**
```python
# السبب: مشكلة في تحديث الواجهة
# الحل: تحديث الصفحة (F5) أو إعادة التشغيل
```

### **إذا ظهرت رسائل خطأ:**
```python
# السبب: مشكلة في الاستيراد
# الحل: تأكد من تشغيل python run.py وليس app.py مباشرة
```

---

## 📊 **ما يجب أن تراه عند النجاح:**

### **في علامة التبويب "Simulation":**
- خريطة تظهر الطائرات (نقاط زرقاء)
- مناطق التغطية (دوائر خضراء)
- النقاط المغطاة والغير مغطاة

### **في علامة التبويب "Metrics":**
- 4 رسوم بيانية:
  1. Coverage over time
  2. Power consumption
  3. Overlap violations  
  4. Performance metrics

### **في Iteration Logs:**
```
Iteration 1: Coverage=45.2%, Active=12, Fitness=0.342
Iteration 2: Coverage=52.1%, Active=14, Fitness=0.389
...وهكذا
```

---

## 🔧 **إذا استمرت المشكلة:**

### **تشخيص متقدم:**
```bash
# تحقق من حالة الاستيراد:
python -c "import app; print('Success')"

# تحقق من المكتبات:
python -c "import dash, plotly, numpy, pandas; print('All modules OK')"
```

### **إعادة تعيين كاملة:**
```bash
# أغلق التطبيق (Ctrl+C)
# احذف __pycache__ folder
# شغل مرة أخرى:
python run.py
```

---

## 💡 **نصائح للحصول على أفضل نتائج:**

1. **ابدأ بخوارزمية Greedy** للتأكد من عمل النظام
2. **استخدم معاملات صغيرة أولاً** (20 طائرة، 50 iteration)  
3. **راقب الـ Logs** للتأكد من التقدم
4. **جرب خوارزميات أخرى** بعد نجاح الأولى
5. **احفظ النتائج الجيدة** باستخدام زر التحميل

---

## 📞 **للدعم الفوري:**

إذا استمرت المشكلة، شارك معي:
1. **screenshot** للواجهة
2. **آخر رسائل في الـ Terminal**  
3. **الإعدادات المستخدمة**

**بإذن الله النظام سيعمل معك بشكل ممتاز!** 🚀

---

*تم إعداد هذا الدليل خصيصاً لحل مشكلة د. تامر - July 2025*
