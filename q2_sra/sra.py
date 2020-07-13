import pandas as pd


def segment(dataframe, path):
    """ Segments SRA manifest into multiple files.

    Each sub-file is grouped by the project id

    Parameters
    ----------
    dataframe : pd.DataFrame
        SRA manifest file.  Must contain ProjectID, Run and Sample columns.
    path : Path
        Path to save the per project manifest files
    """
    runs = dataframe.groupby('ProjectID')
    for project_id, group in runs:
        project_path = f'{path}/sra_manifest_{project_id}.txt'
        group.to_csv(project_path, sep='\t')


def fastq_import(samples, project_id, dirname, manifest, fastq):
    """ Imports fastq file, auto-detecting phred scores

    Parameters
    ----------
    samples : list of str
       Sample names
    project_id : str
       Project id
    dirname : path
       Path of the directory of temporary demuxed files
    manifest : path
       Path to manifest file
    """
    cmd = ("qiime tools import --type 'SampleData[SequencesWithQuality]' "
           f"--input-path {manifest} "
           f"--output-path {dirname}/{project_id}.demux.qza "
           "--input-format SingleEndFastqManifestPhred64V2")
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
    proc.wait()
    print(cmd)
    err = proc.stderr.read().decode('utf-8')
    if 'Decoded Phred score is out of range' in err:
        cmd = ("qiime tools import --type 'SampleData[SequencesWithQuality]' "
               f"--input-path {manifest} "
               f"--output-path {dirname}/{project_id}.demux.qza "
               "--input-format SingleEndFastqManifestPhred33V2")
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True)
        proc.wait()
        print(cmd)
        print(proc.stderr.read())
