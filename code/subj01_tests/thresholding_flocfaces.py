import numpy as np
import nibabel.freesurfer.mghformat as fsmgh

mgz_path = "/Applications/freesurfer/7.3.2/subjects/subj01/label/rh.flocfacestval.mgz"
# loading in mgz (t-value map)
img = fsmgh.load(mgz_path)
# extracting dataobj
dataobj_array = np.asarray(img.dataobj)
# thresholding --- WHICH VALUE??? 2 or 3
new_dataobj_array = np.where(dataobj_array > 2, dataobj_array, 0)
# writing thresholded to new obj
new_img = fsmgh.MGHImage(new_dataobj_array, img.affine,
                         header=img.header, extra=img.extra)

nsd_flocfaces_path = "/Applications/freesurfer/7.3.2/subjects/subj01/label/rh.floc-faces.mgz"
nsd_flocfaces = fsmgh.load(nsd_flocfaces_path)
flocfaces_dataobj_array = np.asarray(nsd_flocfaces.dataobj)
flocfaces0_dataobj_array = np.where(flocfaces_dataobj_array == 1, 1, 0)

new_roi_array = new_dataobj_array * flocfaces0_dataobj_array

new_roi_img = fsmgh.MGHImage(new_roi_array, img.affine,
                             header=img.header, extra=img.extra)

# do for each ROI in nsd ROI file, add each to on array, add to one file (that will be your thresholded ROIs file)


def threshold_rois(tval_surf_path, nsd_roi_path, threshold):
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

    return thresholded_rois


out = threshold_rois(mgz_path, nsd_flocfaces_path, 2)

out.to_filename(
    "/Users/fyzeen/FyzeenLocal/GitHub/IPS-VTC-fWMT/data/subj01/freesurfer/t2flocfaces.mgz")

# new_roi_img.to_filename("/Users/fyzeen/FyzeenLocal/GitHub/IPS-VTC-fWMT/data/subj01/freesurfer/t3flocfaces.mgz")

# new_img.to_filename("/Users/fyzeen/FyzeenLocal/GitHub/IPS-VTC-fWMT/data/subj01/freesurfer/threshold0.mgz")

# img.to_filename("/Users/fyzeen/FyzeenLocal/GitHub/IPS-VTC-fWMT/data/subj01/freesurfer/out.mgz")
