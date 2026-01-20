# EstateHub Django Backend

## تشغيل المشروع

### المتطلبات

- Python 3.8+
- Django 4.2.7
- Pillow (لرفع الصور)

### التثبيت والتشغيل

1. **تفعيل virtual environment:**

```bash
cd backend
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

1. **تطبيق Migrations (تم بالفعل):**

```bash
python manage.py migrate
```

1. **إنشاء superuser للوصول لـ Admin Panel:**

```bash
python manage.py createsuperuser
```

1. **تشغيل السيرفر:**

```bash
python manage.py runserver
```

1. **الوصول للتطبيق:**

- الموقع الرئيسي: <http://127.0.0.1:8000/>
- Admin Panel: <http://127.0.0.1:8000/admin/>

## البنية

### Models

- **UserProfile**: ملف المستخدم (buyer/seller)
- **Property**: العقارات مع دعم اللغتين
- **PropertyImage**: صور العقارات

### Apps

- **users**: إدارة المستخدمين
- **properties**: إدارة العقار at

## المميزات الحالية

✅ Database Models
✅ Admin Panel
⏳ Forms & Views
⏳ Templates
⏳ Authentication

## الجاهز للإنتاج

- Database schema
- Models مع multilingual support
- Admin panel كامل
