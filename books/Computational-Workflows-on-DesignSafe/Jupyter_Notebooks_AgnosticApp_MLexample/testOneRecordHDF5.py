import h5py
h5="/home/jupyter/Work/stampede3/Datasets/NGAWest2/NGAWest2_TimeSeriesOnly_byRSN_AT2_260115.hdf5"
with h5py.File(h5,"r") as f:
    print("/RSN19923" in f)
    # list a few dataset names in that group
    g=f["/RSN19923"]
    print(list(g.keys())[:10])
