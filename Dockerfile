FROM python:2.7.9

ADD . /src

RUN cd /src/tutorial && pip install -r requirements.txt
WORKDIR /src/tutorial

CMD ["gunicorn", "-b", "-b 0.0.0.0:8000", "tutorial.app:get_app()"]

EXPOSE 8000
