# Set-up

## Cleanup my account

        $ rm -rf ~/a1003

## Download a1003

        $ git clone https://github.com/pkyoung/a1003

## Conda

* Check conda installation

    which conda

* Install conda if not installed

### Conda: Anaconda (miniconda) + conda-forge
Use `anaconda` with `conda-forge` channel

        $ which conda
        $ conda info
        $ conda config --show channels
        $ conda config --show default_channels
        $ conda conifg --add channels conda-forge && conda config --set channel_priority strict

### Conda: miniforge3
See [Miniforge Homepage](https://github.com/conda-forge/miniforge)

        $ cd
        $ wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
        $ sh Miniforge3-Linux-x86_64.sh

Then, start new `Terminal`

        $ conda info

## Create conda env

        conda create -n a1003 python=3.10
        conda activate a1003

## Jupyter

        (a1003)$ pip install jupyter
        jupyter

## Check text editor: `Code`

Launch `Code` app

## Check GPU (for training)

        (a1003)$ nvidia-smi
        (a1003)$ nvcc -V
