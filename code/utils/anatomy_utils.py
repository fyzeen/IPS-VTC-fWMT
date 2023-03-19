from utils.system_utils import *
import os.path as op
from nilearn import image


def define_gmwmi(subj_freesurfer_directory, out_path):
    '''
    This function takes defines a gray matter-white matter interface from a FreeSurfer image using Hybrid Surface and
    Volume Segmentation (HSVS). This is described in greater detail elsewhere:
        * https://mrtrix.readthedocs.io/en/dev/reference/commands/5ttgen.html
        * https://www.researchgate.net/publication/342800028_Hybrid_Surface-Volume_Segmentation_for_improved_Anatomically-Constrained_Tractography

    ** NOTE: this implementation is based off of anat_to_gmwmi() in fsub_extractor **

    Inputs
    ----------
    subj_freesurfer_directory: str
        Path to subject's freesurfer directory

    out_path: str
        Path to output FOLDER (e.g., "usr/bin/hello/")

    Outputs
    ----------
    Writes 5tt.nii.gz file and gmwmi.nii.gz file in out_path

    Returns None
    '''
    fivett_out_path = op.join(out_path, "5tt.nii.gz")
    fivettgen_command = ["5ttgen", "hsvs",
                         subj_freesurfer_directory,
                         fivett_out_path,
                         "-nocrop"]
    run_command(fivettgen_command)

    gmwmi_out_path = op.join(out_path, "gmwmi.nii.gz")
    gmwmi_command = ["5tt2gmwmi", fivett_out_path, gmwmi_out_path]
    run_command(gmwmi_command)
    return None


def binarize_gmwmi(gmwmi_file, write_file=False, out_path=None, binarize_to=1):
    '''
    Sets all values > 0 in GMWMI .nii.gz (as defined by hsvs algorithm) -> 1

    Inputs 
    ----------
    gmwmi_file: str
        Path to gmwmi file (.nii.gz)

    write_file: boolean
        True if the function should write the binarized gmwmi to the specified out_path; False if not

    out_path: str
        Path to output FOLDER (e.g., "usr/bin/hello/")

    Outputs
    ----------
    Returns nilearn image with binarized gmwmi

    If write_file==True, the function will write a NIfTI file to the specified location with a binarized GMWMI
    '''
    out = image.math_img(
        "np.where(img > 0, {}, 0)".format(binarize_to), img=gmwmi_file)

    if write_file:
        write_nib_file(gmwmi_file, out_path, out, ".nii.gz", "binarized")
    return out


def concat_volumes(volume1, volume2, change_label, write_file=False, out_path=None):
    out = image.math_img("img1 + img2", img1=volume1, img2=volume2)
    if write_file:
        write_nib_file(volume1, out_path, out, ".nii.gz", change_label)
    return out
