#!/bin/bash -eu


# Configuraiton
idir=data/mydata
odir=./result
model=exp/exp01a/37epoch.pth_
nj=8
# End of Configuraiton

source path.sh

mkdir -p $odir/log
mdir=$(dirname $model)

# 1. Generate feats and split to $nj
#
./steps/make_fbank.sh $idir

key_file=$idir/feats.scp
for n in $(seq $nj); do
    split_scps+=" $odir/log/keys.${n}.scp"
done
utils/split_scp.pl "${key_file}" ${split_scps}

# 2. Run decoding jobs
#
run.pl JOB=1:$nj $odir/log/asr_inference.JOB.log \
    python -m espnet2.bin.asr_inference \
        --data_path_and_name_and_type "$idir/feats.scp,speech,kaldi_ark" \
        --key_file $odir/log/keys.JOB.scp \
        --asr_train_config $mdir/config.yaml \
        --asr_model_file $model \
        --output_dir $odir/log/output.JOB

# 3. Concatenates the output files from each jobs
for f in token token_int score text; do
    for i in $(seq $nj); do
        cat "$odir/log/output.${i}/1best_recog/${f}"
    done | LC_ALL=C sort -k1 >"${odir}/${f}"
done
