# e6homework
 
Для запуска клонируете в папку коммандой:
git clone https://github.com/KznRkjp/e6homework.git

затем делаем контейнер:
sudo docker build -t flask_in_docker_e6:v0.3 .

и запускаем его в бэкграунде: 

sudo docker run -p 8081:8081 flask_in_docker_e6:v0.3

затем создаем конфигурацию для nginx:

sudo nano /etc/nginx/sites-available/e6_homework_flask

и прописываем в ней: 
server {
    listen 8080;
    server_name 89.208.211.24;

    location = /favicon.ico { access_log off; log_not_found off; }
    location / {
        proxy_pass http://127.0.0.1:8081;
    }

}

затем делаем симлинк:
sudo ls -s /etc/nginx/sites-available/e6_homework_flask /etc/nginx/sites-enabled/e6_homework_flask

и перегружаем nginx:
sudo service nginx restart

приложение доступно по вдресу вашей машины на порту 8080



