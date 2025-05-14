# https://github.com/pkyoung/a1003

# 실습 내용
## Setup
See [Setup.md](./Setup.md)
* Conda
* Editor
* Jupyter


## Error Metric

At first open `local/error-metric.ipynb` in Jupyter notebook.
To start Jupyter notebook,
```bash
  conda activate a1003
  pip install jupyter
  jupyter notebook
```

Open `local/wer.ipynb` in Jupyter notebook, or in [Colab](https://colab.research.google.com/github/pkyoung/a1003/blob/main/local/wer.ipynb)

* Edit distnace
* CER and WER


## Feature Extraction

Open `local/play-wav.ipynb` in Jupyter notebook, or in [Colab](https://colab.research.google.com/github/pkyoung/a1003/blob/main/local/play-wav.ipynb)

* Listen to files
* Mel-filterbank
* Specaug

## Training ASR Model with ESPnet(optional)
See [ESPnet-train.md](./ESPnet-train.md)

* Data preparation
* Training
* Assessment

## Run ASR with Espnet models
**리눅스 터미널** 환경에서는 [ESPnet-inference.md](./ESPnet-inference.md) 파일대로 진행합니다.

`local/espnet.ipynb` 파일을 Jupyter notebook 또는
[Colab](https://colab.research.google.com/github/pkyoung/a1003/blob/main/local/espnet.ipynb)에서 열어서 실습합니다.

* Data and model preparatoin
* Inference
* Scoring

## Run ASR with OpenAI Whisper
**리눅스 터미널** 환경에서는 [Whisper.md](./Whisper.md) 파일대로 진행합니다.

`local/whisper.ipynb` 파일을 Jupyter notebook 또는
[Colab](https://colab.research.google.com/github/pkyoung/a1003/blob/main/local/whisper.ipynb)에서 열어서 실습합니다.

* Data and model preparatoin
* Inference
* Scoring

