echo "======СОЗДАЁМ И АКТИВИРУЕМ ВИРТУАЛЬНОЕ ОКРУЖЕНИЕ======"
python3 -m venv env
. ./env/bin/activate
echo "======СКАЧИВАЕМ РЕПОЗИТОРИЙ И ПЕРЕХОДИМ В НЕГО======"
git clone "https://github.com/stasyao/moscow_places"
cd moscow_places
echo "======УСТАНАВЛИВАЕМ ЗАВИСИМОСТИ======"
pip install -r requirements.txt
echo "======РАЗВОРАЧИВАЕМ БАЗУ ДАННЫХ======"
python3 manage.py migrate
echo "======ЗАПОЛНЯЕМ БАЗУ ДАННЫХ ЛОКАЦИЯМИ======"
python3 manage.py load_places_from_github https://github.com/devmanorg/where-to-go-places/tree/master/places
echo "======СОЗДАЁМ СУПЕРЮЗЕРА======"
export DJANGO_SUPERUSER_USERNAME="admin"
export DJANGO_SUPERUSER_PASSWORD="admin"
export DJANGO_SUPERUSER_EMAIL="admin@admin.ru"
python3 manage.py createsuperuser --noinput
echo "=====СОЗДАЁМ КОНТЕНТ-МЕНЕДЖЕРА======"
python3 manage.py create_content_manager manager1 manager1
echo "=====ДЕАКТИВИРУЕМ ВИРТУАЛЬНОЕ ОКРУЖЕНИЕ====="
deactivate