#!/bin/bash

set -eux

env
npm i
npm run build

echo "server {
	listen $PORT default_server;
	root /app/dist;
	index index.html;
	server_name _;
	location / {
		try_files \$uri \$uri/ =404;
	}
}" >| /etc/nginx/conf.d/default.conf

# sed -i "s/listen\s*80/listen $PORT/" /etc/nginx/conf.d/default.conf
# sed -i '0,/root.*/ s/\/usr\/share\/nginx\/html/\/app\/dist/' /etc/nginx/conf.d/default.conf

nginx -g "daemon off;"
