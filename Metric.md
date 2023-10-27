# ASR Metric
How to measure perforance of model or decoder.

## Try it yourself

        (base)$ pip install jupyter
        jupyter lab --notebook-dir ~/a1003/asr-train/local/ --ip 0.0.0.0

On error, run

        /home/etriai01/miniforge3/bin/jupyter lab --notebook-dir ~/a1003/asr-train/local/ --ip 0.0.0.0

Open link shown in ouput using Chrome. Open `error_rate.ipynb`.

## For Korean charaters

Open `wer.ipynb`


## CER and WER for multiple utterances

        (espnet)$ python local/uttwer.py data/mydata/text result/text
        (espnet)$ python local/uttcer.py data/mydata/text result/text

