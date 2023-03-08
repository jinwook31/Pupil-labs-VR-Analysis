from pyplr import utils

# Pupil Labs recording directory
path = 'C:/Users/jinwook/Dropbox (Visual Cognition Lab)/문서/Visual Cognition Lab/Exp_JinWook/Experiment/Multisensory Vection/Experiment 2/Experiment Data/Eye Data/'
participantList = ['2022_10_17 14_40_20_P01']
blockList = ['000','001','002','003','004','005','006','007']

#utils.print_file_structure(path + '/' + participantList[0])


# Columns to load
use_cols = ['confidence',
            'method',
            'pupil_timestamp',
            'eye_id',
            'diameter_3d',
            'diameter']


# Get a handle on a subject
s = utils.new_subject(path + '/' + participantList[0], export='000', out_dir_nm='pyplr_analysis')

# Load pupil data
samples = utils.load_pupil(s['data_dir'], eye_id='best', cols=use_cols)

print(samples)

