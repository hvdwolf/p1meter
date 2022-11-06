#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# mpgraphs.py - This python helper script contains the mathplotlib grap functions

# Copyright (c) 2022, Harry van der Wolf. all rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.


import pandas, matplotlib.pyplot as plt, matplotlib.dates as md, numpy as np
import time
from datetime import datetime
import locale

# Sizes for our canvas and mathplots. These values need to be the same in mpgraphs.py and ui_layout.py
gr_width = 450*3
gr_height = 808

# Dir to save our "figs" to
savedir = "/var/www/html/tmp/"

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


# Alter the font in the web. Somehow default font is bigger there
def alter_fonts():
    plt.rc('font', size=9) #controls default text size
    plt.rc('axes', titlesize=8) #fontsize of the title
    plt.rc('axes', labelsize=8) #fontsize of the x and y labels
    plt.rc('xtick', labelsize=8) #fontsize of the x tick labels
    plt.rc('ytick', labelsize=8) #fontsize of the y tick labels
    plt.rc('legend', fontsize=8) #fontsize of the legend

# 3 functions to add value labels
# This will add the value of import, export and m3 to the top of the bar
def add3labels(bar1,bar2, bar3):

    for rect in bar1 + bar2 + bar3:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.1f}', ha='center', va='bottom')

# This will add the value of import and exportto the top of the bar
def add2labels(bar1,bar2):

    for rect in bar1 + bar2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.1f}', ha='center', va='bottom')

# This will add the value of the chosen option to the top of the bar
def addlabel(bar1):

    for rect in bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.1f}', ha='center', va='bottom')

def plot_chart(all_values, X_axis, data, disp_optie):
        if (all_values['t_alles']):
            imp = plt.bar(X_axis - 0.2, data.importkwh, color = 'm', width = 0.2, label = 'kWh verbruikt')
            exp = plt.bar(X_axis, data.exportkwh, color = 'g', width = 0.2, label = 'kWh (zon)geleverd')
            m3 = plt.bar(X_axis + 0.2, data.gastotaalm3, color = 'r', width = 0.2, label = 'm3 gas verbruikt')
            add3labels(imp, exp, m3)
            plt.ylabel('kWh / m3')
            plt.title("energie verbruik/geleverd de afgelopen " + disp_optie)
        elif (all_values['t_electrisch']):
            imp = plt.bar(X_axis - 0.1, data.importkwh, color = 'm', width = 0.2, label = 'kWh verbruikt')
            exp = plt.bar(X_axis + 0.1, data.exportkwh, color = 'g', width = 0.2, label = 'kWh (zon)geleverd')
            add2labels(imp, exp)
            plt.ylabel('kWh')
            plt.title("energie verbruik/geleverd de afgelopen " + disp_optie)
        elif (all_values['t_verbruikt']):  # verbruikte hoeveelheid kWh
            imp = plt.bar(X_axis, data.importkwh, color='m', width=0.2, label='kWh verbruikt')
            addlabel(imp)
            plt.ylabel('kWh')
            plt.title("energieverbruik de afgelopen " + disp_optie)
        elif (all_values['t_geproduceerd']): # Geproduceerde hoeveelheid kWh
            exp = plt.bar(X_axis, data.exportkwh, color='g', width=0.2, label='kWh geproduceerd')
            addlabel(exp)
            plt.ylabel('kWh')
            plt.title("energie geleverd de afgelopen " + disp_optie)
        elif (all_values['t_gasverbruik']):  # Geproduceerde hoeveelheid kWh
            m3 = plt.bar(X_axis, data.importkwh, color='r', width=0.2, label='m3 verbruikt')
            addlabel(m3)
            plt.ylabel('m3')
            plt.title("gasverbruik de afgelopen " + disp_optie)

        #plt.savefig('pipo.png')

