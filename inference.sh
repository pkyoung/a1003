#!/bin/bash -eu

# Configuraiton
data=/Lxdata/A1003/db/navidlg
model=/Lxdata/A1003/models/ha16k2310c/avg50_10.mdl
odir=./result
conf=conf/decode_asr.yaml
# End of Configuraiton

. ./path.sh
. ./utils/parse_options.sh

mkdir -p $odir/log

trnconfig=$(dirname $model)/config.yaml
python3 -m espnet2.bin.asr_inference --batch_size 1 --ngpu 0 \
    --data_path_and_name_and_type $data/wav.scp,speech,sound \
    --asr_train_config $trnconfig \
    --asr_model_file $model \
    --output_dir $odir \
    --config $conf
