% Subetting tracts to VOF using cleaned classification provided with NSD

% adding mrtrix functions to path
addpath("./utils/mrtrix/");

for i = ["01", "02", "03","04","05","06","07","08","09","10"]
    for j = ["run1", "run2"]
        freesurfer_subj_dir = "/Applications/freesurfer/7.3.2/subjects/";
        diffusion_dir = freesurfer_subj_dir + "subj"+i+"/fyz/anatomy/diffusion/"+j+"/";
        
        load(diffusion_dir + "classification-wholebrain-cleaned.mat");
        subset = (classification.index == 58 | classification.index == 59);
        
        % reading data
        tracks = read_mrtrix_tracks(diffusion_dir + "track-merged.tck");
        % selecting tracts labeled as left VOF (58) or right VOF (59)
        tracks.data = tracks.data(subset);

        % subsetting the tracts, writing to file
        write_mrtrix_tracks(tracks, diffusion_dir + "vof.tck")

        % reset tracks
        tracks = 0;
    end
end