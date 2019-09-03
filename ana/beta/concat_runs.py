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