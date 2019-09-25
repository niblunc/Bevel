
import os
import glob
import numpy as np
import pandas as pd
import pdb
import subprocess
from multiprocessing import Pool
import argparse

def set_parser():
    global parser
    global arglist
    global args
    
    parser=argparse.ArgumentParser(description='fsl analysis script, creates ROI niftis and timeseries text files for betaseries, etc.')
    
    parser.add_argument('-roi',dest='fslmerge',
                        action="store_true", help='generate ROI niftis, uses fslmerge currently')
    parser.add_argument('-ts',dest='fslmeants',
                        action="store_true", help='generate timeseries text files, uses flsmeants currently')
    parser.add_argument('-tpath',dest='trial_path',help='path to the directory that holds the trial log (.txt) text files.')
    parser.add_argument('-nii_path',dest='nifti_path', help='path to the directory to output nifti (.nii.gz) files.')
    
    args = parser.parse_args()

    return args
    
    
        
def combine_timeseries():
    roi_dict = {}
    outpath="/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/timeseries/by_sub"
    roi_dir = glob.glob(os.path.join("/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/timeseries/by_roi/*.txt"))
    for roi_file in sorted(roi_dir):
        #print(roi_file)
        sub_id = roi_file.split("/")[-1].split("_")[0]
        condition = roi_file.split("/")[-1].split("_")[1]
        #print(sub_id)
        if sub_id not in roi_dict:
            roi_dict[sub_id] = {"reward_rois" : [], "punish_rois": []}
        roi_df = pd.read_csv(roi_file, sep="\n", header=None)
        if condition == "reward":
            roi_dict[sub_id]["reward_rois"].append(roi_df)
        else:
            roi_dict[sub_id]["punish_rois"].append(roi_df)
    #print(roi_dict)
    for sub_id in roi_dict:
        reward_outpath = os.path.join(outpath, "{}_reward.txt".format(sub_id))
        punish_outpath = os.path.join(outpath, "{}_punish.txt".format(sub_id))
        reward_dataframes=roi_dict[sub_id]['reward_rois']
        punish_dataframes=roi_dict[sub_id]['punish_rois']
        final_reward_df = pd.concat(reward_dataframes, axis=1, sort=False)
        final_punish_df = pd.concat(punish_dataframes, axis=1, sort=False)
        #print(final_reward_df.head())
        print("Writing files..... \n{} \n and ....... \n{}".format(reward_outpath, punish_outpath))
        final_reward_df.to_csv(reward_outpath, header=None, index=None, sep="\t")
        final_punish_df.to_csv(punish_outpath, header=None, index=None, sep="\t")
    print("Completed making timeseries")
    #print(roi_dict)
    
    
# NEED TO PARALLEIZE ASAP 
# sooooooooooo slowwwwwwww!!!!
def pull_timeseries(nifti):
    # get nifti files
    out_dir = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/timeseries/by_roi"

    # split
    
    beta_text_file = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/betaseries_rois.txt"
    df = pd.read_csv(beta_text_file, sep="\t")
    df_T = df.T
    print(df.head())
    #for nifti in sorted(file_list):
    sub_id = nifti.split("/")[-1].split("_")[0]
    sub_condition=nifti.split("/")[-1].split("_")[1].split(".")[0]
    print(sub_id, sub_condition)
    for index in df.index.values:
        roi = df.iloc[index, 0]
        x = df.iloc[index, 1]
        y = df.iloc[index, 2]
        z = df.iloc[index, 3]
        #print(region,x,y,z)
        out_path = os.path.join(out_dir, "{}_{}_{}.txt".format(sub_id, sub_condition, roi))
        #print("Output file being made: {}".fomrat(out_path))
        cmd='fslmeants -i {} -o {} -c {} {} {} --usemm \n\n'.format(nifti, out_path, x, y, z)
        print("Running shell command: {}".format(cmd))
        subprocess.run(cmd, shell=True)
    


# *************************************************************************************

