
# OpenAI Whisper

* https://github.com/openai/whisper

## Install

        conda create -n whisper python=3.10

Why not `mamba`

        mamba create -n whisper python=3.10

Activate environment

        conda activate whisper
        pip install openai-whisper

## Inference
Models are download automatically if needed

        whisper /Lxdata/A1003/db/navidlg/wav/NAVIDLG201304PKY01_018.wav

# Whisper-x
All-in-one package of ASR. See https://github.com/m-bain/whisperX

* VAD
* Speech-to-text
* Speaker Diarization
* Word Alignment


# Adapt Whisper models with ESPnet
Refer [Hugging Face's model page].
Install whisper in ESPnet using `espnet/tools/installers/install_whisper.sh` 

[Hugging Face's model page]: https://huggingface.co/espnet/shihlun_asr_whisper_medium_finetuned_librispeech100

```
    ./asr.sh \
        --skip_data_prep false \
        --skip_train false \
        --skip_eval false \
        --lang ko \
        --tokenizer_language ko \
        --ngpu 1 \
        --nj 1 \
        --stage 3 \
        --stop_stage 11 \
        --gpu_inference true \
        --inference_nj 1 \
        --token_type whisper_multilingual \
        --feats_normalize '' \
        --max_wav_duration 30 \
        --speed_perturb_factors "" \
        --audio_format "flac.ark" \
        --feats_type raw \
        --use_lm false \
        --cleaner whisper_basic \
        --asr_tag my_whisper \
        --asr_config conf/train_asr_whisper_full.yaml \
        --inference_config conf/decode_asr_whisper_noctc_greedy.yaml \
        --inference_asr_model valid.acc.ave.pth \
        --train_set train \
        --valid_set dev \
        --test_sets test
```

## Inference using ESPnet

Given the ESPnet model from fine-tuning or training from scratch,
inference can be accomplished using `inferece.sh` provided.

```
    bash inference.sh \
        --model exp/my_whisper/valid.acc.ave_3best.pth \
        --conf conf/decode_asr_whisper_noctc_greedy.yaml \
        --data data/test \
        --odir result/
```
