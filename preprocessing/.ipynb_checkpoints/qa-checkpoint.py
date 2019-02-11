import glob, os

deriv_path = '/projects/niblab/bids_projects/Experiments/Bevel/derivatives'
fmriprep_path = '/projects/niblab/bids_projects/Experiments/Bevel/fmriprep'

qa_dict = {}
anats = []
runs = []
onsets_miss =[]
rests = []

qa_dict["SUBJECT_COUNT"] = len(glob.glob(os.path.join(deriv_path,"sub-*")))
deriv_dir = glob.glob(os.path.join(deriv_path, "sub-*"))
#fmriprep_dir = glob.glob(os.path.join(fmriprep_path, "sub-*"))
deriv_subs = []
fmriprep_subs = []

for sub_dir in deriv_dir:
    sub_id =  sub_dir.split("/")[-1]
    deriv_subs.append(sub_id)
for sub_dir in fmriprep_dir:/projects/niblab/bids_projects/Experiments/Bevel/derivatives/baddies/sub-013/func

    sub_id = sub_dir.split("/")[-1]
    fmriprep_subs.append(sub_id)
#missing = [i for i in deriv_subs if i not in fmriprep_subs] 

for sub_dir in deriv_dir:
    sub_id = sub_dir.split("/")[-1]
    anat_file = glob.glob(os.path.join(sub_dir, "anat/*"))
    if not anat_file:
        if sub_id not in qa_dict:
            qa_dict[sub_id] = {}
        qa_dict[sub_id] = {"ANAT": "missing"}
        anats.append(sub_id)
    #else:
     #   for _file in anat_file:
      #      print(_file.split("/")[-1])
    run = glob.glob(os.path.join(sub_dir, "func/*run*preproc_brain.nii.gz"))
    if not run:
        if sub_id not in qa_dict:
            qa_dict[sub_id] = {}
        qa_dict[sub_id]["FUNCS"] = "missing"
        runs.append(sub_id)
    elif len(run) != 4:
        if sub_id not in qa_dict:
            qa_dict[sub_id] = {}
        qa_dict[sub_id]["FUNCS"] = []
        runs.append(sub_id)
        for _file in run:
            run_ = _file.split("/")[-1].split("_")[2]
            qa_dict[sub_id]["FUNCS"].append(run_)
    else:
        pass
    rest = glob.glob(os.path.join(sub_dir, "func/*rest*preproc_brain.nii.gz"))
    if not rest:
        if sub_id not in qa_dict:
            qa_dict[sub_id] = {}
        qa_dict[sub_id]["RESTS"] = "missing"
        rests.append(sub_id)
    onsets = glob.glob(os.path.join(sub_dir, "func/onsets/*.txt"))
    if not onsets:
        if sub_id not in qa_dict:
            qa_dict[sub_id] = {}
        qa_dict[sub_id]["ONSETS"] = "missing"
        onsets_miss.append(sub_id)
    motion1 = glob.glob(os.path.join(sub_dir, "func/motion_assessment/*brain_confound.txt"))
    motion2 =glob.glob(os.path.join(sub_dir, "func/motion_assessment/motion_parameters/*.txt"))
    if not motion1:
        if sub_id not in qa_dict:
            qa_dict[sub_id] = {}
        qa_dict[sub_id]["CONFOUNDS"] = "missing"
    if not motion2:
        if sub_id not in qa_dict:
            qa_dict[sub_id] = {}
        qa_dict[sub_id]["MOTION_PARAMS"] = "missing"
