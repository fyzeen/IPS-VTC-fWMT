from dipy.tracking import life
from dipy.io.streamline import load_tck
import os.path as op
import numpy as np

subjects_dir = "/Applications/freesurfer/7.3.2/subjects"
diffusion_path = op.join(subjects_dir, "subj01", "fyz",
                         "anatomy", "diffusion", "run1")
bvec_path = op.join(diffusion_path, "dwi.bvecs")
tracks_path = op.join(diffusion_path, "vof.tck")
dwi_path = op.join(diffusion_path, "dwi.nii.gz")

#model = life.FiberModel(bvec_path)
#fit = model.fit(dwi_path, tracks_path, np.identity(4))


# HAVING THiS VERY WIERD LENGTH ISSUE WHEN TRYING TO FIT THE BETAS
tck_loaded = load_tck(tracks_path, dwi_path, bbox_valid_check=False)

print(len(tck_loaded[0]))
