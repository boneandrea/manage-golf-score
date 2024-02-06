FROM ghcr.io/railwayapp/nixpacks:ubuntu-1702339400@sha256:1a9c1eed040aacf8f898be048210ef2d3366b1228373c4e6818362bb75611b32

RUN apt update && apt install gpg python3.11 pip -y

RUN apt-get update
ENV TZ=Asia/Tokyo
ENV LANG=en_US.UTF-8
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -yq --no-install-recommends python3-pip \
python3-dev \
curl \
unzip \
tzdata && apt-get upgrade -y && apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Chrome binary
RUN curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
apt-get install -yq --no-install-recommends ./google-chrome-stable_current_amd64.deb && \
apt-get clean && rm google-chrome-stable_current_amd64.deb

# Install Chrome Driver (Get Latest Version)
RUN curl -O https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip && \
mv chromedriver /usr/local/bin/ && \
rm chromedriver_linux64.zip

COPY . /app/backend
WORKDIR /app/backend
RUN pwd
RUN ls
RUN pip install -r requirements.txt


CMD ["gunicorn","main:app"]
