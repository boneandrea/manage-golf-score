# for Railway.app
FROM anzusystems/node:3.0.0-node24-nginx

COPY ./hehe /app
WORKDIR /app
ARG BASIC_AUTH_PASSWORD
ARG BASIC_AUTH_USERNAME
ARG VITE_API_ROOT

RUN npm i && npm run build
ENTRYPOINT ["./entrypoint.sh"]