# ------------------------------- Graphs for values
def netto_per_dag(window, data, all_values, type, WEB=False):
    #Get current plot/figure and clear it
    fig = plt.gcf()
    plt.clf()
    if WEB:
        # For web change default font size from 10 to 8
        plt.rc('font', size=8)
        #alter_fonts()
    plt.xlabel('metingen per 24 uur')
    # Remove below locale value or replace with your own locale
    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')
    if (type == "el"):
        #print(str(round(((data.verbruiknuw).to_numpy().sum())/1000,1)))
        estart = data.exportkwh[0]
        eeind = data.exportkwh[len(data.exportkwh)-1]
        expE = round(eeind-estart, 1)
        #print("geproduceerd: ", str( round(eeind-estart, 1) ))
        istart = data.importkwh[0]
        ieind = data.importkwh[len(data.importkwh)-1]
        impE = round(ieind-istart,1)
        #print("verbruikt: ", str(round(ieind-istart,1)) )
        #print("netto: ", str( round(impE-expE,1)) )
        stroom = "(verbruikt: " + str(round(ieind-istart,1)) + " kWh, geproduceerd: " + str(round(eeind-estart, 1))
        if ((impE-expE) <= 0):
            prod = abs(round(impE-expE,1))
            stroomnetto = " kWh, netto geproduceerd: " + str(prod) + " kWh)"
        else:
            stroomnetto = " kWh, verbruikt: " + str(round(impE-expE,1)) + " kWh)"
        plt.ylabel('Watts')
        plt.title("positief (paars): verbruikt; negatief (groen): door zonnepanelen geleverd")
        if (len(all_values['-CAL-']) == 0):
            plt.suptitle("energie vandaag " + stroom + stroomnetto)
        else:
            plt.suptitle("energie verbruik op " + datetime.strptime(all_values['-CAL-'], '%Y-%m-%d').strftime('%a %d-%m-%Y') + " " + stroom + stroomnetto)
    else:
        plt.ylabel('m3')
        plt.title("Gasverbruik")
        if (len(all_values['-GCAL-']) == 0):
            plt.suptitle("gasverbruik vandaag: " + str(round((data.totaalm3).to_numpy().sum(),1)) + " m3")
        else:
            plt.suptitle("gasverbruik op " + datetime.strptime(all_values['-GCAL-'], '%Y-%m-%d').strftime('%a %d-%m-%Y') + ": " + str(round((data.totaalm3).to_numpy().sum(),1)) + " m3")

    plt.grid(axis='y', linestyle='--')

    if (type == "el"):
        # Prepare for the magenta (positive) and green (negative) values in the graph
        x = np.arange(len(data.tmstmp))
        # plot the magenta (positive) and green (negative) values in the graph
        plt.bar(x[data.verbruiknuw >0], data.verbruiknuw[data.verbruiknuw >0], color='m')
        plt.bar(x[data.verbruiknuw <0], data.verbruiknuw[data.verbruiknuw <0], color='g')
    else:
        if (all_values['_staaf_']):
            plt.bar(data.tmstmp, data.totaalm3, color='red')
        else:
            totaalm3 = data.totaalm3.to_numpy()
            plt.plot(data.tmstmp, data.totaalm3, color='red')

    # Define the location of your ticks relative to the total x-axis length
    time_stamps = np.linspace(0, 240, 13)
    # Define the labels
    time_labels = ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00", "24:00"]
    plt.xlim(0, 240)  # Defines the limit of your x-axis
    plt.xticks(time_stamps, labels=time_labels, rotation=30)  # Adapts the x-axis scale and labels

    # WEB is used in the webscripts and on the pc always False
    if WEB:
        ts = str(time.time()).split(".")
        plt.savefig(savedir + (ts[0]) + '.png', dpi=120)
        PNG = (ts[0]) + '.png'
        return PNG
    else:
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # -------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(gr_width / float(DPI), gr_height / float(DPI))
        #plt.show()
        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
        PNG = ''
        return PNG

def gescheiden_per_dag(window, data, all_values):
    #Get current plot/figure and clear it
    fig = plt.gcf()
    plt.clf()
    plt.xlabel('metingen')
    plt.ylabel('Watts')
    #X_axis = np.arange(len(data.tmstmp)/10)
    plt.xticks(np.arange(len(data.tmstmp)), data.tmstmp, rotation=70)

    if (len(all_values['-CAL-']) == 0):
        plt.suptitle("energie vandaag")
    else:
        plt.suptitle("energie verbruik op " + datetime.strptime(all_values['-CAL-'], '%Y-%m-%d').strftime('%a %d-%m-%Y'))

    plt.title("positief: verbruikt; negatief: door zonnepanelen geleverd")
    plt.grid(axis='y', linestyle='--')


    if (all_values['_staaf_']):
        plt.bar(data.tmstmp, data.importwh,  color = 'm', label = "Watt verbruikt")
        plt.bar(data.tmstmp, data.exportwh,  color = 'g', label = "Watt geleverd")
    else:
        plt.plot(data.tmstmp, data.importwh,  color = 'm', label = "verbruikt Watt")
        plt.plot(data.tmstmp, data.exportwh,  color = 'g', label = "geleverd Watt")

    DPI = fig.get_dpi()
    # -------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
    fig.set_size_inches(gr_width / float(DPI), gr_height / float(DPI))
    #plt.show()
    # ------------------------------- Instead of plt.show()
    draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

