import os, glob

# get directory

bids_deriv_dir = '/projects/niblab/bids_projects/Experiments/Bevel/BIDS/derivatives'

subjects = glob.glob(os.path.join(bids_deriv_dir, "NiBetaSeries/nibetaseries/sub-*"))

subjects = sorted(subjects)

print(subjects)

for beta_dir in subjects:
    tsvs = glob.glob(os.path.join(beta_dir, "func/*.tsv"))
    runs = [x.split("/")[-1].split("_")[2] for x in tsvs]
    #print("RUNS : {} ".format(' '.join(runs)))
    if len(runs) != 8:
        print(beta_dir.split("/")[-1])
        print("RUNS PRODUCED: \n{} ", (' '.join(runs)))