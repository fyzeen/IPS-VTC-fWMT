import numpy as np
import nibabel.freesurfer.mghformat as fsmgh


prf_label_path = "/Applications/freesurfer/7.3.2/subjects/subj01/label/rh.prfeccentricity.mgz"
endpoints_path = "/Users/fyzeen/FyzeenLocal/GitHub/IPS-VTC-fWMT/data/subj01/diffusion/vof_extraction/extracted1.mgz"


def label_endpoints_with_pRF_property(prf_label_path, endpoints_path):
    prf_img = fsmgh.load(prf_label_path)
    endpoints_img = fsmgh.load(endpoints_path)

    prflabel_array = np.asarray(prf_img.dataobj)
    endpoints_array = np.asarray(endpoints_img.dataobj)

    out = np.concatenate((prflabel_array, endpoints_array), axis=1)
    total_fibers_on_surf = np.sum(endpoints_array)

    return out, total_fibers_on_surf
