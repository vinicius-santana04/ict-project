import os
import numpy as np
import pandas as pd


def sectors_coordenation(dataraw, selections):
    dirsave = selections["Gamedir"]
    os.makedirs(os.path.join(dirsave, "Results"), exist_ok=True)

    playfull = selections["PlayersList"]["Defender"] + \
               selections["PlayersList"]["Midfielder"] + \
               selections["PlayersList"]["Forwards"]
    players = [p.split('.')[-2].replace('_', '-') for p in playfull]

    # Separating data
    xdata = dataraw["X"]
    ydata = dataraw["Y"]

    # Time Vector
    freq_ac = float(selections["FreqAc"])
    vtime = np.arange(len(xdata)) / freq_ac / 60

    # Mean of positions
    PlayersMeanX = np.mean(xdata, axis=0)
    PlayersMeanY = np.mean(ydata, axis=0)

    # Team Mean
    teamMeanX = np.mean(PlayersMeanX)
    teamMeanY = np.mean(PlayersMeanY)

    # Median of positions
    PlayersMedianX = np.median(xdata, axis=0)
    PlayersMedianY = np.median(ydata, axis=0)

    teamMedianX = np.median(PlayersMedianX)
    teamMedianY = np.median(PlayersMedianY)

    # Team mean vector
    TMeanX = np.mean(xdata, axis=1)
    TMeanY = np.mean(ydata, axis=1)
    TMean = np.column_stack((TMeanX, TMeanY))

    # Separating sectors
    sD = len(selections["PlayersList"]["Defender"])
    xdataD = xdata[:, :sD]
    ydataD = ydata[:, :sD]
    xmeanD = np.mean(xdataD, axis=1)
    ymeanD = np.mean(ydataD, axis=1)

    sM = len(selections["PlayersList"]["Midfielder"])
    xdataM = xdata[:, sD:sD + sM]
    ydataM = ydata[:, sD:sD + sM]
    xmeanM = np.mean(xdataM, axis=1)
    ymeanM = np.mean(ydataM, axis=1)

    sF = len(selections["PlayersList"]["Forwards"])
    xdataF = xdata[:, sD + sM:sD + sM + sF]
    ydataF = ydata[:, sD + sM:sD + sM + sF]
    xmeanF = np.mean(xdataF, axis=1)
    ymeanF = np.mean(ydataF, axis=1)

    # Calculating Vector Coding
    def calculate_vc(series1, series2):
        diff1 = np.diff(series1)
        diff2 = np.diff(series2)
        hypotenuse = np.sqrt(diff1**2 + diff2**2)
        sine = diff2 / hypotenuse
        cosine = diff1 / hypotenuse
        VC = np.degrees(np.arctan2(sine, cosine))
        VC[VC < 0] += 360
        return VC

    res1 = np.zeros((len(xmeanD) - 1, 3))
    res1[:, 0] = calculate_vc(xmeanD, xmeanM)
    res1[:, 1] = calculate_vc(xmeanD, xmeanF)
    res1[:, 2] = calculate_vc(xmeanM, xmeanF)

    # Create categorical variables
    def create_ctgvar(coupangle):
        CtgVar_vc_DG = np.zeros_like(coupangle, dtype=int)
        ranges = [
            (0, 22.5), (22.5, 67.5), (67.5, 112.5), (112.5, 157.5),
            (157.5, 202.5), (202.5, 247.5), (247.5, 292.5), (292.5, 337.5), (337.5, 360)
        ]
        categories = [1, 2, 3, 4, 1, 2, 3, 4, 1]
        for (start, end), category in zip(ranges, categories):
            CtgVar_vc_DG[(coupangle >= start) & (coupangle < end)] = category

        group_phase = [np.round(np.sum(CtgVar_vc_DG == i) / len(CtgVar_vc_DG) * 100, 3) for i in range(1, 5)]
        return group_phase

    res1vc = np.array([create_ctgvar(res1[:, i]) for i in range(res1.shape[1])]).T

    # Saving results
    titfil = f"NonLinear_Collective_Res_{selections['ColNonLinTyp']}.xlsx"
    fname = os.path.join(dirsave, "Results", titfil)

    with pd.ExcelWriter(fname, engine='openpyxl') as writer:
        pd.DataFrame({"Vector Coding": []}).to_excel(writer, index=False, sheet_name='Summary')
        pd.DataFrame({"Time(s)": vtime, "DxM": res1[:, 0], "MxF": res1[:, 1], "DxF": res1[:, 2]}).to_excel(writer, index=False, sheet_name='Details')
        writer.sheets['Details'].cell(row=2, column=5, value="DxM")
        writer.sheets['Details'].cell(row=2, column=7, value="MxF")
        writer.sheets['Details'].cell(row=2, column=9, value="DxF")
    
    print(f"Results saved to {fname}")
