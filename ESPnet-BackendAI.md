# https://github.com/pkyoung/a1003


# Prepare Backend.AI Env.

* Login: `address_hidden`
* Create Private Folder
    shared
* Create Session
    * Select Environments: `pytorch-espnet`
    * Select Version: `210325`
    * Mount Folders: `a1003` and `shared`
    * Max `CPU`, `RAM`, `Shared Memory`, `GPU`
    * 1 `Session`

# Start Session
    * (unblock popup)
    * Try **copy and paste**

## Prepare for tensorboard

    mkdir -p /home/work/logs
    ln -s /home/work/a1003/models/ref1x /home/work/logs/ref1x

## Try Apps
* `Visual Studio Code`
* `Console`
* `Tensorboard`

## Download scripts

    git clone https://github.com/pkyoung/a1003.git ./train.1
    cd train.1
    cd data && tar xvzf ks.tgz && cd ..
    ln -s /opt/kaldi/egs/wsj/s5/steps .
    ln -s /opt/kaldi/egs/wsj/s5/utils .
    


# Train ASR

## Choice: Set training corpus

    cat data/ks/uttid.01 data/ks/uttid.03 data/ks/uttid.05 > data/ks/uttid.train
    cat data/ks/uttid.01 data/ks/uttid.03 > data/ks/uttid.train
    cat data/ks/uttid.01 > data/ks/uttid.train

## Prepare data

    source path.sh
    mkdir -p data/train data/test data/dev
    filter_scp.pl data/ks/uttid.test data/ks/wav.scp > data/test/wav.scp
    filter_scp.pl data/ks/uttid.dev data/ks/wav.scp > data/dev/wav.scp
    filter_scp.pl data/ks/uttid.train data/ks/wav.scp > data/train/wav.scp
    filter_scp.pl data/ks/uttid.test data/ks/text > data/test/text
    filter_scp.pl data/ks/uttid.dev data/ks/text > data/dev/text
    filter_scp.pl data/ks/uttid.train data/ks/text > data/train/text
    awk '{print $1 " " $1}' data/test/wav.scp > data/test/spk2utt
    awk '{print $1 " " $1}' data/dev/wav.scp > data/dev/spk2utt
    awk '{print $1 " " $1}' data/train/wav.scp > data/train/spk2utt
    cp data/test/spk2utt data/test/utt2spk
    cp data/dev/spk2utt data/dev/utt2spk
    cp data/train/spk2utt data/train/utt2spk

## Run training

    ./steps/make_fbank.sh data/test
    ./steps/make_fbank.sh data/dev
    ./steps/make_fbank.sh data/train

    bash stage3-5.sh
    bash stage9.sh
    bash stage10.sh

    ## testing
    bash stage11.sh

## Tensorboard

    cd /home/work
    mkdir -p logs

    ## tensorboard 위치는 환경에 맞게
    ## train.1 은 아무 이름이나 구분되는 이름으로
    ln -s /home/work/train.1/exp/exp01a/tensorboard ./logs/train.1

# Testing

## Prepare Data

* Prepare files `wav.scp`,`text`,`spk2utt`,`utt2spk` in `data/mydata`
* If you don't have your data,

```
    mkdir data/mydata
    cp /home/work/a1003/db/navidlg/* data/mydata
    ## ignore cp -r ... message
```

## Run inference

* Edit inference.sh and run it

    ./inference.sh

* Measure WER and CER

    python local/uttwer.py data/mydata/text result/text
    python local/uttcer.py data/mydata/text result/text

# Pretrained models

* 훈련데이터

| model | training data | hours  | elapsed |
| ---   | ---           | ---    | ---     |
| 01    | 01            | 173.9h | 8h 8m   |
| 03    | 03            | 192.3h | 8h 55m  |
| 2x    | 01 + 03       | 366.3h | 16h 4m  |
| 3x    | 01 + 03 + 05  | 563.7h | 40h 50m (1080ti x1) |

* 모델 위치

```
    /home/work/a1003/models/ref01/valid.acc.ave_10best.pth
    /home/work/a1003/models/ref03/valid.acc.ave_10best.pth
    /home/work/a1003/models/ref2x/valid.acc.ave_10best.pth
    /home/work/a1003/models/ref3x/valid.acc.ave_10best.pth
```

* tensorboard

```
    ln -s /home/work/a1003/models/ref1x/exp01a/tensorboard /home/work/logs/ref1x
    ln -s /home/work/a1003/models/ref2x/exp01a/tensorboard /home/work/logs/ref2x
    ln -s /home/work/a1003/models/ref3x/exp01a/tensorboard /home/work/logs/ref3x
    ln -s /home/work/a1003/models/ref3x_sa/exp01a/tensorboard /home/work/logs/ref3x_sa
    ln -s /home/work/a1003/models/ref1x_lr5/exp01a/tensorboard /home/work/logs/ref1x_lr5
```
* Evaluation results: data/test

| model    | CER | WER |
| ------   | --- | ---    |
| ref1x    |   |  |
| ref2x    |   |  |
| ref3x    |   |  |
| ref3x+sa

## Evaluate mydata with pretrained models

* Edit inference.sh and run it
```
    model=/home/work/a1003/models/ref01/valid.acc.ave_10best.pth
    model=/home/work/a1003/models/ref03/valid.acc.ave_10best.pth
    model=/home/work/a1003/models/ref2x/valid.acc.ave_10best.pth
    model=/home/work/a1003/models/ref3x/valid.acc.ave_10best.pth

    bash inference.sh
```

* Measure CER/WER

```
python local/uttcer.py data/mydata/text result/text
```

# OpenAI Whisper

* https://github.com/openai/whisper

## Upgrade torch version
```
import torch
torch.__version__
```

```
/opt/conda/bin/python3 -m pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
```
```
pip install torch==1.9.0
```

## Install
```
pip install git+https://github.com/openai/whisper.git 
```

## Inference
```
git clone https://github.com/openai/whisper
cd whisper
whisper tests/jfk.flac --model tiny
```
