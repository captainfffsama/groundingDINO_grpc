###
 # @Author: captainfffsama
 # @Date: 2023-04-12 12:24:47
 # @LastEditors: captainfffsama tuanzhangsama@outlook.com
 # @LastEditTime: 2023-04-12 12:27:02
 # @FilePath: /groundingDINO_grpc/docker/build_container.sh
 # @Description:
###
docker build -t gdino:v1 . --no-cache
docker run -itd --runtime=nvidia --gpus all -p 2812:2812 -p 52017:52017 --name  gdino_server gdino:v1 --restart=always
docker update gdino_server --restart=always