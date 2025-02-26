# for Railway.app
FROM ghcr.io/railwayapp/nixpacks:ubuntu-1702339400@sha256:1a9c1eed040aacf8f898be048210ef2d3366b1228373c4e6818362bb75611b32

RUN apt update && apt install gpg python3.11 pip -y

ENV LANG=ja_JP.UTF-8
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install -y --no-install-recommends python3-pip python3-dev curl unzip tzdata libnss3-dev \
libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 -y libcups2 libdrm-dev libxkbcommon-x11-0 \
libxcomposite-dev libxdamage1 libxrandr2 libgbm-dev libpangocairo-1.0-0 libasound2 nginx

RUN ln -s /usr/bin/python3.10 /usr/bin/python

COPY ./backend /app
WORKDIR /app

ENV PATH="/usr/local/bin:/opt/venv/bin:${PATH}"
RUN pip install -U pip && pip install --use-pep517 -r requirements.txt
CMD ["gunicorn","main:app"]
