#!/bin/bash
#
#SBATCH --job-name=BEVEL_BIDS
#SBATCH -N 1
#SBATCH -c 1
#SBATCH -t 2:00:00
#SBATCH --mem-per-cpu 80000
## %A == SLURM_ARRAY_JOB_ID
## %a == SLURM_ARRAY_TASK_ID
#SBATCH -o /projects/niblab/bids_projects/Experiments/Bevel/error_files/bids_error_%a_out.txt
#SBATCH -e /projects/niblab/bids_projects/Experiments/Bevel/error_files/bids_error_%a_err.txt

if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then
    sub="sub-00${SLURM_ARRAY_TASK_ID}"
else
    sub="sub-0${SLURM_ARRAY_TASK_ID}"
fi


singularity exec -B /:/base_dir /projects/niblab/bids_projects/Singularity_Containers/heudiconv_05_2019.simg \
heudiconv -b -d /base_dir/projects/niblab/bids_projects/Experiments/Bevel/DICOMS/sub-{subject}/*dcm -s sub \
-f /base_dir/projects/niblab/bids_projects/Experiments/Bevel/BIDS/code/bevel_heuristic.py \
-c dcm2niix -o /base_dir/projects/niblab/bids_projects/Experiments/Bevel/BIDS
