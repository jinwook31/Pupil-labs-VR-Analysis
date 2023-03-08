import csv, os, math
from scipy.stats import sem
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
        data.append(line)
    f.close()

    return header, data



def plotData(df):
    pivot = df.pivot_table(index = 'Optic', columns='Audio', values=['cnt'], aggfunc=['mean'])
    print(pivot)

    ciErr = [[1.96 *4.988959 / math.sqrt(20), 1.96 * 4.085081 / math.sqrt(20)], # No aud
    [1.96 *4.057086 / math.sqrt(20), 1.96 *4.463201 / math.sqrt(20)],  # Aud
    [1.96 * 4.941893 / math.sqrt(20), 1.96 *4.7989078 / math.sqrt(20)]]  # Aud No Cho

    fig, ax = plt.subplots()
    pivot.plot(kind='bar', ax=ax, zorder=3, color=['darkgray','royalblue','skyblue'], yerr=ciErr)

    plt.xticks(rotation=0)
    plt.yticks(np.arange(0, 8.5, 0.5))
    plt.legend(('No Audio','Audio Coherence','Audio Non-Coherence'))   # 0 1 2

    ax.set_xticklabels(['20%','80%'])
    ax.set_xlabel('Optic Coherence')
    ax.set_ylabel('Blink Average during Trial (10s)')

    #plt.show()
    plt.savefig('blink.png')
    plt.clf()



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

    

