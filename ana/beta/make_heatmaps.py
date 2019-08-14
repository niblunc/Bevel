import os, import 


def make_output(sub_id, corr_mat_path):
    trial_types = ['punish','reward']
    filename_template = "{sub_id}_task-prob_run-*_bold_space-MNI152NLin2009cAsym_preproc_trialtype-{trial_type}_matrix.tsv"
    for trial_type in trial_types:
        file_path = os.path.join(corr_mat_path, filename_template.format(trial_type=trial_type, sub_id=sub_id))
        #print(file_path)
        tsvs=glob.glob(file_path)
        print("TSV STEP")
        for tsv in tsvs:
            run_id = tsv.split("/")[-1].split("_")[2]
            fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True, figsize=(10, 30),
            gridspec_kw={'wspace': 0.025, 'hspace': 0.075})
            cbar_ax = fig.add_axes([.91, .3, .03, .4])
            r = 0

            for trial_type, df in pd_dict.items():
                g = sns.heatmap(df, ax=axes[r], vmin=-.5, vmax=1., square=True,
                cbar=True, cbar_ax=cbar_ax, cmap="PiYG")
                axes[r].set_title(trial_type)
                # iterate over rows
                r += 1
            #plt.tight_layout()
            plt.savefig(os.path.join(corr_mat_path, "{}_task_heatmap.png".format(run)))
            print("FINISHED")
            
# Main Function to initiate 
def main():
    # go through subjects to collect dataframe from tsv and make heatmap
    # need subject, run, and sub path
    dataset = glob.glob("/projects/niblab/bids_projects/Experiments/Bevel/BIDS/sub-*")
    for sub_dir in sorted(dataset):
        # Get IDs
        #run_id = 
        sub_id = sub_dir.split("/")[-1]
        # Get path
        corr_mat_path = os.path.join("/projects/niblab/bids_projects/Experiments/Bevel/derivatives", "NiBetaSeries/nibetaseries", sub_id, "func")
        make_output(sub_id)