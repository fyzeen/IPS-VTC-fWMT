from nilearn import image


def subset_rois(roi_list, input_roi_file, write_file=False, out_path=None):
    out = image.math_img(
        "np.where(np.isin(img, {}), img, 0)".format(roi_list), img=input_roi_file)
    if write_file:
        out_file = out_path + ".subsetted.nii.gz"
        out.to_filename(out_file)
    return out


# we only want to keep 3 floc-faces ROIs: OFA, FFA-1, FFA-2. These are labeled with 1, 2, 3 (accordingly) in the floc-faces ROI files
face_rois = [1, 2, 3]

subset_rois(face_rois, "/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/rh.floc-faces.projected.nii.gz",
            True, "/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/rh.floc-faces.projected")
