
# Install ESPnet for inference only

## Install ESPnet and (optionally) Kaldi

        conda activate a1003
        pip install espnet torchaudio
        conda install kaldi

## Download espnet code for review

        cd ~
        git clone https://github.com/espnet/espnet

Open `~/espent` directory in VScode

## Download ASR models

`git lfs` is required

        (a1003)$ conda install git-lfs

Download models from huggingface

        (a1003)$ cd a1003
        (a1003)$ mkdir -p models
        (a1003)$ cd models
        (a1003)$ git lfs clone https://hf.co/pkyoung/ma16k2401a
        (a1003)$ git lfs clone https://hf.co/pkyoung/ma16k2401b
        (a1003)$ git lfs clone https://hf.co/pkyoung/ma16k2401c


## Run inference

Check models, data and configuration

        (a1003)$ cd ~/a1003
        (a1003)$ ls models/ma16k2401a
        (a1003)$ ls data/eval_clean
        (a1003)$ ls conf/decode_asr.yaml

Edit `inference.sh` and run it.

        (a1003)$ bash inference.sh

## Scoring results

Open `results/1best_recog/text`

        (a1003)$ python local/uttcer.py data/eval_clean/text results/1best_recog/text

        (a1003)$ sed 's,[.?!,],,g' results/1best_recog/text > results/1best_recog/text.2
        (a1003)$ python local/uttcer.py data/eval_clean/text results/1best_recog/text.2

