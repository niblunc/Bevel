import os, glob
import pandas as pd

beta_dict={}

subs=glob.glob(os.path.join('/projects/niblab/bids_projects/Experiments/Bevel/derivatives', 'sub-*'))
for sub in sorted(subs):
    sub_id = sub.split("/")[-1]
    if sub_id not in beta_dict:
        beta_dict[sub_id] = {}
    feat_dirs = glob.glob(os.path.join(sub,"func/Analysis/feat1/betaseries/run-*/*_run-*_trial-*.feat/stats"))
    total_trial_ct = len(feat_dirs)
    if total_trial_ct == 0:
        print("\n*ID: {} \tTrial Count: {}".format(sub_id, total_trial_ct))
    beta_dict[sub_id]["TOTAL_TRIALS_CT"] = total_trial_ct
    run1_trials=[x for x in feat_dirs if x.split('/')[-3] == "run-1"]
    run2_trials=[x for x in feat_dirs if x.split('/')[-3] == "run-2"]
    run3_trials=[x for x in feat_dirs if x.split('/')[-3] == "run-3"]
    run4_trials=[x for x in feat_dirs if x.split('/')[-3] == "run-4"]  
    run1_trial_ct = len(run1_trials)
    run2_trial_ct = len(run2_trials)
    run3_trial_ct = len(run3_trials)
    run4_trial_ct = len(run4_trials)
    beta_dict[sub_id]["RUN1_TRIALS_CT"] = run1_trial_ct
    beta_dict[sub_id]["RUN2_TRIALS_CT"] = run2_trial_ct
    beta_dict[sub_id]["RUN3_TRIALS_CT"] = run3_trial_ct
    beta_dict[sub_id]["RUN4_TRIALS_CT"] = run4_trial_ct
    
df=pd.DataFrame(beta_dict)
df=df.T