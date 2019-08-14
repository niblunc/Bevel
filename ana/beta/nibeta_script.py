# Nichollette Acosta | Jenny Sadler | Nibetaseries | NIBL 

## Currently program runs by individual subject/run
## To avoid a "global fault" we run through the loop of subjects inside python,
## not nibs command, therefore we do nib commands individually by subject

# ** Not to make more efficient and have output




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





# call nibs
def run_nibeta(_dict, data):
    sub_string = ' '.join(data)
    print(sub_string)
    
    for sub_id in sorted(data):
        cmd = """\
        nibs {bids_dir} fmriprep {out_dir} participant \
        --participant_label {subjects} -sm 6 \
        --run_label 1 -t prob -c CSF FramewiseDisplacement X Y Z RotX RotY RotZ \
        -sp MNI152NLin2009cAsym -w {work_dir} -a {atlas_mni_file} \
        -l {atlas_tsv} --nthreads 16
        """.format(subjects=sub_id,
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
    atlas_mni_file = os.path.join(data_dir, "derivatives", "parcellations", "WashU_300rois_MNI152_3mm_origOrder.nii")
    atlas_tsv = os.path.join(data_dir, "derivatives", "parcellations", "WashU_300rois_order_new.tsv")
        
    dataset = [x.split('/')[-1] for x in glob.glob(os.path.join(data_dir, 'sub-*'))]
    dataset = sorted(dataset)
    
    dataset = [x.split("-")[1] for x in dataset]

    #print("Dataset: \n{}".format(dataset)) 
    n=10
    chunks = [dataset[i * n:(i + 1) * n] for i in range((len(dataset) + n - 1) // n )]  
    for i,chunk in enumerate(chunks):
        print("Chunk {}: \n{}".format(i,' '.join(chunk)))
    # Get parcellation
    
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

