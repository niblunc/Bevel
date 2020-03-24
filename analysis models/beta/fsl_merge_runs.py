import os
import glob
import numpy as np
import pandas as pd
import pdb
import csv


basepath='/Users/jennygilbert/Documents/betaseries_bevel/concatenate/trial_logs'
os.chdir(basepath)

# loop through subject files
for file in glob.glob(os.path.join(basepath,'sub*.txt')):
    #print(file)

    # get identifiers 
    sub=file.split('/')[7].split('_')[0]
    run=file.split('/')[7].split('_')[1]
    #print([sub,run])
    
    # load file into pandas dataframe 
    df = pd.read_csv(file, sep="\t", header=None)
    df.columns = ["trial_num", "reinforcer"] 
    #pdb.set_trace()
    
    reward_trial_nums = df[df['reinforcer'] == 'reward']
    reward_trial_nums = reward_trial_nums['trial_num']
    reward_trials = reward_trial_nums.values.tolist()
    
    punish_trial_nums = df[df['reinforcer'] == 'punishment']
    punish_trial_nums = punish_trial_nums['trial_num']
    punish_trials = punish_trial_nums.values.tolist()
    
    path1='/Users/jennygilbert/Documents/betaseries_bevel/concatenate/%s_%s_reward.txt'%(sub,run) 
    path2='/Users/jennygilbert/Documents/betaseries_bevel/concatenate/%s_%s_punish.txt'%(sub,run)
    
    f_make=open(path1, 'w')
    f_make.write('/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge -t /projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/concatenated/'+ sub + '_' + run + '_reward ')
    for a in reward_trials:
        f_make.write('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/'+ sub +'/func/Analysis/feat1/betaseries/'+ run +'/'+ sub + '_' + run + '_trial-' + str(a)+'.feat/stats/pe1.nii.gz'+' ')
    f_make.close()
    
    f_make=open(path2, 'w')
    f_make.write('/projects/niblab/modules/software/fsl/5.0.10/bin/fslmerge -t /projects/niblab/bids_projects/Experiments/Bevel/derivatives/betaseries/concatenated/'+ sub + '_' + run +'_punish ')
    for a in reward_trials:
        f_make.write('/projects/niblab/bids_projects/Experiments/Bevel/derivatives/'+ sub +'/func/Analysis/feat1/betaseries/'+ run +'/'+ sub + '_' + run + '_trial-' + str(a)+'.feat/stats/pe1.nii.gz'+' ')
    f_make.close()
    
    
filenames = os.listdir('/Users/jennygilbert/Documents/betaseries_bevel/concatenate/command_in_txt/')
content = ''
for f in filenames:
    content = content + '\n' + open(f).read()
open('joined_file.txt','wb').write(content)