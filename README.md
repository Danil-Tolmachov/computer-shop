# Preview:

![2](https://user-images.githubusercontent.com/59608495/202649969-062269ea-c093-4189-8b21-04640c614fdd.PNG)

![3](https://user-images.githubusercontent.com/59608495/202649953-e79bdaec-5a43-451e-8049-ecb60106974d.PNG)

# Overview:
Note: **Don't use it for production. This pet-project and may be too raw to use!**

Stack:
- Python 3.10
- Django
- PostgerSQL
- Docker

Some features:
- Custom user model
- Admin panel for staff
- Delete/add product to card through Ajax requests
- Order system
- Resent viewed products by session or cookies
- Product categories

To do:
- Product filters and search
- Comments and reviews system
- User profile and order tracking pages

# Installation and setup

**1. Clone repository and install requirements**
```sh 
git clone https://github.com/Danil-Tolmachov/ComputerShop/
pip install -r requirements.txt
```
**2. Create .env and setup variables**
```sh
SECRET_KEY=...
DEBUG=TRUE
DATABASE_URL=postgresql://user:password@host:port/db

POSTGRES_DB=...
POSTGRES_USER= ...
POSTGRES_PASSWORD=...
POSTGRES_HOST=...
POSTGRES_PORT=...

SMTP_HOST=...
SMTP_USER=...
SMTP_PASS=...
SMTP_PORT=...
SMTP_USE_TLS=...

CAPTCHA_PUBLIC_KEY=...
CAPTCHA_PRIVATE_KEY=...
```
**3. Run docker compose to create db**
```sh 
docker-compose -f docker-compose.dev.yml run db
```
**3. Run app**
```sh 
cd ComputerShop/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
