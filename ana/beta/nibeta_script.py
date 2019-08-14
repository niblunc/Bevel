import os, glob  # interact with the filesystem
from subprocess import Popen, PIPE, STDOUT  # enable calling commandline
import matplotlib.pyplot as plt  # manipulate figures
import seaborn as sns  # display results
import pandas as pd   # manipulate tabular 
import warnings
import time
from multiprocessing import Pool
from functools import partial
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=UserWarning) 
warnings.filterwarnings("ignore", category=ResourceWarning) 





def get_parcellation(data_dir):
    atlas_txt = os.path.join(data_dir, 'derivatives', 'parcellations','WashU_300rois_order_new.txt')
    atlas_df = pd.read_csv(atlas_txt, sep="\t")
    atlas_df.head()

    atlas_df.drop(['network', 'x_coord', 'y_coord', 'z_coord'], axis='columns', inplace=True)
    atlas_df.tail()

    atlas_df = atlas_df.append({'index' : '300', 'regions' : 'pHippocampusL'}, ignore_index=True)
    print("Atlas Dataframe Tail End \n{tail_df}".format(tail_df=atlas_df.tail))
    atlas_tsv = atlas_txt.replace(".txt", ".tsv")
    atlas_df.to_csv(atlas_tsv, sep="\t", index=False)
    
    return atlas_tsv



"""def make_output(_dict, sub_id):
    corr_mat_path = os.path.join(_dict['out_dir'], "NiBetaSeries", "nibetaseries", sub_id, "func")
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
            print("FINISHED")"""


# call nibs
def run_nibeta(_dict, data):
    sub_string = ' '.join(data)
    print(sub_string)
    
    cmd = """\
    nibs \
    {bids_dir} \
    fmriprep \
    {out_dir} \
    participant \
    --participant_label {subjects} \
    -sm 6 \
    -c CSF FramewiseDisplacement X Y Z RotX RotY RotZ \
    -sp MNI152NLin2009cAsym \
    -t prob \
    -w {work_dir} \
    -a {atlas_mni_file} \
    -l {atlas_tsv} \
    --nthreads 16
    """.format(subjects=sub_string,
           atlas_mni_file=_dict['atlas_mni_file'],
           atlas_tsv=_dict['atlas_tsv'],
           bids_dir=_dict['data_dir'],
           out_dir=_dict['out_dir'],
           work_dir=_dict['work_dir'])
    print("CMD: \n{}".format(cmd))
    
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line)
    print("FINISHED SET: \n{}".format(data))


    


def main():
    # get subjects 
    # get our data directories and the list of subjects     
    # when getting list of subjects we want to get batches 
    # can either get input from USER or we can grab from DIR
    # here we are grabbing from BIDS dir and running subjects
    # -- want to do batches (parallel or ?)
    
    data_dir ='/projects/niblab/bids_projects/Experiments/Bevel/BIDS'
    out_dir = os.path.join(data_dir, "derivatives")
    work_dir = os.path.join(out_dir, "work_dir")
    atlas_mni_file = os.path.join(data_dir,
                              "derivatives",
                              "parcellations",
                              "WashU_300rois_MNI152Asymm_3mm_origOrder.nii")
    atlas_tsv = os.path.join(data_dir,
                              "derivatives",
                              "parcellations",
                              "WashU_300rois_order_new.tsv")
        
    dataset = [x.split('/')[-1] for x in glob.glob(os.path.join(data_dir, 'sub-*'))]
    dataset = sorted(dataset)

    #print("Dataset: \n{}".format(dataset)) 
    n=10
    chunks = [dataset[i * n:(i + 1) * n] for i in range((len(dataset) + n - 1) // n )]  
    for i,chunk in enumerate(chunks):
        print("Chunk {}: \n{}".format(i,' '.join(chunk)))
    # Get parcellation
    #atlas_tsv = get_parcellation(data_dir)
    
    # Get `tsvs` -- IF tsv not setup, RUN script 
    # else just GRAB tsv

    _dict = {
        'atlas_mni_file' : atlas_mni_file,
        'data_dir' : data_dir,
        'out_dir' : out_dir,
        'work_dir' : work_dir,
        'atlas_tsv' : atlas_tsv}

    p = Pool(3)
    func = partial(run_nibeta, _dict)
    p.map(func, chunks)

main()