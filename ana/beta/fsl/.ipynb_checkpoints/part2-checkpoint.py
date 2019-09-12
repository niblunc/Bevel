
import os
import glob
import numpy as np
import pandas as pd
import pdb
import subprocess



def pull_timeseries():
    # get nifti files
    out_dir = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/concatenated_1"
    file_list = glob.glob(os.path.join("/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/concatenated_1/by_run", '*.nii.gz'))
    print("We have {} nifti files.".format(len(file_list)))
    beta_text_file = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/betaseries_rois.txt"
    df = pd.read_csv(beta_text_file, sep="\t")
    df_T = df.T
    print(df.head())
    for nifti in file_list[:2]:
        sub_id = nifti.split("/")[-1].split("_")[0]
        sub_condition=nifti.split("/")[-1].split("_")[2].split(".")[0]
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
            print("Running shell command: {}".format(cmd))
            #subprocess.run(cmd, shell=True)
#pull_timeseries()


# *************************************************************************************



# *************************************************************************************

def concat_runs(nifti_files, outdir):
    dict_ = {}
    for nifti in sorted(nifti_files):
        #print(nifti)
        sub_id = nifti.split("/")[-1].split("_")[0]
        if sub_id not in dict_:
            dict_[sub_id] = { "reward": [], "punish": [] }
        if "reward" in nifti:
            dict_[sub_id]["reward"].append(nifti)
        else:
            dict_[sub_id]["punish"].append(nifti)
    #print(dict_)
    for sub_id in dict_:
        reward_outfile = os.path.join(outdir, "{}_{}".format(sub_id, "reward"))
        punish_outfile = os.path.join(outdir, "{}_{}".format(sub_id, "punish"))
        reward_niftis=dict_[sub_id]["reward"]
        punish_niftis=dict_[sub_id]["punish"]
        #/projects/niblab/modules/software/fsl/5.0.10/bin/
        reward_cmd = "/usr/local/fsl/bin/fslmerge -t {} {} ".format(reward_outfile, ' '.join(reward_niftis))
        punish_cmd =  "/usr/local/fsl/bin/fslmerge -t {} {}".format(punish_outfile, ' '.join(punish_niftis))
        print("RUNNING COMMANDS........\nREWARD COMMAND: {} \nPUNISH COMMAND: {}".format(reward_cmd,punish_cmd))
        subprocess.run(reward_cmd, shell=True)
        subprocess.run(punish_cmd, shell=True)
        print("Completed merging subject runs.")



# local output directory
def concat_trials(files, trial_dict, output_dir):
    #print(sub_dirs)
    
    os.chdir(output_dir)
    # make individual files
    
    for file in files:
        sub=file.split('/')[7].split('_')[0]
        run=file.split('/')[7].split('_')[1]
        print([sub,run])
        if sub not in trial_dict:
            trial_dict[sub] = {}
    
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
    
        reward_path=os.path.join(output_dir, '%s_%s_reward'%(sub,run))
        punish_path=os.path.join(output_dir, '%s_%s_punish'%(sub,run))
    
        reward_cmd_files = ['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', reward_path]
        for a in reward_trials:
            reward_cmd_files.append('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/feat1/betaseries/{}/{}_{}_trial-{}.feat/stats/pe1.nii.gz'.format(sub,run,sub,run, str(a)))
        reward_cmd = ' '.join(reward_cmd_files)
        print("RUNNING COMMAND.... {}".format(reward_cmd))
        #subprocess.run(reward_cmd, shell=True)
        
        
        punish_cmd_files = ['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', punish_path]
        for a in punish_trials:
            punish_cmd_files.append('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/feat1/betaseries/{}/{}_{}_trial-{}.feat/stats/pe1.nii.gz'.format(sub,run,sub,run, str(a)))
        punish_cmd = ' '.join(punish_cmd_files)
        print("RUNNING COMMAND.... {}".format(punish_cmd))
        #subprocess.run(punish_cmd, shell=True)"""
    
    print("Completed making individual run files.")
    

basepath='/Users/nikkibytes/Documents/niblunc/data/runs'#'/projects/niblab/bids_projects/Experiments/Bevel'
trialpath='/projects/niblab/bids_projects/Experiments/Bevel/trial_logs'
output_dir = "/Users/nikkibytes/Documents/niblunc/data/output"
#os.chdir(basepath)
text_files = glob.glob(os.path.join(trialpath,'sub*.txt'))
good_subs=['sub-001',
 'sub-002', 'sub-003', 'sub-004', 'sub-006', 'sub-007', 'sub-009', 'sub-010',
 'sub-012', 'sub-014', 'sub-016',
 'sub-017',
 'sub-018',
 'sub-019',
 'sub-020',
 'sub-021',
 'sub-022',
 'sub-024',
 'sub-025',
 'sub-026',
 'sub-027',
 'sub-028',
 'sub-029',
 'sub-031',
 'sub-032',
 'sub-034',
 'sub-037',
 'sub-038',
 'sub-040',
 'sub-042',
 'sub-043',
 'sub-045',
 'sub-046',
 'sub-048',
 'sub-054',
 'sub-056',
 'sub-058',
 'sub-060',
 'sub-061',
 'sub-063',
 'sub-064']

files = [x for x in text_files if x.split("/")[-1].split("_")[0] in good_subs]

files=sorted(files)
trial_dict = {}
#concat_trials(files, trial_dict, output_dir)
nifti_run_files=glob.glob(os.path.join(basepath, "*.nii.gz"))#"derivatives/betaseries/concatenated_1/by_run/*nii.gz"))
concat_runs(nifti_run_files, output_dir)
#timeseries_pull()