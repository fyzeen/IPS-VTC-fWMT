from nilearn import image


def intersect_roi_gmwmi(roi_file, gmwmi_file, write_file=False, out_path=None):
    '''
    Intersects projected ROI with binarized gmwmi
    '''
    out = image.math_img("img1 * img2", img1=gmwmi_file, img2=roi_file)
    if write_file:
        out_file = out_path + ".gmwmi_intersected.nii.gz"
        out.to_filename(out_file)
    return out


intersect_roi_gmwmi("/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/rh.floc-faces.projected.nii.gz", "/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/gmwmi.binarized.nii.gz",
                    True, "/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/gmwmi")

'''
Code to check dimensions of volumes before doing any voxelwise math
data = image.get_data(
    "/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/.nii.gz")
print(data.shape)
'''
