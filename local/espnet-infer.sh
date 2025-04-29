#!/bin/bash -eu

# Configuraiton
data=./data/a1003
model=./models/ma16k2401a/final.mdl
odir=./results
conf=../conf/decode_asr.yaml
# End of Configuraiton

mkdir -p $odir/log

trnconfig=$(dirname $model)/config.yaml
python3 -m espnet2.bin.asr_inference --batch_size 1 --ngpu 0 \
    --data_path_and_name_and_type $data/wav.scp,speech,sound \
    --asr_train_config $trnconfig \
    --asr_model_file $model \
    --output_dir $odir \
    --config $conf
