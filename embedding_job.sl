#!/bin/bash
#SBATCH --job-name=esm_embed_a100
#SBATCH --output=esm_%j.out
#SBATCH --error=esm_%j.err
#SBATCH --partition=gpu-a100
#SBATCH --gres=gpu:1
#SBATCH --mem=128G
#SBATCH --cpus-per-task=16
#SBATCH --time=08:00:00

module load python/3.10.8
module load pytorch-gpu/1.13.1


python esm_embedding.py
