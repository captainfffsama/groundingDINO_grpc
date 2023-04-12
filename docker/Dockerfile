FROM  pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel as rpc
RUN sed -i "s@http://.*archive.ubuntu.com@http://mirrors.bfsu.edu.cn@g" /etc/apt/sources.list \
    && sed -i "s@http://.*security.ubuntu.com@http://mirrors.bfsu.edu.cn@g" /etc/apt/sources.list \
    && rm /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-key del 7fa2af80 \
    # && wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb \
    # && dpkg -i cuda-keyring_1.0-1_all.deb \
    # && rm cuda-keyring_1.0-1_all.deb \
    && apt update && apt install -y \
    git \
    cmake \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && cd /root \
    && git config --global http.sslverify false \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir grpcio-tools=1.37.0\
    && pip install --no-cache-dir git+https://github.com/captainfffsama/GroundingDINO.git@chiebot_dev \
    && pip install --no-cache-dir pid  \
    && conda clean --all \
    && git clone https://github.com/captainfffsama/groundingDINO_grpc.git \
    && mkdir /root/mount \
    && mkdir /root/mount/bert-base-uncased \
    && cd /root/mount/bert-base-uncased \
    && wget https://huggingface.co/bert-base-uncased/resolve/main/tokenizer.json \
    && wget https://huggingface.co/bert-base-uncased/resolve/main/tokenizer_config.json \
    && wget https://huggingface.co/bert-base-uncased/resolve/main/vocab.txt \
    && wget https://huggingface.co/bert-base-uncased/resolve/main/config.json \
    && wget https://huggingface.co/bert-base-uncased/resolve/main/pytorch_model.bin \
    && cd /root/mount/ \
    && wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha2/groundingdino_swinb_cogcoor.pth


FROM rpc as final
COPY ./utils/monitrc /root/monitrc
COPY ./utils/server_manager /root/server_manager
RUN cd /root \
    && chmod -R a+x ./server_manager/* \
    && mv /root/monitrc /etc/monit/monitrc \
    && chmod 0700 /etc/monit/monitrc \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime #修改时区
EXPOSE 52017
#monit端口
EXPOSE 2812
ENTRYPOINT [ "sh","/root/server_manager/system_entry_point.sh"]
