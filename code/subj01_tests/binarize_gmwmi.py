from nilearn import image


def binarize_gmwmi(input_gmwmi_file, write_file=False, out_path=None):
    '''
    Sets all values > 0 in the GMWMI .nii.gz -> 1
    '''
    out = image.math_img(
        "np.where(img > 0, 1, 0)", img=input_gmwmi_file)
    if write_file:
        out_file = out_path + ".binarized.nii.gz"
        out.to_filename(out_file)
    return out


binarize_gmwmi("/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/gmwmi.nii.gz",
               True, "/Applications/freesurfer/7.3.2/subjects/subj01/fyz-out/gmwmiTEST")
