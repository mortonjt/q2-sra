import os
import pandas as pd


def single_seq_manifest(samples, fastq):
    cols = ['sample-id', 'absolute-filepath']
    seq = list(map(lambda x: f'{fastq}/{x}.fastq', runs))
    manifest = pd.DataFrame(
        {
            cols[0]: samples,
            cols[1]: seq
        }
    )
    if os.path.exists(seq[0]):
        return manifest, True
    else:
        return manifest, False


def paired_seq_manifest(samples, fastq):
    cols = ['sample-id', 'forward-absolute-filepath', 'reverse-absolute-filepath']
    fwd = list(map(lambda x: f'{fastq}/{x}_1.fastq', runs))
    rev = list(map(lambda x: f'{fastq}/{x}_2.fastq', runs))
    manifest = pd.DataFrame(
        {
            cols[0]: samples,
            cols[1]: fwd,
            cols[2]: rev
        }
    )
    if os.path.exists(fwd[0]):
        return manifest, True
    else:
        return manifest, False
