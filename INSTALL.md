# Installation

* https://espnet.github.io/espnet/installation.html

## As of 2021/11/28 with CUDA 11.4/11.5, espnet 0.10.5a1

    git clone https://github.com/espnet/espnet
    cd espnet/tools
    ./setup_anaconda.sh anaconda espnet 3.8
    make TH_VERSION=1.8.1 CUDA_VERSION=11.1
    # or make TH_VERSION=1.9.0 CUDA_VERSION=11.1
    # or make TH_VERSION=1.8.1 CUDA_VERSION=10.2


    # apt-get install wget subversion git
    # apt install automake autoconf unzip sox gfortran libtool zlib1g libtool zlib1g-dev

    cd espnet/tools/kaldi/tools
    extras/check_dependencies.sh
    make -j 8

    cd espnet/tools/kaldi/src
    ./configure --shared --use-cuda=no
    make clean depend -j 8
    make -j 8

