import os.path as op
import numpy as np
import nibabel as nib
from dipy.data import gradient_table
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.tracking import life
from utils.diffusion_utils import *

'''
# Define anatomy for streamline
subjects_dir = "/Applications/freesurfer/7.3.2/subjects"
diffusion_path = op.join(subjects_dir, "subj01", "fyz",
                         "anatomy", "diffusion", "run1")

intersect_tck_with_rois(op.join(diffusion_path, "track-merged.tck"), op.join(
    subjects_dir, "subj01", "fyz", "anatomy", "volumes", "IPS+VTC.t>0.wholebrain.nii.gz"), op.join(diffusion_path, "LiFE"), "1", forLiFESubsetting=True)
'''

subjects_dir = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/data/freesurfer"
diffusion_path = "/home/surly-raid1/kendrick-data/nsd/nsddata_diffusion/ppdata/subj01/run_1/"

bvec_path = op.join(diffusion_path, "dwi", "dwi.bvecs")
bval_path = op.join(diffusion_path, "dwi", "dwi.bvals")
dwi_path = op.join(diffusion_path, "dwi", "dwi.nii.gz")
tracks_path = op.join(subjects_dir, "subj01", "fyz",
                      "anatomy", "diffusion", "run1", "LiFE", "node1.tck")

print("loaded all paths")

gtab = gradient_table(bval_path, bvec_path)

print("loaded gtab")

# get DWI data into 4D array
dwi = nib.load(dwi_path)
dwi_array = dwi.get_fdata()

print("loaded dwi")

sft = load_tractogram(tracks_path, dwi_path)
streamlines = sft.streamlines

print("loaded streamlines")

model = life.FiberModel(gtab)
fit = model.fit(dwi_array, streamlines, np.identity(4))

print("fit streamlines model")

model_prediction = fit.predict(bvec_path)
out_tracks = streamlines[fit.beta > 0]

print("subsetted tracks")

out_sft = StatefulTractogram(out_tracks, dwi_path, Space.VOX)

print("created out_sft from out_tracks")

save_tractogram(out_sft, "~/IPS-VTC-fWMT/subj01_life.tck")

print("saved tracks")