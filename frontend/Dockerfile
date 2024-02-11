FROM nginx:latest

RUN apt update && apt install curl gpg -y

# install node21

RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_21.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt update && apt install nodejs -y
RUN node -v

WORKDIR /app

#RUN sed -i "s/listen\s*80/listen 8888/" /etc/nginx/conf.d/default.conf
#RUN sed -i '0,/root.*/ s/\/usr\/share\/nginx\/html/\/app\/dist/' /etc/nginx/conf.d/default.conf

ENTRYPOINT ["./entrypoint.sh"]
#CMD ["nginx", "-g", "daemon off;"]
