import glob, os
import pandas as pd
import subprocess
import argparse
from multiprocessing import Pool

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
    parser.add_argument('-nii_path',dest='nifti_path', help='path to the directory for the output nifti (.nii.gz) files.')
    parser.add_argument('-stim',dest='stim_id', help="stimulus condition id")
    
    args = parser.parse_args()

    return args

def timeseries_concat(stim_id):
    roi_dict = {}
    inpath="/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/timeseries/{}/rois".format(stim_id)
    outpath="/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/timeseries/{}/subs".format(stim_id)
    roi_dir = glob.glob(os.path.join(inpath, "*.txt"))
    #print(roi_dir)
    
    """for roi_file in sorted(roi_dir):
        sub_id = roi_file.split("/")[-1].split("_")[0]
        if sub_id not in roi_dict:
            roi_dict[sub_id] = {stim_id:[]}
        roi_df = pd.read_csv(roi_file, sep="\n", header=None)
        roi_dict[sub_id][stim_id].append(roi_df)
        #print(roi_dict)
    for sub_id in roi_dict:
        file_outpath = os.path.join(outpath, "{}_{}.txt".format(sub_id, stim_id))
        concat_df = pd.concat(roi_dict[sub_id][stim_id], axis=1, sort=False)
        print("Writing files..... \n{} \n".format(file_outpath))
        concat_df.to_csv(file_outpath, header=None, index=None, sep="\t")
        
        
    """
    
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
    print("Completed making by-subject timeseries")
    #print(roi_dict)
    
    




def fslmerge_run(files, trial_dict, nii_out, stim_id, subjects):
    """for sub in subjects:
        pe1=glob.glob(os.path.join('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/beta/run-*/{}_run-*_{}-*.feat/stats/pe1.nii.gz'.format(sub,sub, stim_id)))
        out_path=os.path.join(nii_out, '%s_%s'%(sub, stim_id))
        fslmerge_lst =['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', out_path]
        for p in pe1:
            fslmerge_lst.append(p)
        fslmerge_cmd = ' '.join(fslmerge_lst)
        print("Running fslmerge on {} for {}.......".format(sub, stim_id))
        subprocess.run(fslmerge_cmd, shell=True)
    print("Completed making ROI nifti files for {}, look for output niftis here: {} \n".format(stim_id,nii_out))
    """
    
    for file in files:
        sub=file.split('/')[-1].split('_')[0]
        run=file.split('/')[-1].split('_')[1]
        #print([sub,run])
        if sub not in trial_dict:
            trial_dict[sub] = {"REWARD_FILES": [], "PUNISH_FILES": []}
        trial_dict[sub][run] = {}
    
        df = pd.read_csv(file, sep="\t", header=None)
        df.columns = ["trial_num", "reinforcer"]
        #print(df)

        reward_trial_nums = df[df['reinforcer'] == 'reward']
        reward_trial_nums = reward_trial_nums['trial_num']
        reward_trials = reward_trial_nums.values.tolist()
        trial_dict[sub][run]["reward"] = reward_trials
    
        punish_trial_nums = df[df['reinforcer'] == 'punishment']
        punish_trial_nums = punish_trial_nums['trial_num']
        punish_trials = punish_trial_nums.values.tolist()
        trial_dict[sub][run]["punish"] = punish_trials
    #print(trial_dict)
    
    for sub in trial_dict:
        pe1=glob.glob(os.path.join('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/beta/run-*/{}_run-*_{}-*.feat/stats/pe1.nii.gz'.format(sub,sub, "rl")))
        reward_path=os.path.join(nii_out, '%s_reward'%(sub))
        punish_path=os.path.join(nii_out, '%s_punish'%(sub))
        reward_files=['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', reward_path]
        punish_files=['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', punish_path]
        #print(pe1)
        #print("PE1: {}".format(pe1))
        for run in trial_dict[sub]:
             # Get all available pe1 files per subject, not distinguished by runs
            for trial in trial_dict[sub][run]:
                if trial == "reward":
                    try:
                        #for x in pe1:
                            #print(x.split("/")[-3].split("_")[2].split("-")[1].split('.')[0])
                        temp=[x for x in pe1 if int(x.split("/")[-3].split("_")[2].split("-")[1].split('.')[0]) in  trial_dict[sub][run][trial]]
                        
                        for x in temp:
                            reward_files.append(x)
                    except:
                        print("PASSING BAD, {}".format(sub))
                else:
                    #print("PUNISH...", pe1)
                    try:
                        temp=[x for x in pe1 if int(x.split("/")[-3].split("_")[2].split("-")[1].split('.')[0]) in  trial_dict[sub][run][trial]]
                        for x in temp:
                            punish_files.append(x)
                    except:
                        print("PASSING BAD, ", sub)
                    
        reward_cmd=' '.join(reward_files)
        punish_cmd=' '.join(punish_files)
        
        print("Running reward command........... \n{} \n\nRunning punish command......... \n{} \n\n".format(reward_cmd,punish_cmd))
        subprocess.run(reward_cmd, shell=True)
        subprocess.run(punish_cmd, shell=True)
    
    
