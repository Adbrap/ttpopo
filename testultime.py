# ----- initialisation des modules -----#
import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from multiprocessing import Process
import multiprocessing
import math
# from playsound import playsound
from ib_insync import *
import sys
import subprocess
import tempfile
from ftplib import FTP

print('')
Write.Print('Backtester Live 1.0', Colors.green, interval=0.000)
print('')
print('-------------------------')
print('')

Write.Print('Voir les figures ? (o/n)', Colors.white, interval=0.000)
print('')
a = 0
while a != 1:
    Write.Print('>> ', Colors.white, interval=0.000)
    voir = input()
    print('')
    if voir == 'o' or voir == 'n' or voir == 'O' or voir == 'N':
        a = 1
    else:
        print('')
        Write.Print('Choix Non Reconnu!', Colors.red, interval=0.000)
        print('')



nombre_point = 0
nombre_magique = 0
mise  = 1000
minargent = 5
laquelle = []
plusbas = []
plusbas1 = 0
changement = []

def get_angle(point1, point2):
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]

    # Pour une ligne verticale, on retourne 90 directement
    if x_diff == 0:
        return 90

    angle = math.atan2(y_diff, x_diff)
    angle = math.degrees(angle)
    return angle


def plot_points(point1, point2):
    angle = get_angle(point1, point2)

    # Si l'angle est 90 (ligne verticale), la pente est "infinie"
    if angle == 90:
        slope_percent = "90"
        return slope_percent
    else:
        slope_percent = math.tan(math.radians(angle)) * 100
        return slope_percent
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

pourcent_gain = 0
if voir == 'o' or voir == 'O':
    activ = True
else:
    activ = False
nombre_regarder = 0
nombre_gagnant = 0
nombre_perdant = 0
debug = []
condition = 0
placebas = 0
pourcentbastete = []
nomperdant = []


file_obj = open("titre_df_verif22.txt", "r")
file_data = file_obj.read()
lines = file_data.splitlines()
file_obj.close()
ticktick=[]
for argument in lines:
    ticktick.append(argument)


