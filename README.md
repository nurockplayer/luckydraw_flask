# Docker 使用步驟


先安裝 Docker Desktop  
Mac 可以用 homebrew 安裝
```
$ brew cask install docker
```
安裝好之後開啟 Docker.app

然後將 docker-compose 啟動
```
$ docker-compose up -d
```

第一次下載會需要一些時間  
趁著下載的期間寫設定檔
```
$ mkdir instance
$ touch instance/local.cfg
```

並將以下三項設定寫進 local_docker.cfg
```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@mariadb:3306/luckydraw?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
```


docker-compose 創建成功之後會顯示
```
Creating luckydraw_flask_mariadb_1 ... done
Creating luckydraw_flask_web_1     ... done
```

看見成功的提示之後就可以用 exec 進入 docker command
```
$ docker exec -it luckydraw_flask_web_1 zsh
```

進入 docker command 模式之後  
要先建立資料庫  
這邊已經用 Makefile 寫好  
只需要下 make 就可以了
```
$ cd root/web
$ make
```

接下來就可以啟動 flask
```
$ flask run --host 0.0.0.0
```

到這邊就可以在瀏覽器開啟網頁了!!!
```
http://localhost:5000
```
