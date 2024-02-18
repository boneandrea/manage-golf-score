# for Railway.app
FROM nginx:latest

RUN apt update && apt install curl gpg apache2-utils -y

# install node21
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_21.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt update && apt install nodejs -y && node -v

COPY ./frontend /app
WORKDIR /app
ARG BASIC_AUTH_PASSWORD
ARG BASIC_AUTH_USERNAME
ENV VITE_API_ROOT=https://backend-dev-0c68.up.railway.app/api
RUN env
RUN npm i && npm run build
ENTRYPOINT ["./entrypoint.sh"]