#ticktick= ['AAPL', 'TSLA', 'A', 'AA', 'AAA', 'AAAU', 'AAC', 'AACG', 'AACI', 'AACIU', 'AADI', 'AADR', 'AAIC', 'AAIC', 'AAIC', 'AAIN', 'AAL', 'AAMC', 'AAME', 'AAN', 'AAOI', 'AAON', 'AAP', 'AAPL', 'AAT', 'AAU', 'ABB', 'ABBV', 'ABC', 'ABCB', 'ABCL', 'ABCM', 'ABEO', 'ABEQ', 'ABEV', 'ABG', 'ABIO', 'ABM', 'ABNB', 'ABOS', 'ABR', 'ABSI', 'ABST', 'ABT', 'ABUS', 'ABVC', 'AC', 'ACA', 'ACAB', 'ACACU', 'ACAD', 'ACAH', 'ACAHU', 'ACAQ', 'ACAX', 'ACAXR', 'ACAXU', 'ACB', 'ACBA', 'ACBAU', 'ACCD', 'ACCO', 'ACEL', 'ACER', 'ACES', 'ACET', 'ACGL', 'ACGLN', 'ACGLO', 'ACHC', 'ACHL', 'ACHR', 'ACHV', 'ACI', 'ACIO', 'ACIU', 'ACIW', 'ACLS', 'ACLX', 'ACM', 'ACMR', 'ACN', 'ACNB', 'ACON', 'ACOR', 'ACP', 'ACQR', 'ACQRU', 'ACR', 'ACRE', 'ACRO', 'ACRS', 'ACRX', 'ACSI', 'ACST', 'ACT', 'ACTG', 'ACTV', 'ACU', 'ACV', 'ACVA', 'ACVF', 'ACWI', 'ACWV', 'ACWX', 'ACXP', 'ADAG', 'ADAL', 'ADALU', 'ADAP', 'ADBE', 'ADC', 'ADCT', 'ADER', 'ADERU', 'ADES', 'ADEX', 'ADFI', 'ADI', 'ADIL', 'ADIV', 'ADM', 'ADMA', 'ADME', 'ADMP', 'ADN', 'ADNT', 'ADOC', 'ADOCR', 'ADP', 'ADPT', 'ADRE', 'ADRT', 'ADSE', 'ADSK', 'ADT', 'ADTH', 'ADTN', 'ADTX', 'ADUS', 'ADV', 'ADVM', 'ADX', 'ADXN', 'AE', 'AEAE', 'AEAEU', 'AEE', 'AEF', 'AEFC', 'AEG', 'AEHL', 'AEHR', 'AEI', 'AEIS', 'AEL', 'AEM', 'AEMB', 'AEMD', 'AENZ', 'AEO', 'AEP', 'AEPPZ', 'AER', 'AES', 'AESC', 'AESR', 'AEVA', 'AEY', 'AEYE', 'AEZS', 'AFAR', 'AFARU', 'AFB', 'AFBI', 'AFCG', 'AFG', 'AFGB', 'AFGC', 'AFGD', 'AFGE', 'AFIB', 'AFIF', 'AFK', 'AFL', 'AFLG', 'AFMC', 'AFMD', 'AFRI', 'AFRM', 'AFSM', 'AFT', 'AFTR', 'AFTR', 'AFTY', 'AFYA', 'AG', 'AGAC', 'AGAC', 'AGBA', 'AGCO', 'AGD', 'AGE', 'AGEN', 'AGFS', 'AGFY', 'AGG', 'AGGH', 'AGGR', 'AGGRU', 'AGGY', 'AGI', 'AGIH', 'AGIL', 'AGIO', 'AGL', 'AGLE', 'AGM', 'AGMH', 'AGNC', 'AGNCM', 'AGNCN', 'AGNCO', 'AGNCP', 'AGNG', 'AGO', 'AGOV', 'AGOX', 'AGQ', 'AGR', 'AGRH', 'AGRI', 'AGRO', 'AGRX', 'AGS', 'AGTI', 'AGX', 'AGYS', 'AGZ', 'AGZD', 'AHCO', 'AHG', 'AHH', 'AHHX', 'AHI', 'AHOY', 'AHRN', 'AHRNU', 'AHT', 'AHYB', 'AI', 'AIA', 'AIB', 'AIBBR', 'AIBBU', 'AIC', 'AIEQ', 'AIF', 'AIG', 'AIH', 'AIHS', 'AILG', 'AILV', 'AIM', 'AIMBU', 'AIMC', 'AIMD', 'AIN', 'AINC', 'AIO', 'AIP', 'AIQ', 'AIR', 'AIRC', 'AIRG', 'AIRI', 'AIRR', 'AIRS', 'AIRT', 'AIRTP', 'AIT', 'AIU', 'AIV', 'AIVI', 'AIVL', 'AIZ', 'AIZN', 'AJG', 'AJRD', 'AJX', 'AJXA', 'AKA', 'AKAM', 'AKAN', 'AKBA', 'AKR', 'AKRO', 'AKTS', 'AKTX', 'AKU', 'AKYA', 'AL', 'ALB', 'ALC', 'ALCC', 'ALCO', 'ALDX', 'ALE', 'ALEC', 'ALEX', 'ALG', 'ALGM', 'ALGN', 'ALGS', 'ALGT']
#ticktick= ['ABVC', 'ACCD', 'ADERU', 'ADOCR', 'AIRG', 'AMRX']
for nomtick in ticktick:
    try:
        nombre_regarder = nombre_regarder +1
        Write.Print(f'Figure {nomtick}', Colors.pink, interval=0.000)
        print('')
        #dossier = "baki/"
        #nom_fichier = f"{t}.json"
        #chemin_fichier = dossier + nom_fichier
        #with open(chemin_fichier, 'r') as fichiers:
        #    data = json.load(fichiers)

        api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{nomtick}/range/1/hour/2023-07-03/2023-08-28?adjusted=true&limit=50000&apiKey=1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
        data = requests.get(api_url_OHLC).json()
        df = pd.DataFrame(data['results'])

        #df = pd.DataFrame(data)
        #df = df.reset_index(drop=True)
        #df = pd.DataFrame(data['results'])

        #with open(chemin_fichier, 'w') as fichier:
        #json.dump(data, fichier)
        local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
        highs = df.iloc[local_max, :]
        lows = df.iloc[local_min, :]

        trouver2 = False
        trouver3 = False
        trouver4 = False

        for i in range(1, len(df)):
            if df['h'].values[i] >= df['c'].values[0]+((df['c'].values[0]*0.8964)/100) and trouver3 == False and trouver2 == False:
                placevert = i
                debug.append(+0.8964)
                pourcent_gain = pourcent_gain + 0.8964
                nombre_gagnant = nombre_gagnant + 1
                nombre_point = nombre_point + (df['c'].index[placevert] - df['c'].index[0])
                trouver2 = True

            if df['c'].values[i] <= df['c'].values[0] - ((df['c'].values[0] * 18.675) / 100) and trouver2 == False and trouver3 == False:

                placerouge = i
                debug.append(((((df['c'].values[i]*100)/ df['c'].values[0]))-100))
                pourcent_gain = pourcent_gain + ((((df['c'].values[i]*100)/ df['c'].values[0]))-100)
                nombre_perdant = nombre_perdant +1
                nombre_point = nombre_point + (df['c'].index[placerouge] - df['c'].index[0])
                trouver3 = True
                nomperdant.append(nomtick)




        # ----- creation des locals(min/max) -----#
        fig1 = plt.figure(figsize=(10, 7))
        plt.plot([], [], " ")
        fig1.patch.set_facecolor('#17DE17')
        fig1.patch.set_alpha(0.3)
        plt.title(f'IETE : {nomtick}', fontweight="bold", color='black')


        df['c'].plot(color=['blue'], label='Clotures')
        df['h'].plot(color=['green'], alpha = 0.3, linestyle='-', label='Plus Haut')
        df['l'].plot(color=['red'], alpha = 0.3, linestyle='-', label='Plus Bas')

        plt.axhline(y=df['c'].values[0]+((df['c'].values[0]*0.8964)/100), linestyle='--', alpha=0.3, color='green', label='12% objectif')
        plt.axhline(y=df['c'].values[0] - ((df['c'].values[0] * 18.675) / 100), linestyle='--', alpha=0.3, color='red', label='-250% objectif')


        #plt.scatter(x=highs.index, y=highs['c'], alpha=0.5)
        #plt.scatter(x=lows.index, y=lows['c'], alpha=0.5)


        plt.scatter(df['c'].index[0],df['c'].values[0], color='orange', label='BUY')

        if trouver2 == True:
            plt.scatter(df['h'].index[placevert], df['h'].values[placevert], color='green', label='SELL')

        if trouver3 == True:
            plt.scatter(df['c'].index[placerouge], df['c'].values[placerouge], color='red', label='SELL')

        plt.legend()
        if activ == True:
            plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
            plt.show()
    except:
        print('')
        Write.Print(f'Probleme {nomtick}', Colors.red, interval=0.000)
        print('')
