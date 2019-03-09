import glob
import os
DER_DIR = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives"
SUB_DIR = "/projects/niblab/bids_projects/Experiments/Bevel/derivatives/sub-*"
SUB_DIRS = glob.glob(SUB_DIR)

for sub in SUB_DIRS:
    subject = sub.split("/")[-1]
    #check for existence of feat2 directory
    FEAT2_DIR = os.path.join(sub, "func/Analysis/feat2")
    if os.path.exists(FEAT2_DIR):
        pass
    else:
        os.makedirs(FEAT2_DIR)
    print("> STARTING PROGRAM......")
    print("----------------------->>>>SUBJECT: ",sub)
    FEATS_PATH = os.path.join(sub, "func/Analysis/feat1/*.feat")
    FEATS = sorted(glob.glob(FEATS_PATH))
    with open(os.path.join(DER_DIR, "design_files/design2.fsf"), 'r') as infile:
        tempfsf=infile.read()
        # set outpath for fsf OUTPATH variable, by run
        subID =  sub.split("/")[-1]
        outpath = os.path.join(sub, "func/Analysis/feat2", subID)
        print(">>>>>>>>>>>>>>>>>SETTING DESIGN OUTPATH: ", outpath)
        tempfsf = tempfsf.replace("OUTPUT", outpath)
        print(FEATS)
        for index,feat_path in enumerate(FEATS):
            feat_id = "FEAT%s"%(index+1)
            print("> %s : %s"%(feat_id, feat_path))
            tempfsf = tempfsf.replace(feat_id, feat_path)
        OUTFILE_PATH = os.path.join(FEAT2_DIR, "%s_design.fsf"%subject)
        print("OUTFILE ------------------------>>>> ", OUTFILE_PATH)
        with open(OUTFILE_PATH, "w") as outfile:
            outfile.write(tempfsf)
        outfile.close()
    infile.close()