import os  # interact with the filesystem
from subprocess import Popen, PIPE, STDOUT  # enable calling commandline
import matplotlib.pyplot as plt  # manipulate figures
import seaborn as sns  # display results
import pandas as pd   # manipulate tabular 
import warnings
import time
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=UserWarning) 
warnings.filterwarnings("ignore", category=ResourceWarning) 

## Setup Paths
def set_paths(data_dir):
    out_dir = os.path.join(data_dir, "derivatives/cosines_output")
    work_dir = os.path.join(out_dir, "work_dir")
    atlas_mni_file = os.path.join(data_dir,
                              "derivatives",
                              "data",
                              "Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz")
    print('Our output directory: {}'.format(out_dir))
    print('Our working output directory: {}'.format(work_dir))

## Modify TSVs if need
# needs sub_id, task, run_id
def confound_edit(sub_id, task, run_id, data_dir):
    events_file = os.path.join(data_dir, '%s/func/%s_task-prob_%s_events.tsv'%(sub_id, sub_id, run_id))
    events_df = pd.read_csv(events_file, sep="\t", na_values="n/a")
    events_df.head()
    # Rename our original columns
    events_df.rename({"outcome": "trial_type"}, axis='columns', inplace=True)
    events_df.head()
    events_df.rename({"RT": "response_time"}, axis='columns', inplace=True)
    events_df.head()
    events_df = events_df.dropna(axis="rows")
    events_df.head()
    new_df= events_df[["onset", "duration", 'trial_type', 'response_time']]
    new_df.head()
    newfile = os.path.join(data_dir, '%s/func/%s_task-%s_%s_events.tsv'%(sub_id, sub_id, task, run_id))
    new_df.to_csv(newfile, sep="\t", na_rep="n/a", index=False)
    
    return

## Setup atlas file
def set_atlas(data_dir):
    atlas_txt = os.path.join(data_dir,
                         "derivatives",
                         "data",
                         "Schaefer2018_100Parcels_7Networks_order.txt")
    atlas_df = pd.read_csv(atlas_txt, sep="\t", header=None)
    atlas_df.head()

    atlas_df.drop([2, 3, 4, 5], axis='columns', inplace=True)
    atlas_df.head()

    atlas_df.rename({0: 'index', 1: 'regions'}, axis='columns', inplace=True)
    atlas_df.head()

    atlas_df.replace(regex={'7Networks_(.*)': '\\1'}, inplace=True)
    atlas_df.head()

    atlas_tsv = atlas_txt.replace(".txt", ".tsv")
    atlas_df.to_csv(atlas_tsv, sep="\t", index=False)
    
    return 
## Setup Command
def set_nibs():
    # Run parallel
    # 
    cmd = """\
    nibs \
    {bids_dir} \
    fmriprep \
    {out_dir} \
    participant \
    -sm 6 \
    --run_label 2 \
    -c WhiteMatter CSF X Y Z RotX RotY RotZ \
    -sp MNI152NLin2009cAsym \
    -w {work_dir} \
    -a {atlas_mni_file} \
    -l {atlas_tsv} \
    """.format(atlas_mni_file=atlas_mni_file,
           atlas_tsv=atlas_tsv,
           bids_dir=os.path.join(data_dir),
           out_dir=out_dir,
           work_dir=work_dir)

    # Since we cannot run bash commands inside this tutorial
    # we are printing the actual bash command so you can see it
    # in the output
    print("The Example Command:\n", cmd)


## Run Command
def run_nibs():
    # call nibs
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line)
    

## Fill output in dataframe
def set_output_df(sub_id):
    corr_mat_path = os.path.join(out_dir, "NiBetaSeries", "nibetaseries", "%s"%sub_id, "func")
    trial_types = ['punish','reward']
    filename_template = "%s_task-%s_%s_bold_space-MNI152NLin2009cAsym_preproc_trialtype-{trial_type}_matrix.tsv"%(sub_id, task, run_id)
    pd_dict = {}
    for trial_type in trial_types:
        file_path = os.path.join(corr_mat_path, filename_template.format(trial_type=trial_type))
        print(file_path)
        pd_dict[trial_type] = pd.read_csv(file_path, sep='\t', na_values="n/a", index_col=0)
        # display example matrix
        print(pd_dict[trial_type].head())

    return pd_dict

## Plot Heatmap 
def plot_heatmap(out_dir,run_id):
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True, figsize=(10, 30),
                         gridspec_kw={'wspace': 0.025, 'hspace': 0.075})
    cbar_ax = fig.add_axes([.91, .3, .03, .4])
    r = 0
    for trial_type, df in pd_dict.items():
        g = sns.heatmap(df, ax=axes[r], center=0, vmin=0, vmax=1., square=True,
                    cbar=True, cbar_ax=cbar_ax)
        axes[r].set_title(trial_type)
        # iterate over rows
        r += 1
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "%s_task_heatmap.png"%run_id))


def main():
    data_dir = input("Enter data dir:")
    set_paths()
