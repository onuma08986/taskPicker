FROM python:3.10.2

ENV PYTHONUNBUFFERED 1          # 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONDONTWRITEBYTECODE 1   # キャッシュファイルを作成しない

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
