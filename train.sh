#!/bin/bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

./asr.sh \
    --skip_data_prep false \
    --skip_train false \
    --skip_eval false \
    --lang ko \
    --ngpu 1 \
    --nj 8 \
    --stage 3 \
    --stop_stage 5 \
    --gpu_inference true \
    --inference_nj 1 \
    --token_type char \
    --feats_normalize 'global_mvn' \
    --max_wav_duration 30 \
    --speed_perturb_factors "" \
    --audio_format "flac.ark" \
    --feats_type raw \
    --use_lm false \
    --asr_exp exp/tf \
    --asr_config conf/train_asr_transformer2.yaml \
    --inference_config conf/decode_asr.yaml \
    --inference_asr_model valid.acc.ave.pth \
    --train_set train \
    --valid_set dev \
    --test_sets test
