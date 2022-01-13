#!/bin/bash -eu

# Configuraiton
data_dir=data/mydata
out_dir=./result
model_file=/path/to/model.pth
beam_size=3
nj=8
# End of Configuraiton

. ./path.sh
. ./utils/parse_options.sh

mkdir -p $out_dir/log
mdir=$(dirname $model_file)

# 1. Generate feats and split to $nj
#
if [ ! -f $data_dir/feats.scp ]; then
    ./steps/make_fbank.sh $data_dir
else
    echo "$data_dir/feats.scp exists. using it"
fi

key_file=$data_dir/feats.scp
for n in $(seq $nj); do
    split_scps+=" $out_dir/log/keys.${n}.scp"
done
utils/split_scp.pl "${key_file}" ${split_scps}

# 2. Run decoding jobs
#
run.pl JOB=1:$nj $out_dir/log/asr_inference.JOB.log \
    python -m espnet2.bin.asr_inference \
        --data_path_and_name_and_type "$data_dir/feats.scp,speech,kaldi_ark" \
        --key_file $out_dir/log/keys.JOB.scp \
        --asr_train_config $mdir/config.yaml \
        --beam_size $beam_size \
        --asr_model_file $model_file \
        --output_dir $out_dir/log/output.JOB

# 3. Concatenates the output files from each jobs
for f in token token_int score text; do
    for i in $(seq $nj); do
        cat "$out_dir/log/output.${i}/1best_recog/${f}"
    done | LC_ALL=C sort -k1 >"${out_dir}/${f}"
done
