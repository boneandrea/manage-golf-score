FROM ghcr.io/railwayapp/nixpacks:ubuntu-1702339400@sha256:1a9c1eed040aacf8f898be048210ef2d3366b1228373c4e6818362bb75611b32

RUN apt update && apt install gpg python3.11 pip -y
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrom-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/googlechrom-keyring.gpg
RUN apt update && apt install google-chrome-stable -y

ENV PATH="/usr/local/bin:/opt/venv/bin:${PATH}"
RUN mkdir /app
COPY . /app/backend
WORKDIR /app/backend
RUN pwd
RUN ls
RUN pip install -r requirements.txt
RUN google-chrome --version

CMD ["gunicorn","main:app"]
