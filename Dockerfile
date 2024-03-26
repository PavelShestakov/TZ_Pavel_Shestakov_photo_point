FROM python:3.11.5


SHELL ["bin/bash", "-c"]

#запрещает контейнеру создавать файлы с кэшем
ENV PYTHONDONTWHITEBYTECODE 1
#запрещает буферизировать сообщения с логами и ошибками
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

#Устанавливает пакеты линукса необхожитмые для работы провекта.
#RUN apt update && apt -qy install ...

#создаем нового пользователя и выдаем права на директории
RUN useradd -rms /bin/bash test_username && chmod 777 /opt /run

#указываем рабочую директорию внутри контейнера
WORKDIR /test_dir

#Создаем папки дляхранения статика и медиа джанги. тут же содаются все нужные директории для проекта
#и меняем права на чтение и запись основной директории
RUN mkdir /test_dir/static && mkdir /test_dir/media && chown -R test_username:test_username /test_dir && cdmod 755 /test_dir

#Копируем файлы из локального компьютера внутрь контейнера. Владелец файлов меняется на test_username и из текущей дир . все файлы копируются в текущую cd диреторию .
COPY --chown=test_username:test_username . .

#Установка зависимостей из requirements.txt
RUN pip install -r requirements.txt

#переключаемся на нащего пользователя
USER test_username

#Выполняем команду запуска проекта.
CMD ["gunicorn", "-b", "0.0.0.0:8001", "soaqaz.wsgi:application"]