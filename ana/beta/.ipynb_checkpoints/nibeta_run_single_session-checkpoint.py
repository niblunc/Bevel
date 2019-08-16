# Run One Subject

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

data_dir = '/projects/niblab/bids_projects/Experiments/Bevel/BIDS' #RENCI PATH
#data_dir = '/Users/nikkibytes/Documents/niblunc/testing_beta' #LOCAL PATH
print('Our working directory: {}'.format(data_dir))

out_dir = os.path.join(data_dir, "derivatives")
work_dir = os.path.join(out_dir, "work_dir")
atlas_mni_file = os.path.join(data_dir, "derivatives", "parcellations", "WashU_300rois_MNI152_3mm_origOrder.nii")
atlas_tsv = os.path.join(data_dir, "derivatives", "parcellations", "WashU_300rois_order_new.tsv")

for sub in subs:
    try:
        cmd = """\
        nibs \
        {bids_dir} \
        fmriprep \
        {out_dir} \
        participant \
        --participant_label {sub} \
        -sm 6 \
        -t prob \
        --run_label 4 \
        -c CSF FramewiseDisplacement X Y Z RotX RotY RotZ \
        -sp MNI152NLin2009cAsym \
        -w {work_dir} \
        -a {atlas_mni_file} \
        -l {atlas_tsv} \
        --nthreads 16
        """.format(atlas_mni_file=atlas_mni_file,
           atlas_tsv=atlas_tsv,
           sub=sub,
           bids_dir=os.path.join(data_dir),
           out_dir=out_dir,
           work_dir=work_dir)

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line)
    except IndexError as e:
        print(e)
        print(sys.exc_type)   
        print('bad')
    
subs =  ['sub-002', 'sub-003', 'sub-004', 'sub-005', 'sub-006', 'sub-007', 'sub-008', 'sub-009', 'sub-010', 'sub-012', 'sub-013', 'sub-014', 'sub-015', 'sub-018', 'sub-022', 'sub-025', 'sub-030', 'sub-031', 'sub-032', 'sub-034', 'sub-035', 'sub-036', 'sub-037', 'sub-038', 'sub-039', 'sub-042', 'sub-043', 'sub-044', 'sub-045', 'sub-046', 'sub-048', 'sub-050', 'sub-056', 'sub-058', 'sub-061', 'sub-062', 'sub-063', 'sub-064', 'sub-065', 'sub-066', 'sub-067', 'sub-068', 'sub-069', 'sub-070', 'sub-071', 'sub-072', 'sub-073', 'sub-075', 'sub-076', 'sub-077', 'sub-079', 'sub-080', 'sub-081', 'sub-082', 'sub-083', 'sub-084', 'sub-085', 'sub-086', 'sub-089', 'sub-090']

subs = [x.split("-")[1] for x in subs]