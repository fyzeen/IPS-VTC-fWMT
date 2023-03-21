import os.path as op
import numpy as np
import nibabel as nib
from dipy.tracking import life
from dipy.io.streamline import load_tck


subjects_dir = "/Applications/freesurfer/7.3.2/subjects"


diffusion_path = op.join(subjects_dir, "subj01", "fyz",
                         "anatomy", "diffusion", "run1")
bvec_path = op.join(diffusion_path, "dwi.bvecs")
tracks_path = op.join(diffusion_path, "track-merged.tck")
dwi_path = op.join(diffusion_path, "dwi.nii.gz")

# get DWI data into 4D array
#dwi = nib.load(dwi_path)
#dwi_array = dwi.get_fdata()

#model = life.FiberModel(bvec_path)
# fit = model.fit(dwi_array, tracks_path (<- THIS NEEDS TO BECOME A LIST), np.identity(4))


# HAVING THiS VERY WIERD LENGTH ISSUE WHEN TRYING TO FIT THE BETAS
#tck_loaded = load_tck(tracks_path, dwi_path, bbox_valid_check=False)

# print(list(tck_loaded))
