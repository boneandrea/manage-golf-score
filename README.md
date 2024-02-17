# What

ゴルフスコア管理システム  
ランキング作成のため

# 構成
以下のモノレポ構成  
localは`docker compose`, deployは`git push`でOK

- front: Vue
- back: Flask
- DB: mongodb

Railwayで稼働するため、`Dockerfile`と`Dockerfile.local`が別れている.  
localでは`docker compose`が`*/Dockerfile.local`を読んで動作する

## 環境変数

### local
- `WEB_PORT`=8003 フロントエンドのポート. `http://localhost:WEB_PORT`で稼働
- `API_PORT`=8004 バックエンドAPIのポート.
- (frontend) `VITE_API_ROOT`=`http://localhost:8004/api` frontendからbackendを叩くときのルート
- (backend) `FRONTEND_URL` CORS制限のため、backendにfrontendのURLを与える

以下、DB情報
- (backend) `DB_SERVER` 
- (backend) `DB_PORT`
- (backend) `DB_USERNAME`
- (backend) `DB_PASSWORD`


### production
localと同様だが、`WEB_PORT` `API_PORT`は不要  
さらに、以下を設定

- (frontend) `RAILWAY_DOCKERFILE_PATH` Dockerfileのパス
- (backend) `RAILWAY_DOCKERFILE_PATH` Dockerfileのパス