def verbruik_per_dag(window, data, all_values, WEB=False):
    #print(all_values)
    #Get current plot/figure and clear it
    fig = plt.gcf()
    plt.clf()
    if WEB:
        # For web change default font size from 10 to 8
        plt.rc('font', size=8)
        #alter_fonts()

    X_axis = np.arange(len(data.dagdatum))
    plot_chart(all_values, X_axis, data, "dagen")

    plt.grid(axis='y', linestyle='--')
    plt.xticks(X_axis, data.dagdatum, rotation=30)
    plt.xlabel('weekdagen')
    plt.legend(loc='upper right')
    # WEB is used in the webscripts and on the pc always False
    if WEB:
        ts = str(time.time()).split(".")
        plt.savefig(savedir + (ts[0]) + '.png', dpi=120)
        PNG = (ts[0]) + '.png'
        return PNG
    else:
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(gr_width / float(DPI), gr_height / float(DPI))
        #plt.show()
        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
        PNG = ''
        return PNG


def verbruik_per_week(window, data, all_values, WEB=False):
    #Get current plot/figure and clear it
    fig = plt.gcf()
    plt.clf()
    #X_axis = np.arange(len(data.weekno))
    X_axis = np.arange(len(data.wknrdatum))
    #print(data.wknrdatum)
    plot_chart(all_values, X_axis, data, "weken")

    plt.grid(axis='y', linestyle='--')
    #plt.xticks(X_axis, data.weekno)
    plt.xticks(X_axis, data.wknrdatum)
    plt.xlabel('weeknummers (datum)')
    # WEB is used in the webscripts and on the pc always False
    if WEB:
        ts = str(time.time()).split(".")
        plt.savefig(savedir + (ts[0]) + '.png', dpi=120)
        PNG = (ts[0]) + '.png'
        return PNG
    else:
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(gr_width / float(DPI), gr_height / float(DPI))
        # plt.show()
        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
        PNG = ''
        return PNG

def verbruik_per_maand(window, data, all_values, WEB=False):
    #Get current plot/figure and clear it
    fig = plt.gcf()
    plt.clf()
    X_axis = np.arange(len(data.month_name))

    plot_chart(all_values, X_axis, data, "maanden")
    plt.grid(axis='y', linestyle='--')
    #plt.xticks(X_axis, data.weekno)
    plt.xticks(X_axis, data.month_name)
    plt.xlabel('maandnummers (maand)')
    #plt.ylabel('kWh / m3')

    # WEB is used in the webscripts and on the pc always False
    if WEB:
        ts = str(time.time()).split(".")
        plt.savefig(savedir + (ts[0]) + '.png', dpi=120)
        PNG = (ts[0]) + '.png'
        return PNG
    else:
        # plt.title("energie verbruik/geleverd de afgelopen maanden")
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(gr_width / float(DPI), gr_height / float(DPI))
        # plt.show()
        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
        PNG = ''
        return PNG

def daily_totals(window, data):
    #Get current plot/figure and clear it
    fig = plt.gcf()
    plt.clf()
    X_axis = np.arange(len(data.datum))

    plt.bar(X_axis - 0.2, data.importkwh, 0.2, label = 'Import kWh')
    plt.bar(X_axis, data.exportkwh, 0.2, label = 'Export kWh')
    plt.bar(X_axis + 0.2, data.gastotaalm3, 0.2, label = 'gas m3')

    plt.xticks(X_axis, data.datum, rotation=30)
    plt.title("totaal energie over de afgelopen dagen")
    fig = plt.gcf()
    DPI = fig.get_dpi()
    # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
    fig.set_size_inches(gr_width / float(DPI), gr_height / float(DPI))
    #plt.show()
    # ------------------------------- Instead of plt.show()
    draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

