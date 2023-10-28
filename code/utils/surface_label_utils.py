from utils.system_utils import *
import os.path as op
import numpy as np
import nibabel.freesurfer.mghformat as fsmgh
import nibabel.freesurfer.io as fsio
from nilearn import image


def threshold_rois(tval_surf_path, nsd_roi_path, threshold, write_file=False, out_path=None):
    '''
    This function takes liberally defined ROIs and thresholds them to a higher t-value

    Inputs
    ----------
    tval_surf_path: str
        Path to surface label with t-values with which liberal ROIs were defined. File should be .mgz or .mgh (in vertex space)

    nsd_roi_path: str
        Path to surface label with liberal ROI definitions. File should be .mgz or .mgh (in vertex space)

    threshold: int
        t-value to which each ROI should be thresholded

    write_file: boolean
        True if the function should write new file with thresholded ROIs; False if not.

    out_path: str
        Path to output FOLDER (e.g., "usr/bin/hello/")

    Outputs
    ----------
    Returns nibabel freesurfer object with thresholded ROIs

    If write_file==True, the function will write a .mgz file to the specified location with thresholded surface ROIs
    '''

    tval_mgz = fsmgh.load(tval_surf_path)
    tval_array = np.asarray(tval_mgz.dataobj)
    thresholded_tval_array = np.where(tval_array >= threshold, tval_array, 0)

    nsd_roi_mgz = fsmgh.load(nsd_roi_path)
    nsd_roi_array = np.asarray(nsd_roi_mgz.dataobj)
    for i in np.unique(nsd_roi_array):
        filter_array = np.where(nsd_roi_array == i, 1, 0)
        filtered_tval = thresholded_tval_array * filter_array
        new_roi_array = np.where(filtered_tval != 0, i, 0)
        if i == 0:
            thresholded_rois_array = new_roi_array
        else:
            thresholded_rois_array += new_roi_array

    thresholded_rois = fsmgh.MGHImage(
        thresholded_rois_array, tval_mgz.affine, header=tval_mgz.header, extra=tval_mgz.extra)

    if write_file:
        change_label = f"thresholded{threshold}"
        write_nib_file(nsd_roi_path, out_path,
                       thresholded_rois, ".mgz", change_label)

    return thresholded_rois


def surfROI_to_WM(surface_roi_path, aseg_path, hemi, subject, out_path):
    '''
    This function takes an ROI map on a freesurfer surface (vertex space) and projects it into the white matter
    ** NOTE: implementation based off of project_roi() in fsub_extractor **

    Inputs
    ----------
    surface_roi_path: str
        Path to surface ROI (.mgz or .mgh file (in vertex space))

    aseg_path: str
        Path to subject's aseg.mgz file (a FreeSurfer output)

    hemi: str
        "rh" or "lh"

    subject: str
        Name of subject in FreeSurfer subjects director (e.g., "subj01")

    out_path: str
        Path to output FOLDER (e.g., "usr/bin/hello/")

    Outputs
    ----------
    Creates a .nii.gz file in specified location with surface ROIs projected to white matter

    Returns path to created file
    '''
    file_name = surface_roi_path.replace(".mgz", ".projected.nii.gz")
    file_name = op.basename(file_name)
    out_file = op.join(out_path, file_name)

    command = ["mri_surf2vol",
               "--surfval", surface_roi_path,
               "--template", aseg_path,
               "--hemi", hemi,
               "--subject", subject,
               "--identity", subject,
               "--fill-projfrac", "-2", "0", "0.05",
               "--o", out_file]

    run_command(command)

    return out_file


def intersect_roi_gmwmi(roi_file, gmwmi_file, write_file=False, out_path=None):
    '''
    Intersects white matter-projected ROI with binarized GMWMI. Defines ROI restricted to GMWMI.

    Inputs
    ----------
    roi_file: str
        Path to file contianing ROIs projected into white matter

    gmwmi_file: str
        Path to file contianing whole-brain GMWMI (as defined by hsvs algorithm)

    write_file: boolean
        True if the function should write new NIfTI file with GMWMI-restricted ROIs; False if not

    out_path: str
        Path to output FOLDER (e.g., "usr/bin/hello/")

    Outputs
    ----------
    Returns nibabel object with GMWMI-restricted ROIs

    If write_file==True, the function will write a NIfTI file to the specified location with ROIs restricted to GMWMI
    '''
    out = image.math_img("img1 * img2", img1=gmwmi_file, img2=roi_file)
    if write_file:
        write_nib_file(roi_file, out_path, out, ".nii.gz", "gmwmi_intersected")
    return out


