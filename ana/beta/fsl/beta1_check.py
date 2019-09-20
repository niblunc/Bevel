import os, glob
import pandas as pd

beta_dict={}
rerun_subs = []

subs=glob.glob(os.path.join('/projects/niblab/bids_projects/Experiments/Bevel/derivatives', 'sub-*'))
sub_ids = [x.split('/')[-1] for x in subs]
for sub in sorted(subs):
    sub_id = sub.split("/")[-1]
    if sub_id not in beta_dict:
        beta_dict[sub_id] = {}
    feat_dirs = glob.glob(os.path.join(sub,"func/Analysis/feat1/betaseries/run-*/*_run-*_trial-*.feat/stats"))
    total_trial_ct = len(feat_dirs)
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
    if total_trial_ct == 0:
        print("\n*ID: {} \tTrial Count: {}".format(sub_id, total_trial_ct))
        rerun_subs.append(sub_id)
    run_ct = 0
    if run1_trial_ct != 0:
        run_ct += 1
    if run2_trial_ct != 0:
        run_ct += 1
    if run3_trial_ct != 0:
        run_ct += 1
    if run4_trial_ct != 0:
        run_ct += 1
    beta_dict[sub_id]["TOTAL_RUNS_CT"] = run_ct
    
df=pd.DataFrame(beta_dict)
df=df.T

zero1=df["RUN1_TRIALS_CT"] == 0
zero2=df["RUN2_TRIALS_CT"] == 0
zero3=df["RUN3_TRIALS_CT"] == 0
zero4=df["RUN4_TRIALS_CT"] == 0
notzero1=df["RUN1_TRIALS_CT"] != 0
notzero2=df["RUN2_TRIALS_CT"] != 0
notzero3=df["RUN3_TRIALS_CT"] != 0
notzero4=df["RUN4_TRIALS_CT"] != 0


zero_df = df[zero1 & zero2 & zero3 & zero4]

all_zero_df = df[zero1 & zero2 & zero3 & zero4]
zero_df = df[zero1 | zero2 | zero3 | zero4]
notzero_df1 =  df[notzero1 & notzero2 & notzero3 & notzero4]
notzero_df2 =  df[notzero1 & notzero2 & notzero3 | notzero4]
notzero_df3 =  df[notzero1 & notzero2 | notzero3 | notzero4]


# list of subjects with trials done for all 4 runs - 
all_runs_list = notzero_df1.index.tolist()
missing_runs_list = [x for x in sub_ids if x not in all_runs_list]

index = ["RUN1_TRIALS_CT", "RUN2_TRIALS_CT", "RUN3_TRIALS_CT", "RUN4_TRIALS_CT", "TOTAL_TRIALS_CT"]
df_mia = pd.DataFrame(index=index, columns=missing_runs_list)
df_T = df.T
for x in sorted(missing_runs_list):
    df_mia[x] = df_T[x]
df_mia.sort_index(axis=1, inplace=True)

df_mia.T.to_csv("inspect.csv", sep="\t")
df.to_csv("trial_count.csv", sep="\t")
all_zero_df.to_csv("zero_trials.csv", sep="\t")
