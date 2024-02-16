# MongoDBを使う

管理画面から以下のvalueを取る
- `MONGO_INITDB_ROOT_USERNAME`
- `MONGO_INITDB_ROOT_PASSWORD`

## 接続
```
mongosh monorail.proxy.rlwy.net:56751 -u $MONGO_INITDB_ROOT_USERNAME
```

```
test> use score
switched to db score
score> db.score.insertOne({fe:1, puga:2})
{
  acknowledged: true,
  insertedId: ObjectId('65baa8b398030d88e4a311b3')
}
score> db.score.find()
[ { _id: ObjectId('65baa8b398030d88e4a311b3'), fe: 1, puga: 2 } ]
score> db.score.drop()
true
score> db.score.find()

score>
```

## Programmable access
https://www.hopes.host/blog/php-mongodb

# Railsway.appの設定
`MongoDB -> Settings _> Source -> Source Image -> mongo` をbuild
