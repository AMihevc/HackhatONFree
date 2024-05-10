#!/bin/bash
#SBATCH --job-name=weather
#SBATCH --output=logs/weather_%A_%a.out
#SBATCH --error=logs/weather_%A_%a.err
#SBATCH --time=4-00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --array=0-0%18

##SBATCH --mem-per-cpu=2G

# srun --time=0-04:00 -n 1 -N 1 -c 12 --mem=16G --partition gpu --gres gpu:0 --pty bash -i


if [ -z "$SLURM_ARRAY_TASK_ID" ]; then
    export SLURM_ARRAY_TASK_ID=0
fi


source "$HOME"/.bashrc
conda activate hackathon

cd /d/hpc/home/tp1859/HackhatONFree/src/weather_simple

export PYTHONUNBUFFERED=1
export CUDA_VISIBLE_DEVICES=0


srun python main.py \
    --date_fr 2022-01-01 \
    --date_to 2024-05-10 \
    2>&1 | tee output2022.log

srun python main.py \
    --date_fr 2010-01-01 \
    --date_to 2024-05-10 \
    2>&1 | tee output2010.log

srun python main.py \
    --date_fr 2000-01-01 \
    --date_to 2024-05-10 \
    2>&1 | tee output2000.log
    # --partition gpu \
    # --time=0-04:00 \
    # --gres=gpu:2 \
    # -N 1 -n 1 \
    # -c 16 \
    # --mem=0 \
    # -w wn205 \
    
cd -
