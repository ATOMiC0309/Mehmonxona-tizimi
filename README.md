# Mehmonxona-tizimi
Sodda loyiha, mehmonxona qo'shish, xona qo'shish, xona band qilish(tahrirlash va o'chirish admin panel orqali), sharh va baho qoldirish, to'lov qilish va chek generatsiya qilish(Haqiqiy to'lov tizimi emas), chekni yuklab olish(pdf shaklida)

# 🧩 Django Loyihasi

Bu Django asosidagi web ilova. Quyidagi amallar yordamida loyihani lokal kompyuteringizda ishga tushurishingiz mumkin.

---

## 🔧 O‘rnatish bosqichlari

### 1. Repository-ni klonlash
```bash
git clone https://github.com/ATOMiC0309/Mehmonxona-tizimi
cd Mehmonxona-tizimi
```
### 2. Loyihadagi kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```
### 3. Ma'lumotlar bazasini sozlash(Migratsiyani bajarish)
```bash
python manage.py makemigrations
python manage.py migrate
```
### 4. Superuser (admin) yaratish(Admin panelga kirish uchun)
```bash
python manage.py createsuperuser
```
### 5. 🚀 Loyiha ishga tushirish
```bash
python manage.py runserver
```
### 6. Loyihani ko'zdan kechirish
Loyiha muvaffaqqiyatli ishga tushgandan so'ng quyidagi havolani istalgan brouzerda oching:
```bash
http://127.0.0.1:8000
```
---
# 🔐 Admin panelga kirish
Loyiha ishga tushgach, quyidagi havola orqali admin panelga kirishingiz mumkin:
```bash
http://127.0.0.1:8000/admin
```
-⚠️ Admin panelga kirish uchun oldin createsuperuser orqali yaratilgan foydalanuvchi ma'lumotlari bilan tizimga kiring.

