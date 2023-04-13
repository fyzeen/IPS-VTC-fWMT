from utils.system_utils import *
import numpy as np
import nibabel.freesurfer.mghformat as fsmgh


def streamlines_to_surface(tck_path, T1_path, out_path, freesurfer_subject, hemi):
    '''
    This function takes streamlines and projects each ones' endpoints to the cortical surface. The surface will count streamline ends
    multiple times (i.e., the same streamline endpoint may contribute to multiple points on the surface). 

    Inputs 
    ----------
    tck_path: str
        Path to tck file with streamlines to project onto surface

    T1_path: str
        Path to brain-masked, T1-weighted anatomical image for the subject

    out_path: str
        Path to the FOLDER for all outputs

    freesurfer_subject: str
        Name of subject in freesurfer directory

    hemi: str
        "rh" or "lh"

    Outputs
    ----------
    Writes a NIfTI file with endpoint count in each voxel (aligned with T1 anatomical volume) in location specified by user.

    Writes an .mgz file with endpoint count in each voxel projected onto the freesurfer cortical surface in location specified by user.
    '''
    endpoints_filename = op.basename(tck_path)
    endpoints_filename = endpoints_filename[:-4] + ".endpoints.nii.gz"
    tck_endpoints_path = op.join(out_path, endpoints_filename)
    tckmap_command = ["tckmap", tck_path, tck_endpoints_path,
                      "-template", T1_path,
                      "-ends_only",
                      "-contrast", "tdi",
                      "-datatype", "float32", "-force"]
    run_command(tckmap_command)

    surface_filename = op.basename(tck_endpoints_path)
    surface_filename = endpoints_filename[:-7] + ".mgz"
    surface_endpoints_path = op.join(out_path, surface_filename)
    mrivol2surf_command = ["mri_vol2surf",
                           "--src", tck_endpoints_path,
                           "--out", surface_endpoints_path,
                           "--regheader", freesurfer_subject,
                           "--hemi", hemi,
                           "--interp", "nearest",
                           "--projfrac-max", "-0.5", "0.5", "0.1"]
    run_command(mrivol2surf_command)

    return None


def label_endpoints_with_pRF_property(prf_label_path, endpoints_path):
    '''
    This function takes a surface label with pRF information at each vertex (e.g., eccentricity, size, etc.) and labels endpoints
    at the same vertex to that pRF property. 

    Inputs 
    ----------
    prf_label_path: str
        Path to .mgz or .mgh file with pRF information at each vertex

    endpoints_path: str
        Path to .mgz or .mgh file with number of streamline endpoints at each vertex

    Outputs
    ---------
    [0]: nx2 numpy array with one column storing information about pRF and the other storing information about # streamline endpoints
    [1]: int, total number of streamlines projected onto the surface (Note: this number is not equal to the number of streamlines in
        the .tck file from which the surface was generated because 1 voxel can contribute to multiple vertices.)
    '''
    prf_img = fsmgh.load(prf_label_path)
    endpoints_img = fsmgh.load(endpoints_path)

    prflabel_array = np.asarray(prf_img.dataobj)
    endpoints_array = np.asarray(endpoints_img.dataobj)

    out = np.concatenate((prflabel_array, endpoints_array), axis=1)
    total_fibers_on_surf = np.sum(endpoints_array)

    return out.sum(axis=-1), total_fibers_on_surf


def normalize_streamlines_on_surf(endpoints_path, out_path):
    '''
    This function writes a new mgz file that contains a proportion of fibers (instead of number of fibers) at each vertex on the surface

    This will be useful for group analysis.
    '''
    endpoints_img = fsmgh.load(endpoints_path)
    endpoints_array = np.asarray(endpoints_img.dataobj)
    total_fibers_on_surf = np.sum(endpoints_array)

    normalized_endpoints_array = endpoints_array / total_fibers_on_surf

    normalized_mgz = fsmgh.MGHImage(normalized_endpoints_array, endpoints_img.affine,
                                    header=endpoints_img.header, extra=endpoints_img.extra)

    change_label = "normalized"
    write_nib_file(endpoints_path, out_path,
                   normalized_mgz, ".mgz", change_label)
