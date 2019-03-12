# Feat2 Design File Generator
# This script needs an input directory path where there are "sub-*" folders,
# and it needs the design 2 (.fsf) template file path. Then it executes the generator
# that outputs the individual "feat2/sub-XX_design.fsf" files. 


# Package Import
import glob
import os
import argparse 

# Parser setup
def set_parser():
    global arglist
    parser=argparse.ArgumentParser(description='make your fsf files')
    parser.add_argument('-task_only',dest='TASK',
                        default=False, help='make only task files?')
    parser.add_argument('-rest_only', dest='REST',
                        default=False, help='make only rest files?')
    parser.add_argument('-multi_sess', dest='MULTI_SESS',
                        default=False, help='multiple sessions, specify session with -sess flag ( else default runs all available sessions found)')
    parser.add_argument('-sess', dest='SESS',
                        default=False, help='session to run on') # make so it can hold list
    parser.add_argument('-design_file',dest='TEMPLATE',
                        default=False, help='path of feat2 design file template?(.fsf)')
    parser.add_argument('-input_dir ',dest='INDIR',
                        default=False, help='please enter your input directory path, should be ~/derivatives path')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
        




    
def write_fsf(sub_dir):

    subject_id = sub_dir.split("/")[-1]
    
    #check for existence of feat2 directory
    FEAT2_DIR = os.path.join(sub_dir, "func/Analysis/feat2")
    if os.path.exists(FEAT2_DIR):
        pass
    else:
        os.makedirs(FEAT2_DIR)
        
    print("> WRITING FILE......")
    
    # Get input feat1 directories 
    # -- add cases here to do various tasks and rest files
    #if arglist["REST"] == True:
        
    if arglist["TASK"] == True:
        out_dir_name = "%s_tasks"%subject_id
        FEATS_PATH = os.path.join(sub_dir, "func/Analysis/feat1/*task*.feat") # add key here to grab unique file
        FEATS = glob.glob(FEATS_PATH)
    
        # Open design template file and replace OUTPATH and the INPUTDIRS
        with open(DESIGN_FILE, 'r') as infile:
            tempfsf=infile.read()
            outpath = os.path.join(sub, "func/Analysis/feat2", out_dir_name)
            print(">SETTING DESIGN OUTPATH: ", outpath)
            tempfsf = tempfsf.replace("OUTPUT", outpath)
            
            # Currently script loops through feat directories and assigns to input by index
            for index,feat_path in enumerate(FEATS):
                feat_id = "FEAT%s"%(index+1)
                print("> %s : %s"%(feat_id, feat_path))
                tempfsf = tempfsf.replace(feat_id, feat_path)
            OUTFILE_PATH = os.path.join(FEAT2_DIR, "%s_design_tasks.fsf"%subject_id)
            print("> OUTFILE: ", OUTFILE_PATH)
            with open(OUTFILE_PATH, "w") as outfile:
                outfile.write(tempfsf)
            outfile.close()
        infile.close()
    
# Main Function
def main():
    set_parser()
    
    # SET PATHS 
    DER_DIR = arglist["INDIR"]
    DESIGN_FILE = ""

    # GET SUBJECT DIRECTORIES -- add case for multiple sessions
    SUB_DIRS = sorted(glob.glob(os.path.join(DER_DIR, "sub-*")))
    
    # Loop through subjects and make the design file
    for sub_dir in SUB_DIRS:
        write_fsf(sub_dir)
main()