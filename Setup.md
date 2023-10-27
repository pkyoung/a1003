# Set-up

## Conda
### Conda: Anaconda (miniconda) + conda-forge
Use `anaconda` with `conda-forge` channel

        (base)$ which conda
        (base)$ conda info
        (base)$ conda config --show channels
        (base)$ conda config --show default_channels
        (base)$ conda conifg --add channels conda-forge && conda config --set channel_priority strict

### Conda: miniforge3
See [Miniforge Homepage](https://github.com/conda-forge/miniforge)

        (base)$ cd
        (base)$ wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
        (base)$ sh Miniforge3-Linux-x86_64.sh

Then, start new `Terminal`

        (base)$ conda info

## Jupyter

        (base)$ pip install jupyter
        jupyter

On error,

        /home/etriai01/miniforge3/bin/jupyter

## Check GPU

        (base)$ nvidia-smi
        (base)$ nvcc -V

## Check text editor: `Code`
Launch `Code` app

