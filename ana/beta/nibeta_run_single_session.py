# Run One Subject

# run-4s become run-3
 ['sub-005', 'sub-014', 'sub-018', 'sub-022', 'sub-025', 'sub-031', 'sub-032', 'sub-034', 
  'sub-035', 
  'sub-037', 'sub-038', 'sub-039', 'sub-042', 'sub-043',
  'sub-044', 'sub-045', 'sub-046', 'sub-048', 'sub-050', 
  'sub-056', 'sub-058', 'sub-061', 'sub-062', 'sub-063', 
  
  'sub-064', 'sub-065', 'sub-066', 'sub-067', 'sub-068', 
  'sub-069', 'sub-070', 'sub-071', 'sub-072', 'sub-073', 
  'sub-075', 'sub-076', 'sub-077', 'sub-079', 'sub-080',
  'sub-082', 'sub-083', 'sub-084', 'sub-085', 'sub-086', 
  'sub-089', 'sub-090'] 
    
    
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



subs=['sub-035']
subs = [x.split("-")[1] for x in subs]


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
    
