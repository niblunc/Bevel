# Derivatives Template Generator 
# Author: Nichollette Acosta | NIBL
# This program generates the ~/derivatives/ directory and the anat/, func/, 
# motion_assessment/ and onset/ directories within it. It will also fill in the 
# directories if prompted to with the relevant anatomical and functional files.

# Import necessary packages

import os, glob


# Given Directory Paths 
base_dir = '/projects/niblab/bids_projects/Experiments/Bevel'
fmriprep_dir = '/projects/niblab/bids_projects/Experiments/Bevel/lin_fmri/fmriprep' 

# Get subjects to fill derivatives path with
SUBJECTS = sorted([x for x in glob.glob(os.path.join(fmriprep_dir, "sub-*")) if "html" not in x])

# New Directory Paths to make
deriv_path = os.path.join(base_dir, "testing_lin", "derivatives")
if not os.path.exists(deriv_path):
    os.makedirs(deriv_path)
    
# Create the subject directories
for sub_dir in SUBJECTS:
    sub_id = sub_dir.split("/")[-1]
    paths = []
    deriv_sub_dir = os.path.join(deriv_path, sub_id)
    paths.append(deriv_sub_dir)
    anat_path = os.path.join(deriv_sub_dir, "anat")
    paths.append(anat_path)
    func_path = os.path.join(deriv_sub_dir, "func")
    paths.append(func_path)
    onset_path = os.path.join(func_path, "onsets")
    paths.append(onset_path)
    motion_path = os.path.join(func_path, "motion_assessment")
    paths.append(motion_path)
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
            
    # Fill in Paths
    fmri_anat = os.path.glob(fmriprep_dir, sub_id, "anat/%s_space-MNI152Lin_desc-preproc_T1w.nii.gz"%sub_id)
    print(fmri_anat)
    fmri_funcs = glob.glob(os.path.join(fmriprep_dir, sub_id, "func/*preproc_bold.nii.gz"))
    print(fmri_funcs)
    