#


print('')
print('')
Write.Print(f'Le Gain Cumulé est  : {round(pourcent_gain, 2)}', Colors.purple, interval=0.000)
print('')
Write.Print(f'{round(nombre_regarder, 2)} : Figure(s) Testée(s)', Colors.purple, interval=0.000)
print('')
print('-------------------')
print('')
Write.Print(f'{round(nombre_gagnant, 2)} Figure(s) Gagnante(s)', Colors.green, interval=0.000)
print('')
Write.Print(f'{round(nombre_perdant, 2)} Figure(s) Perdante(s)', Colors.red, interval=0.000)
print('')
Write.Print(f'{debug}', Colors.white, interval=0.000)
print('')
Write.Print(f'{min(debug)}', Colors.white, interval=0.000)
print('')
print('')
Write.Print(f'{nomperdant}', Colors.white, interval=0.000)
print('')
pourc_gagn = (nombre_gagnant*100)/(nombre_gagnant+nombre_perdant)
pourc_gagn = round(pourc_gagn,2)
Write.Print(f'{pourc_gagn} Pourcentage gagnant', Colors.white, interval=0.000)
print('')
Write.Print(f'Nombre de Figure(s) en Cour(s) : {round(nombre_regarder - (nombre_gagnant+nombre_perdant),2)}', Colors.white, interval=0.000)
print('')
Write.Print(f'Nombre de Point(s) Moyen(s) : {round(nombre_point / (nombre_gagnant+nombre_perdant),2)}', Colors.white, interval=0.000)
print('')