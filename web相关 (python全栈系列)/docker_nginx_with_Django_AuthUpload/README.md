# nginx with django to support auth, upload(drag or click) and pic_pipeline.

# Why use this?

If you want to start a nginx with upload by login and user control, you can use this folder as docker to start by one command.

# How to use?
```
cd docker/
# only once
docker-compose build

docker-compose up -d  #you can change the .yml=> /src/files path and rerun this command
```