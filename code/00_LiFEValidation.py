##### UNUSED SCRIPT #####


import os.path as op
import numpy as np
from dipy.core.gradients import gradient_table
from dipy.io.gradients import read_bvals_bvecs
from dipy.io.image import load_nifti
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
# If using node1.tck: 
    #tracks_path = op.join(subjects_dir, "subj01", "fyz", "anatomy", "diffusion", "run1", "LiFE", "node1.tck")
tracks_path = op.join(subjects_dir, "subj01", "fyz", "run1", "lh", "all", "t>3", "track-merged", "node2-19.tck")

print("loaded all paths")


bvals, bvecs = read_bvals_bvecs(bval_path, bvec_path)
gtab = gradient_table(bvals, bvecs)

print("loaded gtab")

# get DWI data into 4D array
dwi_data, affine, dwi_img = load_nifti(dwi_path, return_img=True)

print("loaded dwi")

sft = load_tractogram(tracks_path, dwi_path)
streamlines = sft.streamlines

print("loaded streamlines")

model = life.FiberModel(gtab)
fit = model.fit(dwi_data, streamlines, np.identity(4))

print("fit streamlines model")

#model_prediction = fit.predict(gtab)
out_tracks = streamlines[fit.beta > 0]

print("subsetted tracks")

print("Numeber remaining streamlines = " + str(len(out_tracks)))

out_sft = StatefulTractogram(out_tracks, dwi_path, Space.VOX)

print("created out_sft from out_tracks")

save_tractogram(out_sft, "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/node2-19_LiFE.tck", bbox_valid_check=False)

print("saved tracks")


from utils.streamline_to_surface_utils import *
from utils.surface_label_utils import *

T1_path = op.join("/home/surly-raid1/kendrick-data/nsd/nsddata", "ppdata", "subj01", "anat", "T1_0pt8_masked.nii.gz")
subj_dir = op.join(subjects_dir, "subj01")
tck_path = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/"
tck = "node2-19_LiFE.tck"
subj = "subj01"
hemi = "lh"

streamlines_to_surface(op.join(tck_path, tck), T1_path, tck_path, subj, hemi)

intersect_surf_labels(op.join(tck_path, tck[:-4]+".endpoints.mgz"),
                      op.join(subj_dir, "fyz", "anatomy", hemi+"-rois",
                              "all", "kastner", hemi+".Kastner2015.subsetted.mgz"),
                      True, tck_path, "IPS-intersected")


