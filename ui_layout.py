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
# Vorige: [sg.Text('Verbruiks Overzichten', font = ('any', 12, 'bold')), sg.Frame('', dagenLayout), sg.Button('Verbruik per week'), sg.Button('Dagelijkse totalen'), sg.Button('Sluiten', button_color=('white', 'firebrick3'))],
#                [sg.Text('Verbruiks Overzichten', font = ('any', 12, 'bold')), sg.Frame('', dagenLayout), sg.Button('Verbruik per week'), sg.Button('Verbruik per maand'), sg.Button('Sluiten', button_color=('white', 'firebrick3'))],
    # per periode
    periodeLayout = [ [ sg.Text('periodes (dagen/weken/maanden): '), sg.Push(), sg.Radio('4', "aantalperiodes", default=False, key='_vier_'), sg.Radio('7', "aantalperiodes", default=True, key='_zeven_'), sg.Radio('12', "aantalperiodes", default=False, key='_twaalf_'), sg.Radio('14', "aantalperiodes", default=False, key='_veertien_'), sg.Radio('30', "aantalperiodes", default=False, key='_dertig_'), sg.Radio('onbeperkt', "aantalperiodes", default=False, key='_onbeperkt_')] ]
    # Create a 7, 14, unlimited day layout
    dagenLayout = [ [ sg.Button('Verbruik per dag'), sg.Text('aantal: '),sg.Radio('7', "aantaldagen", default=True, key='_zeven_'), sg.Radio('14', "aantaldagen", default=False, key='_veertien_'), sg.Radio('30', "aantaldagen", default=False, key='_dertig_'), sg.Radio('onbeperkt', "aantaldagen", default=False, key='_onbeperkt_')] ]
    # create a layout for an overview per type: used, produced, gas
    typelayout = [ [ sg.Radio('Verbruikt/Geproduceerd/Gas', 'type', default=True, key='t_alles'), sg.Radio('Verbruikt/Geproduceerd', 'type', default=False, key='t_electrisch'), sg.Radio('Verbruikt', 'type', default=False, key='t_verbruikt'), sg.Radio('Geproduceerd', 'type', default=False, key='t_geproduceerd'), sg.Radio('Gas verbruik', 'type', default=False, key='t_gasverbruik') ]]
    # Combine both periode and type layout into one
    optiesLayout = [ [ sg.Text('periodes (dagen/weken/maanden): ', font = ('any', 10, 'bold')), sg.Push(), sg.Radio('4', "aantalperiodes", default=False, key='_vier_'), sg.Radio('7', "aantalperiodes", default=True, key='_zeven_'), sg.Radio('12', "aantalperiodes", default=False, key='_twaalf_'), sg.Radio('14', "aantalperiodes", default=False, key='_veertien_'), sg.Radio('30', "aantalperiodes", default=False, key='_dertig_'), sg.Radio('onbeperkt', "aantalperiodes", default=False, key='_onbeperkt_')],
                     [ sg.Text('Type grafiek:', font = ('any', 10, 'bold')), sg.Radio('Verbruikt/Geproduceerd/Gas', 'type', default=True, key='t_alles'), sg.Radio('Verbruikt/Geproduceerd', 'type', default=False, key='t_electrisch'), sg.Radio('Verbruikt', 'type', default=False, key='t_verbruikt'), sg.Radio('Geproduceerd', 'type', default=False, key='t_geproduceerd'), sg.Radio('Gas verbruik', 'type', default=False, key='t_gasverbruik') ],
                   ]
    optiesFrameLayout = [ [sg.Frame('', optiesLayout) ] ]
    optiesTextLayout = [ [sg.Text('Selectie opties', font = ('any', 12, 'bold')),] ]

    mainLayout = [ [sg.Text('Stroomverbruik', font = ('any', 12, 'bold')), sg.Button('Vandaag'), sg.CalendarButton('Op datum', key='_CALENDAR_', target='-CAL-', format=( '%Y-%m-%d'),locale='nl_NL',), sg.Text('Gasverbruik', font = ('any', 12, 'bold')), sg.Button('Vandaag', key='_gasvandaag_'), sg.CalendarButton('Op datum', key='_GCALENDAR_', target='-GCAL-', format=( '%Y-%m-%d'),locale='nl_NL',),],
                   [sg.Text('Overzichten', font=('any', 12, 'bold')), sg.Button('Per dag'), sg.Button('Per week'), sg.Button('Per maand'), ],
                   #[sg.Text('Selectie opties', font = ('any', 12, 'bold')), sg.Push(), sg.Frame('', periodeLayout),],
                   #[sg.Push(), sg.Frame('', typelayout) ],
                   [sg.Column(optiesTextLayout, vertical_alignment='top'), sg.Push(), sg.Column(optiesFrameLayout,  vertical_alignment='top')],
               [sg.Text('Diagram type Verbruiks Overzichten', font = ('any', 12, 'bold')), sg.Radio('Staafdiagram', "grafiektype", default=True, key='_staaf_'), sg.Radio('Lijndiagram', "grafiektype", default=False, key='_lijn_'), sg.Push(), sg.Button('Programma afsluiten', button_color=('white', 'firebrick3'))],
               #[sg.Text('', key='_progress_msg')],
               [sg.In(key='-CAL-', enable_events=True, visible=False), sg.In(key='-GCAL-', enable_events=True, visible=False)],
               [sg.TabGroup([[sg.Tab('Grafiek', layoutPlotTab, key='_PlotTab_'),
                             sg.Tab('Tekst Uitvoer', layoutOutputTab, key='_OutputTab_'),
               ]])],
               ] 


    # Open the window and return it to pyimagefuser
    return sg.Window('Overzicht p1 meter data', mainLayout)