#local output directory
def concat_trials(files, trial_dict, output_dir):
    #print(sub_dirs)
    
    os.chdir(output_dir)
    # make individual files

    
    for file in files:
        sub=file.split('/')[-1].split('_')[0]
        run=file.split('/')[-1].split('_')[1]
        #print([sub,run])
        if sub not in trial_dict:
            trial_dict[sub] = {"REWARD_FILES": [], "PUNISH_FILES": []}
    
        trial_dict[sub][run] = {}
    
        df = pd.read_csv(file, sep="\t", header=None)
        df.columns = ["trial_num", "reinforcer"] 

        reward_trial_nums = df[df['reinforcer'] == 'reward']
        reward_trial_nums = reward_trial_nums['trial_num']
        reward_trials = reward_trial_nums.values.tolist()
        trial_dict[sub][run]["reward"] = reward_trials
    
        punish_trial_nums = df[df['reinforcer'] == 'punishment']
        punish_trial_nums = punish_trial_nums['trial_num']
        punish_trials = punish_trial_nums.values.tolist()
        trial_dict[sub][run]["punish"] = punish_trials
        #print("Reward: {} \nPunish {}".format(reward_trials, punish_trials))
    
        #reward_path=os.path.join(output_dir, '%s_%s_reward'%(sub,run))
        #punish_path=os.path.join(output_dir, '%s_%s_punish'%(sub,run))
    
        #reward_cmd_files = ['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', reward_path]
        #for a in reward_trials:
            #pe_file ='/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/feat1/betaseries/{}/{}_{}_trial-{}.feat/stats/pe1.nii.gz'.format(sub,run,sub,run, str(a))
            #reward_cmd_files.append(pe_file)
            #trial_dict[sub]["REWARD_FILES"].append(pe_file)
        #reward_cmd = ' '.join(reward_cmd_files)
        
        #print("RUNNING COMMAND.... {}".format(reward_cmd))
        #subprocess.run(reward_cmd, shell=True)
        
        #print("FILES FOUNDS: {} \n".format(pe1_files))
        #punish_cmd_files = ['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', punish_path]
        #for a in punish_trials:
            #pe_file='/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/feat1/betaseries/{}/{}_{}_trial-{}.feat/stats/pe1.nii.gz'.format(sub,run,sub,run, str(a))
            #punish_cmd_files.append(pe_file)
            #trial_dict[sub]["PUNISH_FILES"].append(pe_file)
        #punish_cmd = ' '.join(punish_cmd_files)
        #print("RUNNING COMMAND.... {}".format(punish_cmd))
        #subprocess.run(punish_cmd, shell=True)"""
    for sub in trial_dict:
        reward_path=os.path.join(output_dir, '%s_reward'%(sub))
        punish_path=os.path.join(output_dir, '%s_punish'%(sub))
        reward_files=['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', reward_path]
        punish_files=['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', punish_path]
        print(sub)
        pe1=glob.glob(os.path.join('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/feat1/betaseries/run-*/{}_run-*_trial-*.feat/stats/pe1.nii.gz'.format(sub,sub)))
        for run in trial_dict[sub]:
             # Get all available pe1 files per subject, not distinguished by runs
            for trial in trial_dict[sub][run]:
                if trial == "reward":
                    temp=[x for x in pe1 if int(x.split("/")[-3].split("_")[2].split("-")[1].split('.')[0]) in  trial_dict[sub][run][trial]]
                    for x in temp:
                        reward_files.append(x)
                else:
                    temp=[x for x in pe1 if int(x.split("/")[-3].split("_")[2].split("-")[1].split('.')[0]) in  trial_dict[sub][run][trial]]
                    for x in temp:
                        punish_files.append(x)
                        
        reward_cmd=' '.join(reward_files)
        punish_cmd=' '.join(punish_files)
        print("Running reward command........... \n{} \n\nRunning punish command......... \n{} \n\n".format(reward_cmd,punish_cmd))
        subprocess.run(reward_cmd, shell=True)
        subprocess.run(punish_cmd, shell=True)
                
            
            
            #print(reward_pe1_files)
        """punish_pe1_files=[x for x in pe1 if int(x.split("/")[-3].split("_")[2].split("-")[1].split('.')[0]) in punish_trials]
        print(punish_pe1_files)
        fsl_cmd = "/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge -t"
        #set output paths
        reward_out = os.path.join(output_dir, "{}_reward".format(sub))
        punish_out = os.path.join(output_dir, "{}_punish".format(sub))
        # print if you want to check that files separated b/w trials match original list
        #reward_files = [x.split("/")[-3] for x in trial_dict[sub]["REWARD_FILES"]]
        #punish_files = [x.split("/")[-3] for x in trial_dict[sub]["PUNISH_FILES"]]
        #print("REWARD: \t{} \n{} \nPUNISH: \t{} \n{} \n".format(reward_trials, reward_files, punish_trials, punish_files))
        reward_cmd = "{} {} {}".format(fsl_cmd, reward_out, ' '.join(trial_dict[sub]["REWARD_FILES"]))
        punish_cmd = "{} {} {}".format(fsl_cmd, punish_out, ' '.join(trial_dict[sub]["PUNISH_FILES"]))
        #print("Running command........... \n{} \nRunning command........... \n{} \n".format(reward_cmd, punish_cmd))
        #subprocess.run(reward_cmd, shell=True)
        #subprocess.run(punish_cmd, shell=True)"""

    print("Completed making individual run files.")
    
# Our main() function:
# We get initially get our inputs, we need: a path to the trial logs, 
# an output directory path, a derivatives directory path (or directorty where the subjects (sub-*) input directories are held)
# 
def main(): 
    #trial_path='/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/trial_logs'
    #output_dir = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/niftis"
    args=set_parser()
    
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    trial_dict ={}
    #print("Argument list: \n{}".format(type(args)))
    trial_path = args.trial_path #arglist['trial_path']
    nii_outpath = args.nifti_path #arglist['nifti_path']
    
    text_files = glob.glob(os.path.join(trial_path,'*sub*run*txt'))
    good_subs=[x.split("/")[-1] for x in glob.glob("/projects/niblab/bids_projects/Experiments/Bevel/derivatives/sub-0*")]
    
    #get arguments
    # get only the text files of the subjects found in good subs 
    files = [x for x in text_files if x.split("/")[-1].split("_")[0] in good_subs]
    files=sorted(files)
    #print(args.trial_path)
    # Run if we want to run fslmerge and create nifti ROI files (-roi flag)
    if args.fslmerge == True:
        print("Starting fslmerge function....")
        print(args.fslmerge)
        #concat_trials(files, trial_dict, output_dir)
    if args.fslmeants == True:
        print("Starting fslmeants function....")
        print(args.fslmeants)
        nifti_run_files=glob.glob(os.path.join(nii_outpath, "*.nii.gz"))
        file_list = glob.glob(os.path.join("/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/niftis", 'sub-0*.nii.gz'))
        print("We have {} nifti files.".format(len(file_list)))
        pool = Pool(processes=16)
        #pool.map(pull_timeseries, file_list)
        #combine_timeseries()
    
main()