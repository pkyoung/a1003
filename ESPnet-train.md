
# Install ESPnet for inference only

## Before install

* Download conda
    ```          
    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
    ```
    
* Install
    ```
    sh Miniforge3-Linux-x86_64.sh
    ```
        
* Disable auto_activate_base if conda installed
    ```
    conda config --set auto_activate_base false
    ```

## Install ESPnet
See [ESPnet Installation] page.

        $ cd
* clone source
    ```
    git clone https://github.com/espnet/espnet
    ```

* setup env
    ```
    cd ~/espnet/tools
    ./setup_miniforge.sh ~/miniforge3 espnet 3.10
    ```
* install
    ```
    make CUDA_VERSION=12.8
    ```

[ESPnet Installation]: https://espnet.github.io/espnet/installation.html

## Now download a1003

* clone source
        cd
        git clone https://github.com/pkyoung/a1003.git

* make soft link
    ```
    cd ~/a1003
    ln -sf ~/espnet/egs2/TEMPLATE/asr1/{steps,utils,pyscripts,scripts} .
    ```
    
* Edit `path.sh`.

        $ source path.sh
        (espnet)$ ls

# Training ASR Model with ESPnet

## Prepare data: train/valid/test

### Select train data
We will use data from AIHub [[KsponSpeech]]. List of files are mode for convenience.

        (espnet)$ cd ~/a1003/data/
        (espnet)$ tar xvzf ks.tgz

Choose one of following 3 options:

        (espnet)$ cd ~/a1003/data/ks
        (espnet)$ cat uttid.01 uttid.03 uttid.05 > uttid.train

or

        (espnet)$ cd ~/a1003/data/ks
        (espnet)$ cat uttid.01 uttid.03 > uttid.train

or

        (espnet)$ cd ~/a1003/data/ks
        (espnet)$ cat uttid.01 > uttid.train

[KsponSpeech]: https://aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=realm&dataSetSn=123

## Prepare data directory
Prepare data director in Kaldi format. We need 4 files.

* `wav.scp`: mapping of utterence id to wav file path
* `text`: mapping of utterence id to transcription
* `utt2spk`: mapping of utterence id to speaker id
* `spk2utt`: mapping of speaker id to utterence id

        cd ~/a1003

* generate train dir
    ```     
    mkdir -p data/train
    filter_scp.pl data/ks/uttid.train data/ks/wav.scp > data/train/wav.scp
    filter_scp.pl data/ks/uttid.train data/ks/text > data/train/text
    awk '{print $1 " " $1}' data/train/wav.scp > data/train/spk2utt
    cp data/train/spk2utt data/train/utt2spk
    ```
* generate dev dir
    ```
    mkdir -p data/dev
    filter_scp.pl data/ks/uttid.dev data/ks/wav.scp > data/dev/wav.scp
    filter_scp.pl data/ks/uttid.dev data/ks/text > data/dev/text
    awk '{print $1 " " $1}' data/dev/wav.scp > data/dev/spk2utt
    cp data/dev/spk2utt data/dev/utt2spk
    ```
* generate test dir
    ```
    mkdir -p data/test
    filter_scp.pl data/ks/uttid.test data/ks/wav.scp > data/test/wav.scp
    filter_scp.pl data/ks/uttid.test data/ks/text > data/test/text
    awk '{print $1 " " $1}' data/test/wav.scp > data/test/spk2utt
    cp data/test/spk2utt data/test/utt2spk
    ```

## Run training with asr.sh
Do it step by step (for convenience of explanation)

### run asr.sh: stage3-5

* Stage 3: `Format wav.scp: data/ -> dump/raw`
  - elapsed=1126s,93s,6s
* Stage 4: `Remove long/short data: dump/raw/org -> dump/raw`
* Stage 5:
  - `Generate character level token_list from dump/raw/org/train/text`
  - `Generate token_list from dump/raw/org/train/text using BPE`

* Edit `--stage 3` and `--stop_stage 5` in `train.sh`, then run:

        (espnet)$ bash train.sh

Open `data/ko_token_list/char/tokens.txt` or `data/ko_token_list/bpe_unigram5000/tokens.txt`

### run asr.sh: stage10

* Stage 10: `ASR collect stats: train_set=dump/raw/train, valid_set=dump/raw/dev`
* Edit `--stage 10` and `--stop_stage 10` in `train.sh`, then run:

        (espnet)$ bash train.sh

* `Successfully finished. [elapsed=1153s,240s]`
* See `asr_stats_`...

### run asr.sh: stage11

* Stage 11: `ASR Training: train_set=dump/raw/train, valid_set=dump/raw/dev`
* Edit `--stage 11` and `--stop_stage 11` in `train.sh`, then run:

        (espnet)$ bash train.sh

### Monitoring training with tensorboard

* Run `nvidia-smi`
* Run one of followings and open `http://localhost:6006` from Chorme

        (espnet)$ tensorboard --logdir /Lxdata/A1003/models

or

        (espnet)$ tensorboard --logdir ~/a1003/exp

or

        (espnet)$ tensorboard --logdir ~/a1003/exp --bind_all

* See `exp/myasr/train.log`

        (espnet)$ tail -f ~/a1003/exp/train.log

Output looks like:

        [hostname] 2023-10-27 13:29:13,321 (trainer:298) INFO: 1/30epoch started
        [hostname] 2023-10-27 13:37:46,484 (trainer:753) INFO: 1epoch:train:1-4025batch: iter_time=1.924e-04, forward_time=0.040, loss_ctc=174.564, loss_att=145.106, acc=0.235, loss=153.944, backward_time=0.049, grad_norm=156.442, clip=100.000, loss_scale=1.000, optim_step_time=0.015, optim0_lr0=1.007e-05, train_time=0.127
        [hostname] 2023-10-27 13:46:05,691 (trainer:753) INFO: 1epoch:train:4026-8050batch: iter_time=1.180e-04, forward_time=0.038, loss_ctc=144.091, loss_att=107.210, acc=0.317, loss=118.274, backward_time=0.047, grad_norm=101.564, clip=100.000, loss_scale=1.000, optim_step_time=0.014, optim0_lr0=3.019e-05, train_time=0.124
        [hostname] 2023-10-27 13:54:00,278 (trainer:753) INFO: 1epoch:train:8051-12075batch: iter_time=2.779e-04, forward_time=0.038, loss_ctc=141.743, loss_att=100.691, acc=0.336, loss=113.007, backward_time=0.043, grad_norm=105.291, clip=100.000, loss_scale=1.000, optim_step_time=0.013, optim0_lr0=5.032e-05, train_time=0.118

## Testing

### Prepare Data

* Prepare files `wav.scp`,`text`,`spk2utt`,`utt2spk` in `data/mydata`

### Run
Edit `inference.sh` and run it.


# Pretrained models

* Training data

| model | training data | hours  | elapsed |
| ---   | ---           | ---    | ---     |
| 01    | 01            | 173.9h | 8h 8m   |
| 03    | 03            | 192.3h | 8h 55m  |
| 2x    | 01 + 03       | 366.3h | 16h 4m  |
| 3x    | 01 + 03 + 05  | 563.7h | 40h 50m (1080ti x1) |

* Path to models (obsolete)

        /path/to/a1003/models/ref01/valid.acc.ave_10best.pth
        /path/to/a1003/models/ref03/valid.acc.ave_10best.pth
        /path/to/a1003/models/ref2x/valid.acc.ave_10best.pth
        /path/to/a1003/models/ref3x/valid.acc.ave_10best.pth

* tensorboard (obsolete)

        (espnet)$ tensorboard --logdir /path/to/a1003/models

