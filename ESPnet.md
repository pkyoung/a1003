
# Install ESPnet and setting up enviroment

## Cleanup my account

        $ rm -rf ~/a1003

## Install ESPnet
See [ESPnet Installation] page.

        $ export PATH=/usr/local/cuda/bin:$PATH
        $ mkdir -p ~/a1003
        $ cd ~/a1003

        $ git clone https://github.com/espnet/espnet

        $ cd ~/a1003/espnet/tools
        $ ./setup_anaconda.sh miniconda espnet 3.8
        $ make
        $ git clone --depth 1 https://github.com/kaldi-asr/kaldi

To clean installation

        $ conda env remove -n espnet

[ESPnet Installation]: https://espnet.github.io/espnet/installation.html

## Now download a1003

        $ cd ~/a1003
        $ git clone https://github.com/pkyoung/a1003 ./asr-train

        $ cd ~/a1003/asr-train
        $ ls

        $ ls -l ~/a1003/espnet/egs2/TEMPLATE/asr1/
        $ ls -l ~/a1003/espnet/egs2/ksponspeech/asr1/

        $ ln -sf ~/a1003/espnet/egs2/TEMPLATE/asr1/{steps,utils,pyscripts,scripts} .

Edit `path.sh`.

        $ source path.sh
        (espnet)$ ls

# Training ASR Model with ESPnet

## Prepare data: train/valid/test

### Select train data
We will use data from AIHub [[KsponSpeech]]. List of files are mode for convenience.

        (espnet)$ cd ~/a1003/asr-train/data/
        (espnet)$ tar xvzf ks.tgz

Choose one of following 3 options:

        (espnet)$ cd ~/a1003/asr-train/data/ks
        (espnet)$ cat uttid.01 uttid.03 uttid.05 > uttid.train

or

        (espnet)$ cd ~/a1003/asr-train/data/ks
        (espnet)$ cat uttid.01 uttid.03 > uttid.train

or

        (espnet)$ cd ~/a1003/asr-train/data/ks
        (espnet)$ cat uttid.01 > uttid.train

[KsponSpeech]: https://aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=realm&dataSetSn=123

## Prepare data directory
Prepare data director in Kaldi format. We need 4 files.

* `wav.scp`: mapping of utterence id to wav file path
* `text`: mapping of utterence id to transcription
* `utt2spk`: mapping of utterence id to speaker id
* `spk2utt`: mapping of speaker id to utterence id

        (espnet)$ cd ~/a1003/asr-train

        (espnet)$ mkdir -p data/train
        (espnet)$ filter_scp.pl data/ks/uttid.train data/ks/wav.scp > data/train/wav.scp
        (espnet)$ filter_scp.pl data/ks/uttid.train data/ks/text > data/train/text
        (espnet)$ awk '{print $1 " " $1}' data/train/wav.scp > data/train/spk2utt
        (espnet)$ cp data/train/spk2utt data/train/utt2spk

        (espnet)$ mkdir -p data/dev
        (espnet)$ filter_scp.pl data/ks/uttid.dev data/ks/wav.scp > data/dev/wav.scp
        (espnet)$ filter_scp.pl data/ks/uttid.dev data/ks/text > data/dev/text
        (espnet)$ awk '{print $1 " " $1}' data/dev/wav.scp > data/dev/spk2utt
        (espnet)$ cp data/dev/spk2utt data/dev/utt2spk

        (espnet)$ mkdir -p data/test
        (espnet)$ filter_scp.pl data/ks/uttid.test data/ks/wav.scp > data/test/wav.scp
        (espnet)$ filter_scp.pl data/ks/uttid.test data/ks/text > data/test/text
        (espnet)$ awk '{print $1 " " $1}' data/test/wav.scp > data/test/spk2utt
        (espnet)$ cp data/test/spk2utt data/test/utt2spk


## Run trining with asr.sh
Do it step by step (for convenience of explanation)

### run asr.sh: stage3-5

* Stage 3: `Format wav.scp: data/ -> dump/raw`
  - elapsed=1126s,93s,6s
* Stage 4: `Remove long/short data: dump/raw/org -> dump/raw`
* Stage 5:
  - `Generate character level token_list from dump/raw/org/train/text`
  - `Generate token_list from dump/raw/org/train/text using BPE`

Run one of `stage3-5.sh` and `stage3-5use_bpe.sh`

        (espnet)$ bash stage3-5.sh

or

        (espnet)$ bash stage3-5use_bpe.sh

Open ``

### run asr.sh: stage10

* Stage 10: `ASR collect stats: train_set=dump/raw/train, valid_set=dump/raw/dev`

        (espnet)$ bash stage10.sh

* `Successfully finished. [elapsed=1153s,240s]`

### run asr.sh: stage11

* Stage 11: `ASR Training: train_set=dump/raw/train, valid_set=dump/raw/dev`

        (espnet)$ bash stage11.sh

### Monitoring training with tensorboard

* Run `nvidia-smi`
* Run one of followings and open `http://localhost:6006` from Chorme

        (espnet)$ tensorboard --logdir /Lxdata/A1003/models

or

        (espnet)$ tensorboard --logdir ~/a1003/asr-train/exp

or

        (espnet)$ tensorboard --logdir ~/a1003/asr-train/exp --bind_all

* See `exp/myasr/train.log`

        (espnet)$ tail -f ~/a1003/asr-train/exp/train.log

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

