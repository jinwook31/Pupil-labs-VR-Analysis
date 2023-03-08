import os, csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def averageTrials(trials):
    df = pd.DataFrame(trials)
    return df.mean().tolist()


def main():
    measureType = ['3D']
    for m in measureType:
        data = np.load('./preprocessedDiameter_'+ m +'.npy', allow_pickle=True)
        stimuli = data.tolist()      # 0,1,2 / 20,80  =>  (0 20) (0 80) (1 20) (1 80) (2 20) (2 80)

        title = ['20%, No Audio', '80%, No Audio', '20%, Audio Coherence', '80%, Audio Coherence', '20%, Audio Non-Coherence', '80%, Audio Non-Coherence']
        idx = 0

        averaged = []
        err = []
        for s in stimuli:
            avg = averageTrials(s)

            # Resample (120Hz -> time으로 변환)
            t = []
            for i in range(1440):
                t.append(i / 120)

            plt.plot(t, avg)

            plt.yticks(np.arange(-0.08, 0.11, 0.02))
            plt.title(title[idx])
            plt.axvline(2.0, 0, 1, color='lightgray', linestyle='--', linewidth=1)
            plt.axhline(0.0, 0, 1, color='lightgray', linestyle='--', linewidth=1)
            plt.xlabel("Time (s)")
            plt.ylabel("Pupil Diameter Difference from Baseline")
            
            plt.savefig(title[idx] + '_' + m + '.png')
            plt.clf()

            idx += 1



if __name__ == "__main__":
    main()

