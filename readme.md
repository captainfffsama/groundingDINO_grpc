# Introduction
a simple grpc server of [groundingDINO](https://github.com/IDEA-Research/GroundingDINO)

# docker build
```shell
cd docker
docker build -t gdino:v1 . --no-cache
docker run -itd --runtime=nvidia --gpus all -p 2812:2812 -p 52017:52017 --name  gdino_server gdino:v1 --restart=always
```

