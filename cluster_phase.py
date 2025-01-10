import os
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from scipy.spatial.distance import pdist
from scipy.signal import hilbert
import tkinter as tk
from tkinter import simpledialog

def cluster_phase(dataraw, selections):
    dirsave = selections["Gamedir"]
    os.makedirs(os.path.join(dirsave, "Results"), exist_ok=True)
    
    playfull = (selections["PlayersList"]["Defender"] +
                selections["PlayersList"]["Midfielder"] +
                selections["PlayersList"]["Forwards"])
    
    players = []
    for p in playfull:
        po = p.rfind('.')
        player_name = p[:po].replace('_', '-')
        players.append(player_name)
    
    # Separating data
    xdatat1 = dataraw["X"]
    ydatat1 = dataraw["Y"]
    xdatat2 = dataraw["OpX"]
    ydatat2 = dataraw["OpY"]
    
    # Metric calculations
    # Effective Area
    SufAreat1 = []
    SufAreat2 = []
    for i in range(len(xdatat1)):
        K1 = ConvexHull(np.column_stack((xdatat1[i], ydatat1[i]))).vertices
        K2 = ConvexHull(np.column_stack((xdatat2[i], ydatat2[i]))).vertices
        SufAreat1.append(ConvexHull(np.column_stack((xdatat1[i][K1], ydatat1[i][K1]))).volume)
        SufAreat2.append(ConvexHull(np.column_stack((xdatat2[i][K2], ydatat2[i][K2]))).volume)
    
    # Width, Length, and LpW Ratio
    DistAt1, DistPt1, LpWRatiot1 = [], [], []
    DistAt2, DistPt2, LpWRatiot2 = [], [], []
    
    for i in range(len(xdatat1)):
        # Team 1
        Aminpt1 = np.argmin(ydatat1[i])
        Amaxpt1 = np.argmax(ydatat1[i])
        DistAt1.append(pdist([[xdatat1[i][Aminpt1], ydatat1[i][Aminpt1]],
                              [xdatat1[i][Amaxpt1], ydatat1[i][Amaxpt1]]], 'euclidean')[0])
        
        Pminpt1 = np.argmin(xdatat1[i])
        Pmaxpt1 = np.argmax(xdatat1[i])
        DistPt1.append(pdist([[xdatat1[i][Pminpt1], ydatat1[i][Pminpt1]],
                              [xdatat1[i][Pmaxpt1], ydatat1[i][Pmaxpt1]]], 'euclidean')[0])
        LpWRatiot1.append(DistPt1[-1] / DistAt1[-1])
        
        # Team 2
        Aminpt2 = np.argmin(ydatat2[i])
        Amaxpt2 = np.argmax(ydatat2[i])
        DistAt2.append(pdist([[xdatat2[i][Aminpt2], ydatat2[i][Aminpt2]],
                              [xdatat2[i][Amaxpt2], ydatat2[i][Amaxpt2]]], 'euclidean')[0])
        
        Pminpt2 = np.argmin(xdatat2[i])
        Pmaxpt2 = np.argmax(xdatat2[i])
        DistPt2.append(pdist([[xdatat2[i][Pminpt2], ydatat2[i][Pminpt2]],
                              [xdatat2[i][Pmaxpt2], ydatat2[i][Pmaxpt2]]], 'euclidean')[0])
        LpWRatiot2.append(DistPt2[-1] / DistAt2[-1])
    
    # Select variables
    listvar = ['Effective Area', 'Width', 'Length', 'LpWRatio']
    root = tk.Tk()
    root.withdraw()
    indx = simpledialog.askinteger("Select variable", "Enter the index (1-4):")
    root.destroy()
    
    if indx == 1:
        vt1 = SufAreat1
        vt2 = SufAreat2
    elif indx == 2:
        vt1 = DistAt1
        vt2 = DistAt2
    elif indx == 3:
        vt1 = DistPt1
        vt2 = DistPt2
    elif indx == 4:
        vt1 = LpWRatiot1
        vt2 = LpWRatiot2
    
    ts_data = np.column_stack((vt1, vt2))
    TSnumber = ts_data.shape[1]
    TSlength = ts_data.shape[0]
    
    # Compute phase for each time series using Hilbert transform
    TSphase = np.unwrap(np.angle(hilbert(ts_data, axis=0)), axis=0)
    
    # Compute mean running cluster phase
    clusterphase = np.unwrap(np.angle(np.mean(np.exp(1j * TSphase), axis=1)))
    
    # Compute relative phases and amplitudes
    TSrhoGRP = np.abs(np.mean(np.exp(1j * (TSphase - clusterphase[:, None])), axis=1))
    GRPrhoM = np.mean(TSrhoGRP)
    
    # Save results
    fname = os.path.join(dirsave, "Results", f"NonLinear_Collective_Res_{selections['ColNonLinTyp']}.csv")
    results = pd.DataFrame({"Time (s)": np.arange(len(TSrhoGRP)), "Cluster Phase Analysis": TSrhoGRP})
    results.to_csv(fname, index=False)
    
    print(f"Results saved to {fname}")
