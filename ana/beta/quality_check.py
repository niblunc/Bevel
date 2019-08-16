import os, glob

# get directory

bids_deriv_dir = '/projects/niblab/bids_projects/Experiments/Bevel/BIDS/derivatives'

subjects = glob.glob(os.path.join(bids_deriv_dir, "NiBetaSeries/nibetaseries/sub-*"))

subjects = sorted(subjects)
sub_err_list = []
print(subjects)

for beta_dir in subjects:
    sub_id = beta_dir.split("/")[-1]
    tsvs = glob.glob(os.path.join(beta_dir, "func/*.tsv"))
    runs = [x.split("/")[-1].split("_")[2] for x in tsvs]
    #print("RUNS : {} ".format(' '.join(runs)))
    if len(runs) != 8:
        print("CHECK SUBJECT: \n{}".format(beta_dir.split("/")[-1]))
        print("RUNS PRODUCED: \n{} ".format(' '.join(runs)))
        sub_err_list.append(sub_id)
        
        
n=10
chunks = [sub_err_list[i * n:(i + 1) * n] for i in range((len(sub_err_list) + n - 1) // n )]  
for i,chunk in enumerate(chunks):
    print("Chunk {}: \n{}".format(i,' '.join(chunk)))
    
print("STRING ERROR LIST \n", sub_err_list )