import os, csv
import pandas as pd
import numpy as np
from scipy import signal

#  marker -2 ~ 10s 추출 / baseline 설정 / 조건별 평균 / data_pupil[i].get("confidence") > 0.8  (in next script)
# BlockData에 마커 정보 넣어주기 (자극 기간이 아닌 경우 -1로 기록 / timestamp도 lapse로 추가해서 누적 기록하기)
path = 'C:/Users/jinwook/Desktop/Vection Data Analysis/Analysis Code/Eye Analysis/Pupil Diameter/'

def getFileName(path_dir):
    file_list = os.listdir(path_dir)
    file_list.sort()
    dataList = []

    for f in file_list:
        if f.find('.csv') != -1:
            dataList.append(f)

    return dataList



def readCSV(partiPath):
    f = open(path + partiPath, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    isHeader = True
    header = []
    data = []

    for line in rdr:
        if isHeader:
            header = line
            isHeader = False
            continue
        data.append(line)
    f.close()

    return header, data


def readData():
    pList = getFileName(path)

    # Merge data
    fullData = []
    for p in pList:
        header, data = readCSV(p)
        fullData.extend(data)

    return header, fullData



def allignTrial(data): 
    totalTrials = []
    isTrial = False

    t = []
    for l in data:
        if int(l[10]) == -1 and isTrial:
            isTrial = False
            totalTrials.append(t)
            t = []

        elif int(l[10]) >= 0 and int(l[10]) < 1440:  #120Hz
            isTrial = True
            t.append(l)
    
    stim = [[],[],[],[],[],[]]  # 0, 1, 2 / 20, 80  =>  (0 20) (0 80) (1 20) (1 80) (2 20) (2 80)
    for t in totalTrials:
        sample = t[0]
        optic = [20, 80]
        idx = 2 * int(sample[8]) + optic.index(int(sample[9]))
        stim[idx].append(t)

    return stim



# 0~2s baseline 평균 내기
def calBaseline(trial, measure):
    size = []
    for t in trial:
        if int(t[10]) < 240:
            if measure == '3D':
                size.append(float(t[5]))  #3D
            else:
                size.append(float(t[3]))  #2D

    return sum(size) / len(size)


def calDiffPupilSize(baseline, trial, measure):
    diffTrial = []
    for t in trial:
        if measure == '3D':
            diffTrial.append(float(t[5])-baseline)  #3D
        else:
            diffTrial.append(float(t[3])-baseline)  #2D

    return diffTrial


def calcuateDiameter(stimuliSet, measure):
    stimDiffDiameter = [[],[],[],[],[],[]]
    index = -1

    for stim in stimuliSet:
        index += 1
        for t in stim:
            bsline = calBaseline(t, measure)
            filtered = btFilter(calDiffPupilSize(bsline, t, measure))
            stimDiffDiameter[index].append(filtered)

    return stimDiffDiameter


def btFilter(trial):
    N = 2
    Wn = 0.01

    B, A = signal.butter(N, Wn, output='ba')
    trial = signal.filtfilt(B, A, trial)

    return trial


def main():
    header, data = readData()
    stimuli = allignTrial(data)

    measureType = ['3D']
    for m in measureType:
        result = calcuateDiameter(stimuli, m)

        # Save Data
        result = np.array(result)
        np.save('./preprocessedDiameter_' + m, result)


if __name__ == "__main__":
    main()


