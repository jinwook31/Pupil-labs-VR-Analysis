import os
import collections

import msgpack
import numpy as np


PLData = collections.namedtuple("PLData", ["data", "timestamps", "topics"])

# edit `path` s.t. it points to your recording
path = 'C:/Users/jinwook/Dropbox (Visual Cognition Lab)/문서/Visual Cognition Lab/Exp_JinWook/Experiment/Multisensory Vection/Experiment 2/Experiment Data/Eye Data/'

participantList = ['2022_10_17 14_40_20_P01','2022_10_17 19_09_08_P02','2022_10_20 14_28_23_P04','2022_10_20 19_30_40_P05','2022_10_21 14_39_07_P06','2022_10_22 18_23_55_P08','2022_10_24 19_38_40_P09','2022_11_28 16_40_24_P13','2022_11_28 19_18_23_P14','2022_11_29 16_10_55_P15','2022_11_30 16_21_15_P17','2022_11_30 19_44_17_P18','2022_12_01 13_36_04_P19','2022_12_01 16_25_51_P20','2022_12_01 19_13_59_P21','2022_12_03 13_10_57_P23','2022_12_04 13_27_11_P26','2022_12_04 16_57_53_P27','2022_12_04 20_43_21_P28','2022_12_05 12_02_30_P29']

blockList = ['000','001','002','003','004','005','006','007']

def serialized_dict_from_msgpack_bytes(data):
    return msgpack.unpackb(
        data, raw=False, use_list=False, ext_hook=msgpack_unpacking_ext_hook,
    )


def msgpack_unpacking_ext_hook(self, code, data):
    SERIALIZED_DICT_MSGPACK_EXT_CODE = 13
    if code == SERIALIZED_DICT_MSGPACK_EXT_CODE:
        return serialized_dict_from_msgpack_bytes(data)
    return msgpack.ExtType(code, data)


def load_pldata_file(directory, topic):
    ts_file = os.path.join(directory, topic + "_timestamps.npy")
    msgpack_file = os.path.join(directory, topic + ".pldata")
    try:
        data = []
        topics = []
        data_ts = np.load(ts_file)
        with open(msgpack_file, "rb") as fh:
            for topic, payload in msgpack.Unpacker(fh, raw=False, use_list=False):
                datum = serialized_dict_from_msgpack_bytes(payload)
                data.append(datum)
                topics.append(topic)
    except FileNotFoundError:
        print('File Not Found')
        data = []
        data_ts = []
        topics = []

    return PLData(data, data_ts, topics)


def getPupilList(partiNum, blockNum):
    # Read "gaze.pldata" and "gaze_timestamps.npy" data
    fullPath = path + partiNum + "/" + blockNum + "/"
    get_data = load_pldata_file(fullPath, "pupil")

    data_pupil = get_data.data
    data_ts = get_data.timestamps
    topics = get_data.topics

    return data_pupil, data_ts, topics



def getEventMarkers(partiNum, blockNum):
    # Read "gaze.pldata" and "gaze_timestamps.npy" data
    fullPath = path + partiNum + "/" + blockNum + "/"
    get_data = load_pldata_file(fullPath, "annotation")

    data_annot = get_data.data
    data_ts = get_data.timestamps
    topics = get_data.topics

    markerList = []
    trial = []
    for d in data_annot:
        if d['trialStatus'] == 'Start':
            trial.append(d['audio']) 
            trial.append(d['optic'])
            trial.append(d['trialNum'])
            trial.append(d['timestamp'])  # Start Time

        elif d['trialStatus'] == 'End':
            trial.append(d['timestamp'])  # End Time
            trial.append(0)  # pupil counter
            markerList.append(trial)
            trial = []

    return markerList



def saveResult2CSV(partNum, marker):
    print('Saving Result...')

    header = ['timestamp', 'id', 'confidence','diameter','method','diameter_3d', 'block', 'trial', 'audio', 'visual', 'sampleNum']
    import csv
    with open('./Pupil Diameter/' + partNum + '_pupil diameter.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(marker)
        


def main():
    for p in participantList:
        fullList = []
        trial = 0

        for b in blockList:
            blockData = []
            data_pupil, ts, topics = getPupilList(p, b)
            marker = getEventMarkers(p, b)

            # https://pyplr.github.io/cvd_pupillometry/04d_analysis.html
            for i in range(0, len(data_pupil)):
                if topics[i] == 'pupil.0.3d':   # pupil.0.2d / 0.3d / 1.2d / 1.3d (3D 데이터 사용)
                    data = [data_pupil[i].get("timestamp"), data_pupil[i].get("id"), data_pupil[i].get("confidence"), data_pupil[i].get("diameter"), data_pupil[i].get("method"), data_pupil[i].get("diameter_3d"), b, -1, -1, -1, -1]
                    blockData.append(data)


            # BlockData에 마커 정보 넣어주기 (자극 기간이 아닌 경우 -1로 기록 / timestamp도 lapse로 추가해서 누적 기록하기)
            for m in marker:    # [0] audio / [1] optic / m[3] = start /  m[4] = endtime   (1s = 1 / total 12s)
                sampleNum = 0
                if len(m) != 6:
                    continue

                for d in blockData:
                    if d[0] >= m[3] and d[0] <= m[4]:
                        d[7] = trial
                        d[8] = m[0]
                        d[9] = m[1]
                        d[10] = sampleNum
                        sampleNum += 1
                trial += 1

            print(trial)
            fullList.extend(blockData)

        saveResult2CSV(p, fullList)


if __name__ == "__main__":
    main()







