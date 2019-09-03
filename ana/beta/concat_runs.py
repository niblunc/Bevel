# Script to build a nifti file tsv file of concatenated runs from a subject 
# Author Nichollette A. and Jenny S
# Bevel Betaseries

import glob, os
import numpy as np
import nibabel as nib
import pandas as pd 
 
bids_path = "/projects/niblab/bids_projects/Experiments/Bevel/BIDS"
SUBJECTS = glob.glob(os.path.join(bids_path, "sub-001"))

for sub_path in sorted(SUBJECTS):
    sub_id = sub_path.split("/")[-1]
    niftis = sorted(glob.glob(os.path.join(sub_path, "func/*run-*.nii.gz")))
    outpath = os.path.join(sub_path, "func")
    FILENAME = "{}_task-runs_bold.nii.gz".format(sub_id)
    print("Generating files {}.......".format(FILENAME))
    #load in all the files from the glob above, then convert them from nifti1 to nifti2\n",
    #ni2_funcs = (nib.Nifti2Image.from_image(nib.load(func)) for func in niftis)
    #concat, this is with nibabel, but should work with nilearn too
    #ni2_concat = nib.concat_images(ni2_funcs, check_affines=False, axis=3)
    #set the output file name
    #outfile=os.path.join(outpath,FILENAME)
    #write the file
    #ni2_concat.to_filename(outfile)
    tsvs = sorted(glob.glob(os.path.join(sub_path, "func/*run-*.tsv")))
    tsv_out = os.path.join(outpath, "{}_task-runs_events.tsv".format(sub_id))    
    dfs = []
    for tsv in tsvs:
        df = pd.read_csv(tsv, sep="\t")
        dfs.append(df)
    concat_df = pd.concat(dfs)
    concat_df.to_csv(tsv_out, sep="\t", index=None)
    
    
    
    
FMRIPREP = glob.glob(os.path.join(bids_path, "derivatives/fmriprep", "sub-001"))
for sub_path in FMRIPREP:
    sub_id = sub_path.split("/")[-1]
    preproc_niis = sorted(glob.glob(os.path.join(sub_path, "func/*run-*preproc.nii.gz")))
    mask_niis = sorted(glob.glob(os.path.join(sub_path, "func/*run-*brainmask.nii.gz")))
    confound_tsvs = sorted(glob.glob(os.path.join(sub_path, "func/*run-*confounds.tsv")))
    outpath = os.path.join(sub_path, "func")
    FILENAME = "{}_task-runs_bold_space-MNI152NLin2009cAsym_preproc.nii.gz".format(sub_id)
    print("Generating file {}....... \nFILES: \t{}".format(FILENAME, preproc_niis))
    #load in all the files from the glob above, then convert them from nifti1 to nifti2\n",
    ni2_funcs = (nib.Nifti2Image.from_image(nib.load(func)) for func in preproc_niis)
    #concat, this is with nibabel, but should work with nilearn too
    ni2_concat = nib.concat_images(ni2_funcs, check_affines=False, axis=3)
    #set the output file name
    outfile=os.path.join(outpath,FILENAME)
    #write the file
    ni2_concat.to_filename(outfile)
    MASK_FILENAME = "{}_task-runs_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz".format(sub_id)
    print("Generating file {}....... \nFILES: \t{}".format(MASK_FILENAME, mask_niis))
    #load in all the files from the glob above, then convert them from nifti1 to nifti2\n",
    ni2_funcs = (nib.Nifti2Image.from_image(nib.load(func)) for func in mask_niis)
    #concat, this is with nibabel, but should work with nilearn too
    ni2_concat = nib.concat_images(ni2_funcs, check_affines=False)
    #set the output file name
    outfile=os.path.join(outpath,MASK_FILENAME)
    #write the file
    ni2_concat.to_filename(outfile)
    
    tsv_out = os.path.join(outpath, "{}_task-runs_bold_confounds.tsv".format(sub_id))    
    dfs = []
    for tsv in confound_tsvs:
        df = pd.read_csv(tsv, sep="\t")
        dfs.append(df)
    concat_df = pd.concat(dfs)
    print("Writing out tsv file {}........".format(tsv_out))
    concat_df.to_csv(tsv_out, sep="\t", index=None)
    