def fslmeants_run(nifti):
    print(nifti)
    # get nifti files
    stim_id = nifti.split("/")[-1].split("_")[1].split(".")[0]
    out_dir = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/timeseries/rl/rois".format(stim_id)
    # split
    beta_text_file = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/betaseries_rois.txt"
    df = pd.read_csv(beta_text_file, sep="\t")
    df_T = df.T
    #print(df.head())
    #for nifti in sorted(file_list):
    sub_id = nifti.split("/")[-1].split("_")[0]
    sub_condition=nifti.split("/")[-1].split("_")[1].split(".")[0]
    #print(sub_id, sub_condition)
    for index in df.index.values:
        roi = df.iloc[index, 0]
        x = df.iloc[index, 1]
        y = df.iloc[index, 2]
        z = df.iloc[index, 3]
        #print(region,x,y,z)
        out_path = os.path.join(out_dir, "{}_{}_{}.txt".format(sub_id, sub_condition, roi))
        #print("Output file being made: {}".fomrat(out_path))
        cmd='fslmeants -i {} -o {} -c {} {} {} --usemm \n\n'.format(nifti, out_path, x, y, z)
        print("Running shell fslmeants command X for roi {} on file: {}".format(roi, cmd))# nifti.split("/")[-1]))
        subprocess.run(cmd, shell=True)
        
    
    
def main(): 
    args = set_parser()
    print(args)
    trial_path='/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/trial_logs'
    #trial_path=str(args.trial_path)
    #nii_out=str(args.nifti_path)
    #stim_id=str(args.stim_id)
    stim_id="rl"
    nii_out = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/niftis"
    #print(str(trial_path))
    trial_dict ={}
    
    text_files = glob.glob(os.path.join(trial_path,'*sub*run*txt'))
    good_subs=[x.split("/")[-1] for x in glob.glob("/projects/niblab/bids_projects/Experiments/Bevel/derivatives/sub-0*")]
    
    #get arguments
    # get only the text files of the subjects found in good subs 
    files = [x for x in text_files if x.split("/")[-1].split("_")[0] in good_subs]
    files=sorted(files)
    
    #fslmerge_run(files, trial_dict, nii_out, stim_id, good_subs)
    if args.fslmerge == True:
        print("Starting fslmerge function....")
        fslmerge_run(files, trial_dict, nii_out, stim_id)
    #if args.fslmeants == True:
    print("Starting fslmeants function....")
    file_list = glob.glob(os.path.join(nii_out, 'sub-0*{}*.nii.gz'.format(stim_id)))
    print("We have {} nifti files.".format(len(file_list)))
    #pool = Pool(processes=2)
    #pool.map(fslmeants_run, file_list)
    timeseries_concat(stim_id)
main()