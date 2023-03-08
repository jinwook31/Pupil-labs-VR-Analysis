import csv, os
from email import header
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



path = './Blink Data/'

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
        line.append(partiPath[20:23])
        data.append(line)
    f.close()
    header.append('PartNum')

    return header, data



def plotData(df):
    pivot = df.pivot_table(index = 'PartNum', columns=['Audio', 'Optic'], values=['cnt'], aggfunc=['mean'])
    #print(pivot)
    #pivot = pivot.reset_index()
    pivot.columns = ['20_0', '80_0', '20_1', '80_1', '20_2', '80_2']
    print(pivot)
    pivot.to_csv('blink spss.csv', encoding='utf-8', sep=',', na_rep='NaN')



def main():
    pList = getFileName(path)

    # Merge data
    fullData = []
    for p in pList:
        header, data = readCSV(p)
        fullData.extend(data)
    
    # Plot Data (Pivot)
    df = pd.DataFrame(fullData[1:], columns = header)
    df = df.astype({'Audio':'float', 'Optic':'float', 'cnt':'float'})
    print(df)

    plotData(df)



if __name__ == '__main__':
    main()

    
