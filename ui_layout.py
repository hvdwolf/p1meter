# -*- coding: utf-8 -*-

# ui_layout.py - This python helper scripts holds the user interface functions

# Copyright (c) 2022, Harry van der Wolf. all rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public Licence as published
# by the Free Software Foundation, either version 2 of the Licence, or
# version 3 of the Licence, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public Licence for more details.

import PySimpleGUI as sg

import os, platform


#----------------------------------------------------------------------------------------------
#---------------------  Main function that builds the whole gui  ------------------------------
#----------------------------------------------------------------------------------------------
def create_and_show_gui():
# This creates the complete gui and then returns the gui
# to pyimagefuser where the events are evaluated

    # Sizes for our canvas and mathplots. These values need to be the same in mpgraphs.py and ui_layout.py
    gr_width = 450*3
    gr_height = 808

    sg.theme('SystemDefault1') # I hate all these colourful, childish themes. Please play with it and then grow up.
    sg.SetOptions(font = ('Helvetica', 12))

    MLINE_KEY = '-ML-'+sg.WRITE_ONLY_KEY        # multiline element's key. Indicate it's an output only element
    layoutOutputTab = [ [sg.Multiline('Uitvoer venster\n', size=(120,40), key=MLINE_KEY)], ]

    layoutPlotTab = [[sg.Canvas(key='controls_cv')],
                     [sg.Column(
                     layout=[
                             # it's important that you set this size 
                             [sg.Canvas(key='fig_cv',size=(gr_width, gr_height))] ],
                             background_color='#DAE0E6',
                             pad=(0, 0) )
                     ],
                ] 
# sg.Button('Gescheiden vandaag'), ==> werk niet goed
    dagenLayout = [ [ sg.Button('Verbruik per dag'), sg.Text('aantal: '),sg.Radio('7', "aantaldagen", default=True, key='_zeven_'), sg.Radio('14', "aantaldagen", default=False, key='_veertien_'), sg.Radio('onbeperkt', "aantaldagen", default=False, key='_onbeperkt_')] ]

    mainLayout = [ [sg.Text('Stroomverbruik', font = ('any', 12, 'bold')), sg.Button('Vandaag'), sg.CalendarButton('Op datum', key='_CALENDAR_', target='-CAL-', format=( '%Y-%m-%d'),locale='nl_NL',), sg.Text('Gasverbruik', font = ('any', 12, 'bold')), sg.Button('Vandaag', key='_gasvandaag_'), sg.CalendarButton('Op datum', key='_GCALENDAR_', target='-GCAL-', format=( '%Y-%m-%d'),locale='nl_NL',),],
               [sg.Text('Verbruiks Overzichten', font = ('any', 12, 'bold')), sg.Frame('', dagenLayout), sg.Button('Verbruik per week'), sg.Button('Dagelijkse totalen'), sg.Button('Sluiten', button_color=('white', 'firebrick3'))],
               [sg.Text('Diagram type Verbruiks Overzichten', font = ('any', 12, 'bold')), sg.Radio('Staafdiagram', "grafiektype", default=True, key='_staaf_'), sg.Radio('Lijndiagram', "grafiektype", default=False, key='_lijn_')],
               #[sg.Text('', key='_progress_msg')],
               [sg.In(key='-CAL-', enable_events=True, visible=False), sg.In(key='-GCAL-', enable_events=True, visible=False)],
               [sg.TabGroup([[sg.Tab('Grafiek', layoutPlotTab, key='_PlotTab_'),
                             sg.Tab('Tekst Uitvoer', layoutOutputTab, key='_OutputTab_'),
               ]])],
               ] 


    # Open the window and return it to pyimagefuser
    return sg.Window('Overzicht p1 meter data', mainLayout)
