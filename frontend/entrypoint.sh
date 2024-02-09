#!/bin/bash

set -eux

echo "server {
	listen $PORT default_server;
	listen [::]:$PORT default_server;
	root /app/frontend/dist;
	index index.html;
	server_name _;
	location / {
		try_files \$uri \$uri/ =404;
	}
	location /api {
      proxy_pass http://0.0.0.0:8000;
	}
}" >| /etc/nginx/conf.d/default.conf
cd /app/frontend
npm i
npm run build

nginx -g "daemon off;"
