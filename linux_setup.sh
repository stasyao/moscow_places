echo "======СОЗДАЁМ И АКТИВИРУЕМ ВИРТУАЛЬНОЕ ОКРУЖЕНИЕ======"
python3 -m venv env
. ./env/bin/activate
echo "======СКАЧИВАЕМ РЕПОЗИТОРИЙ И ПЕРЕХОДИМ В НЕГО======"
git clone "https://github.com/stasyao/dvmn"
cd dvmn
echo "======УСТАНАВЛИВАЕМ ЗАВИСИМОСТИ======"
pip install -r requirements.txt
echo "======РАЗВОРАЧИВАЕМ БАЗУ ДАННЫХ======"
python3 manage.py makemigrations
python3 manage.py migrate
echo "======ЗАПОЛНЯЕМ БАЗУ ДАННЫХ ЛОКАЦИЯМИ======"
python3 manage.py load_places_from_github \
                               devmanorg \
                      where-to-go-places \
                                  places
echo "======СОЗДАЁМ СУПЕРЮЗЕРА======"
export DJANGO_SUPERUSER_USERNAME="super"
export DJANGO_SUPERUSER_PASSWORD="super"
export DJANGO_SUPERUSER_EMAIL="super@super.ru"
python3 manage.py createsuperuser --noinput
echo "=====СОЗДАЁМ АДМИНИСТРАТОРА======"
python3 manage.py create_places_admin admin admin
echo "=====ЗАПУСКАЕМ ЛОКАЛЬНЫЙ СЕРВЕР====="
python3 manage.py runserver
