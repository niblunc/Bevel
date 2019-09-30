import glob, os
import pandas as pd
import subprocess
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
    parser.add_argument('-nii_path',dest='nifti_path', help='path to the directory for the output nifti (.nii.gz) files.')
    parser.add_argument('-stim',dest='stim_id', help="stimulus condition id")
    
    args = parser.parse_args()

    return args

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



def concat_trials(files, trial_dict, nii_out, stim_id):
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
    #print(trial_dict)
    for sub in trial_dict:
        reward_path=os.path.join(nii_out, '%s_reward_%s'%(sub, stim_id))
        punish_path=os.path.join(nii_out, '%s_punish_%s'%(sub,stim_id))
        reward_files=['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', reward_path]
        punish_files=['/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge', '-t', punish_path]
        print(sub)
        pe1=glob.glob(os.path.join('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/{}/func/Analysis/beta/run-*/{}_run-*_{}-*.feat/stats/pe1.nii.gz'.format(sub,sub, stim_id)))
        #print("PE1: {}".format(pe1))
        for run in trial_dict[sub]:
             # Get all available pe1 files per subject, not distinguished by runs
            for trial in trial_dict[sub][run]:
                if trial == "reward":
                    try:
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


    print("Completed making individual run files.")
    
    
    
def main(): 
    args = set_parser()
    print(args)
    trial_path='/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/trial_logs'
    #trial_path=str(args.trial_path)
    #nii_out=str(args.nifti_path)
    #stim_id=str(args.stim_id)
    stim_id="choice"
    nii_out = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/output/niftis"
    #print(str(trial_path))
    trial_dict ={}
    
    text_files = glob.glob(os.path.join(trial_path,'*sub*run*txt'))
    good_subs=[x.split("/")[-1] for x in glob.glob("/projects/niblab/bids_projects/Experiments/Bevel/derivatives/sub-0*")]
    
    #get arguments
    # get only the text files of the subjects found in good subs 
    files = [x for x in text_files if x.split("/")[-1].split("_")[0] in good_subs]
    files=sorted(files)
    concat_trials(files, trial_dict, nii_out, stim_id)
    """if args.fslmerge == True:
        print("Starting fslmerge function....")
        concat_trials(files, trial_dict, nii_out, stim_id)
    if args.fslmeants == True:
        print("Starting fslmeants function....")
        nifti_run_files=glob.glob(os.path.join(nii_outpath, "*.nii.gz"))
        file_list = glob.glob(os.path.join(nii_out, 'sub-0*{}*.nii.gz'.format(stim_id)))
        print("We have {} nifti files.".format(len(file_list)))
        pool = Pool(processes=16)
        pool.map(pull_timeseries, file_list)"""
        
main()