def subset_rois(roi_list, input_roi_file, type, write_file=False, out_path=None, name="subsetted"):
    '''
    This function takes ROI labels in a brain volume (NIfTI file) and subsets the labeled to ROIs to only those of interest.
    Labels in the volume must be integers.

    Inputs
    ----------
    roi_list: list of ints
        List of integer labels in the volume ROI that correspond with ROIs you would like to keep.

    input_roi_file: str
        Path to input NIfTI file with ROI labels

    type: str
        .mgz or .nii.gz

    write_file: boolean
        True if the function should write new NIfTI file with subsetted ROIs; False if not.

    out_path: str
        Path to output FOLDER (e.g., "usr/bin/hello/")

    Outputs
    ----------
    Returns the nibabel image object with subsetted ROIs

    If write_file==True, the function will write a NIfTI file to the specified location with subsetted ROI labels
    '''
    if type == ".nii.gz":
        out_img = image.math_img(
            "np.where(np.isin(img, {}), img, 0)".format(roi_list), img=input_roi_file)
    elif type == ".mgz":
        input = fsmgh.load(input_roi_file)
        input_array = np.asarray(input.dataobj)
        out_array = np.where(np.isin(input_array, roi_list), input_array, 0)
        out_img = fsmgh.MGHImage(out_array, input.affine,
                                 header=input.header, extra=input.extra)
    if write_file:
        write_nib_file(input_roi_file, out_path, out_img, type, name)

    return out_img


def smooth_surf_labels(surf_path, out_path, freesurfer_subj, hemi):
    file_name = surf_path.replace(".mgz", ".smoothed.mgz")
    file_name = op.basename(file_name)
    out_file = op.join(out_path, file_name)

    smoothing_command = ["mri_surf2surf",
                         "--srcsurfval", surf_path,
                         "--srcsubject", freesurfer_subj,
                         "--trgsubject", freesurfer_subj,
                         "--trgsurfval", out_file,
                         "--hemi", hemi,
                         "--nsmooth-out", "7"]
    run_command(smoothing_command)
    return None


def available_floc_rois(surf_labels_path):
    #floc_faces_labels = {1: "OFA", 2: "FFA1", 3: "FFA2"}
    floc_words_labels = {1: "OWFA", 2:"VWFA-1", 3:"VWFA-2"}
    input = fsmgh.load(surf_labels_path)
    input_array = np.asarray(input.dataobj)
    check = np.unique(input_array)
    out = [floc_words_labels[i] for i in check if i in floc_words_labels]
    out_nums = [i for i in check if i in floc_words_labels]
    return out, out_nums


def intersect_surf_labels(label_path, roi_path, write_file=False, out_path=None, change_label="roi-intersected"):
    label = fsmgh.load(label_path)
    label_array = np.asarray(label.dataobj)
    roi = fsmgh.load(roi_path)
    roi_array = np.asarray(roi.dataobj)

    roi_array = np.where(roi_array > 0, 1, 0)
    out_array = label_array * roi_array

    out = fsmgh.MGHImage(
        out_array, label.affine, header=label.header, extra=label.extra)

    if write_file:
        write_nib_file(label_path, out_path,
                       out, ".mgz", change_label)

    return out


def concat_surflabels(label1_path, label2_path, write_file=False, out_path=None, change_label="concatenated"):
    label1 = fsmgh.load(label1_path)
    label1_array = np.asarray(label1.dataobj)
    label2 = fsmgh.load(label2_path)
    label2_array = np.asarray(label2.dataobj)

    out_array = label1_array + label2_array
    out = fsmgh.MGHImage(out_array, label1.affine,
                         header=label1.header, extra=label1.extra)

    if write_file:
        write_nib_file(label1_path, out_path,
                       out, ".mgz", change_label)

    return out, out_array


def de_intersect_surflabels(label_path, roi_path, write_file=False, out_path=None, change_label="cleaned"):
    label = fsio.read_label(label_path)  # this must be a .label file
    roi_img = fsmgh.load(roi_path)
    roi_img_array = np.asarray(roi_img.dataobj)
    roi_img_array[label] = 0

    out = fsmgh.MGHImage(roi_img_array, roi_img.affine,
                         header=roi_img.header, extra=roi_img.extra)

    if write_file:
        write_nib_file(roi_path, out_path,
                       out, ".mgz", change_label)

    return out, roi_img_array
