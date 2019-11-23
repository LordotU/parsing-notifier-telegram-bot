FROM python:3-alpine

WORKDIR /app

RUN apk update && apk upgrade && \
    apk add gcc musl-dev python3-dev libffi-dev openssl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./parsing-notifier.py" ]
