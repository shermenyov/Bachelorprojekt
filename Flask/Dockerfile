FROM python:3.7.6

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

# RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
