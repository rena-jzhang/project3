#!/usr/bin/env bash
#SBATCH --mem=30000
#SBATCH --gres=gpu:1
#SBATCH --time=0
#SBATCH --output=slurm_out/slurm-%j.out

#set -e


out_dir=$1
inits=$2  # a list of models joined by ","
iters=$3  # a list of models joined by ","
num_mask=$4
max_iter=$5

hint_lang=$6
lang=$7

mkdir -p ${out_dir}

IFS=','
read -ra INITS <<< "${inits}"
read -ra ITERS <<< "${iters}"

for init in "${INITS[@]}"; do
    for iter in "${ITERS[@]}"; do

        if [[ $init == all && $iter == none ]]; then
            my_max_iter=1
        else
            my_max_iter=$max_iter
        fi

        filename=${out_dir}/init_${init}_iter_${iter}.out
        pred_dir=${out_dir}/init_${init}_iter_${iter}

        python scripts/probe.py --use_hint --hint_lang $hint_lang --no_len_norm --lang $lang --num_mask $num_mask \
            --max_iter $my_max_iter --pred_dir $pred_dir --init_method $init --iter_method $iter &> $filename
        # fi
    done
done
