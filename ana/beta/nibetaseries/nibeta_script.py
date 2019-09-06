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
        
        print("RUNNING SUBJECT: ", sub_id)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line)

        
    


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
    
    dataset =  ['sub-001', 'sub-002', 'sub-003', 'sub-004', 'sub-005', 'sub-006', 'sub-007', 'sub-008', 'sub-009', 'sub-010', 'sub-012', 'sub-013', 'sub-014', 'sub-015', 'sub-018', 'sub-022', 'sub-025', 'sub-030', 'sub-031', 'sub-032', 'sub-034', 'sub-035', 'sub-036', 'sub-037', 'sub-038', 'sub-039', 'sub-042', 'sub-043', 'sub-044', 'sub-045', 'sub-046', 'sub-048', 'sub-050', 'sub-056', 'sub-058', 'sub-061', 'sub-062', 'sub-063', 'sub-064', 'sub-065', 'sub-066', 'sub-067', 'sub-068', 'sub-069', 'sub-070', 'sub-071', 'sub-072', 'sub-073', 'sub-075', 'sub-076', 'sub-077', 'sub-079', 'sub-080', 'sub-081', 'sub-082', 'sub-083', 'sub-084', 'sub-085', 'sub-086', 'sub-089', 'sub-090']
    #dataset = [x.split('/')[-1] for x in glob.glob(os.path.join(data_dir, 'sub-*'))]
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

