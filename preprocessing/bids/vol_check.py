import glob, os
import subprocess
import shutil

# MAKE EXECUTABLE AS SCRIPT --


path="/projects/niblab/bids_projects/Experiments/Bevel/remake_space/test"
bad_files=[]
ALL_RUN_FUNCS=glob.glob(os.path.join(path, "sub-*/func/*run-*nii.gz"))
for func in ALL_RUN_FUNCS:
    vol = int(subprocess.check_output(['fslnvols', func]))
    if vol != 199:
        bad_files.append(func)
        

print("OUT OF {} RUN FILES, {} HAVE BAD VOLUMES".format(len(ALL_RUN_FUNCS),len(bad_files)))

bad_path = "/projects/niblab/bids_projects/Experiments/Bevel/remake_space/test/derivatives/bad_vol_runs"
for bad_file in sorted(bad_files):
    print("FILE {}".format(bad_file))
    #move bad file **delete later 
    sub_id = bad_file.split("/")[-3]
    bad_run_id = bad_file.split("/")[-1].split("_")[2]
    bad_run_files=glob.glob(os.path.join(path, sub_id, "func/*{}*".format(bad_run_id)))
    for file in bad_run_files:
        try:
            shutil.move(file, bad_path)
        except:
            print("ERROR")
    
for sub_path in sorted(glob.glob(os.path.join(path, "sub-002/func"))):
    print("ID: {}".format(sub_path.split("/")[-2]))
    run_1_files = glob.glob(os.path.join(sub_path, "*run-1*"))
    run_2_files = glob.glob(os.path.join(sub_path, "*run-2*"))
    run_3_files = glob.glob(os.path.join(sub_path, "*run-3*"))
    run_4_files = glob.glob(os.path.join(sub_path, "*run-4*"))
    run_5_files = glob.glob(os.path.join(sub_path, "*run-5*"))
        
    print("RUN 1: {} \nRUN 2: {} \nRUN 3: {} \nRUN 4: {} \nRUN 5: {}".format(len(run_1_files), run_2_files, run_3_files, run_4_files, run_5_files))