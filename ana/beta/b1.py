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

cmd = """\
nibs \
{bids_dir} \
fmriprep \
{out_dir} \
participant \
--participant_label 016 040 032 044 015 051 071 072 054 014 028 070 084 039 029 073 085 \
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
           bids_dir=os.path.join(data_dir),
           out_dir=out_dir,
           work_dir=work_dir)

# call nibs

p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
try:
    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line)
except IndexError as e:
    print(e)
    print(sys.exc_type)   
    print('bad')
    
 
--run_label 1 \


 012 008 053 086 050 006 009 075 002 010 046 022 080 045 042 077 067 082 004 076 068 057 007 005 035 069 020 034 066 011 021 037 060 079 003 048 026 036 064 033 059 043 027 031 089 083 024 030 062 025 019 063 023 065 055 013 049 041 047 052 087 078 081 088