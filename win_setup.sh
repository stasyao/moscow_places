echo "======СКАЧИВАЕМ РЕПОЗИТОРИЙ И ПЕРЕХОДИМ В НЕГО======"
git clone https://github.com/stasyao/dvmn
cd dvmn
echo "======СОЗДАЕМ ВИРТУАЛЬНОЕ ОКРУЖЕНИЕ======"
python -m venv env
echo "======АКТИВИРУЕМ ВИРТУАЛЬНОЕ ОКРУЖЕНИЕ======"
source env/Scripts/activate
echo "======УСТАНАВЛИВАЕМ ЗАВИСИМОСТИ======"
pip install -r requirements.txt
echo "======РАЗВОРАЧИВАЕМ БАЗУ ДАННЫХ======"
python manage.py makemigrations
python manage.py migrate
echo "======ЗАПОЛНЯЕМ БАЗУ ДАННЫХ ЛОКАЦИЯМИ======"
python manage.py load_places_from_github \
                               devmanorg \
                      where-to-go-places \
                                  places
echo "======СОЗДАЁМ СУПЕРЮЗЕРА======"
export DJANGO_SUPERUSER_USERNAME="super"
export DJANGO_SUPERUSER_PASSWORD="super"
export DJANGO_SUPERUSER_EMAIL="super@super.ru"
python manage.py createsuperuser --noinput
echo "=====СОЗДАЁМ АДМИНИСТРАТОРА======"
python manage.py create_places_admin admin admin
echo "=====ЗАПУСКАЕМ ЛОКАЛЬНЫЙ СЕРВЕР====="
python manage.py runserver