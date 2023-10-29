
# ESPnet 설치를 위한 Docker 환경 구성

* 이 부분은 관리자가 수행한다.

        sudo apt-get update
        sudo apt-get install -y nvidia-driver-535 nvidia-utils-535

        distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
            && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey \
            | sudo apt-key add - \
            && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list \
            | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
        sudo apt-get update
        sudo apt-get install -y nvidia-docker2
        sudo systemctl restart docker

        sudo usermod -a -G docker etriai02

        ## apt upgrade nvidia-container-toolkit nvidia-container-toolkit-base

* 이제 logout 하고 다시 login 하자.

        $ id
        uid=1002(etriai02) gid=1002(etriai02) groups=1002(etriai02),999(docker)

        $ docker run --gpus all nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04 nvidia-smi
        Unable to find image 'nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04' locally
        12.2.2-cudnn8-devel-ubuntu22.04: Pulling from nvidia/cuda

## Install ESPnet on Docker

        $ docker run -it --shm-size=8G --gpus all -v /Lxdata:/Lxdata -v /home:/home \
            nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04 /bin/bash

        # apt update && apt install -y git wget

* 아래 `etriai02` 및 `1002` 는 현재 로그인한 계정에 맞게 바꾸어 실행한다.

        # groupadd -g 1002 etriai02
        # useradd -u 1002 -g 1002 -d /home/etriai02 -s /bin/bash etriai02
        # su - etriai02

Now see [ESPNet](./ESPNet.md)
