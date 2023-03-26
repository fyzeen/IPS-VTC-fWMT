% Subetting tracts to VOF using cleaned classification provided with NSD

% adding mrtrix functions to path
addpath("~/IPS-VTC-fWMT/code/utils/mrtrix/");

for i = ["01", "02", "03","04","05","06","07","08"]
    for j = ["run1", "run2"]
        freesurfer_subj_dir = "/home/naxos2-raid25/ahmad262/IPS-VTC-fWMT/data/freesurfer";
        diffusion_dir = freesurfer_subj_dir + "subj"+i+"/fyz/anatomy/diffusion/"+j+"/";
        
        if j == "run1"
            k = "run_1"
        elseif j == "run2"
            k = "run_2"
        end

        nsd_diffusion_dir = "/home/surly-raid1/kendrick-data/nsd/nsddata_diffusion/ppdata/subj"+i+"/"+k+"/"
        
        load(nsd_diffusion_dir + "tract-segmentation/classification-wholebrain-cleaned.mat");
        subset = (classification.index == 58 | classification.index == 59);
        
        % reading data
        tracks = read_mrtrix_tracks(nsd_diffusion_dir + "track/track-merged.tck");
        % selecting tracts labeled as left VOF (58) or right VOF (59)
        tracks.data = tracks.data(subset);

        % subsetting the tracts, writing to file
        write_mrtrix_tracks(tracks, diffusion_dir + "vof.tck")

        % reset tracks
        tracks = 0;
    end
end