# -*- coding: utf-8 -*-
#@author: comet

import tkinter as tk
from tkinter import messagebox
import locale as lcl
import xml.etree.ElementTree as ET
from pathlib import Path
import matplotlib.pyplot as plt
import datetime as dtme
import time
import math
import numpy as np
import os

#Backlog
#Teildauern ausgaben
#Diagramme - y-Achse - Teilung entsprechend Distanz
#charakteristische Werte für Routen fertigstellen
#  - Schlussstück
#charakteristische Werte für Tracks/Tracksegmente fertigstellen
#  - Schlussstück
#  - Rotationsenergie
#Eingabedialog

class winddialog(object):
    def __init__(self, parent):
        self.wdir = tk.StringVar() # Variale für Windrichtung
        self.wspd = tk.StringVar() # Variale für Windgeschwindigkeit
        self.top = tk.Toplevel(parent)
        self.frDir = tk.Frame(self.top)
        self.frDir.pack(side=tk.TOP, fill=tk.BOTH)
        txtstr = 'Windrichtung in Grad'
        self.lblDir = tk.Label(self.frDir, text=txtstr)
        self.lblDir.pack(side=tk.LEFT)
        self.entDir = tk.Entry(self.frDir, textvariable = self.wdir)
        self.entDir.pack(side=tk.LEFT)
        self.frSpd = tk.Frame(self.top)
        self.frSpd.pack(side=tk.TOP, fill=tk.BOTH)
        txtstr = 'Windgeschwindigkeit in m/s'
        self.lblSpd = tk.Label(self.frSpd, text=txtstr)
        self.lblSpd.pack(side=tk.LEFT)
        self.entSpd = tk.Entry(self.frSpd, textvariable = self.wspd)
        self.entSpd.pack(side=tk.LEFT)
        #Felgendurchmesser Felgenmitte
        #Raddurchmesser
        #Speichenzahl
        #Speichendurchmesser
        #Gesamtgewicht
        self.frBtn = tk.Frame(self.top)
        self.frBtn.pack(side=tk.TOP, fill=tk.BOTH)
        self.btnOK = tk.Button(self.frBtn, text='OK', underline=0,
                               command=self.ok)
        self.btnOK.pack(side=tk.LEFT, padx=5, pady=5)
        self.btnCancel = tk.Button(self.frBtn, text='Abbrechen',
                                   underline=0,command=self.cancel)
        self.btnCancel.pack(side=tk.LEFT, padx=5, pady=5)

    def ok(self):
        self.top.destroy()

    def ergebnis(self):
        wgeschw = self.wspd.get()
        wrichtung = self.wdir.get()
        while wrichtung > 360:
            wrichtung -= 360
        while wrichtung < 0:
            wrichtung += 360
        return(wgeschw, wrichtung)

    def cancel(self):
        self.top.destroy()

    def ergebnis(self):
        return()

class topo(object):
    def __init__(self, parent, blst, llst):
        self.blst = blst
        self.llst = llst
        self.top = tk.Toplevel(parent)
        tk.Label(self.top, text='Topografische Darstellung').pack()
        bmin = bmax = self.blst[0]
        lmin = lmax = self.llst[0]
        for cnt, ele in enumerate(blst, 0):
            if cnt > 0:
                bmin = min(bmin, self.blst[cnt])
                bmax = max(bmax, self.blst[cnt])
                lmin = min(lmin, self.llst[cnt])
                lmax = max(lmax, self.llst[cnt])
        distns = 36000/400*(bmax - bmin)
        distew = 36000/400*(lmax - lmin)*math.cos((lmax + lmin)/2*math.pi/180)
        if distns > distew: #schmale hohe Karte
            cnvwidth = int(600*distew/distns + 0.5)
            cnvheight = 600
        else: #breite niedrige Karte
            cnvwidth = 600
            cnvheight = int(600*distns/distew + 0.5)
        self.frameTop = tk.Frame(self.top) #Rahmen für Canvas
        self.frameTop.pack(side=tk.TOP, fill=tk.BOTH)
        self.frameDwn = tk.Frame(self.top) #Rahmen für Button
        self.frameDwn.pack(side=tk.TOP, fill=tk.BOTH)
        self.cnvtopo = tk.Canvas(self.frameTop,
                                 width=cnvwidth, height=cnvheight)
        self.cnvtopo.pack(side=tk.TOP, padx=5, pady=5)
        self.btnOK = tk.Button(self.frameDwn, text='OK', command=self._ok,
                               underline = 0)
        self.btnOK.pack(side=tk.LEFT, padx=5, pady=5)
        erstlauf = True
        for cnt, ele in enumerate(blst, 0):
            _x = (self.llst[cnt] - lmin)/(lmax - lmin)*cnvwidth*\
                math.cos((lmax + lmin)/2*math.pi/180)
            _y = (bmax - self.blst[cnt])/(bmax - bmin)*cnvheight
            if erstlauf:
                erstlauf = False
                _x0 = _x
                _y0 = _y
            else:
                self.cnvtopo.create_line(_x, _y, _xalt, _yalt, fill='blue')
            _xalt = _x
            _yalt = _y

    def _ok(self):
        self.top.destroy()

class tdelta(object):
    def __init__(self):
        pass
    
    def dstrkomp(self, sekzahl):
        dzahl = hzahl = mzahl = 0
        if sekzahl < 0:
            ausstr = '-('
            endstr = ')'
        else:
            ausstr = ''
            endstr = ''
        sekzahl = abs(sekzahl)
        if sekzahl > 86400:
            dzahl = sekzahl//86400
            sekzahl -= dzahl*86400
            ausstr += str(dzahl) + 'd, '
        if sekzahl > 3600:
            hzahl = sekzahl//3600
            sekzahl -= hzahl*3600
            ausstr += str(hzahl) + 'h, '
        if sekzahl > 60:
            mzahl = sekzahl//60
            sekzahl -= mzahl*60
            ausstr += str(mzahl) + 'm, '
        return(ausstr + str(sekzahl) + 's' +  endstr)
    
    def set1(self, ye, mo, da, hh = 0, mm = 0, ss = 0):
        self.__dt1s = dtme.datetime(ye, mo, da, hh, mm, ss)
        self.__dt1d = dtme.datetime(ye, mo, da)
    
    def set2(self, ye, mo, da, hh = 0, mm = 0, ss = 0):
        self.__dt2s = dtme.datetime(ye, mo, da, hh, mm, ss)
        self.__dt2d = dtme.datetime(ye, mo, da)
        
    def now1(self):
        now = dtme.datetime.now()
        self.__dt1s = dtme.datetime(now.year, now.month, now.day,
                                    now.hour, now.minute, now.second)
        
    def now2(self):
        now = dtme.datetime.now()
        self.__dt2s = dtme.datetime(now.year, now.month, now.day,
                                    now.hour, now.minute, now.second)
        
    def file1(self, dn):
        ftime = os.path.getmtime(dn)
        fye = int(time.strftime('%Y', time.localtime(ftime)))
        fmo = int(time.strftime('%m', time.localtime(ftime)))
        fda = int(time.strftime('%d', time.localtime(ftime)))
        fhh = int(time.strftime('%H', time.localtime(ftime)))
        fmm = int(time.strftime('%M', time.localtime(ftime)))
        fss = int(time.strftime('%S', time.localtime(ftime)))
        self.__dt1s = dtme.datetime(fye, fmo, fda, fhh, fmm, fss)
        
    def file2(self, dn):
        ftime = os.path.getmtime(dn)
        fye = int(time.strftime('%Y', time.localtime(ftime)))
        fmo = int(time.strftime('%m', time.localtime(ftime)))
        fda = int(time.strftime('%d', time.localtime(ftime)))
        fhh = int(time.strftime('%H', time.localtime(ftime)))
        fmm = int(time.strftime('%M', time.localtime(ftime)))
        fss = int(time.strftime('%S', time.localtime(ftime)))
        self.__dt2s = dtme.datetime(fye, fmo, fda, fhh, fmm, fss)
    
    def dseksgn(self):
        self.__tdelta = (self.__dt2s - self.__dt1s).seconds
        self.__tdelta += 86400*(self.__dt2s - self.__dt1s).days
        return(self.__tdelta)
    
    def ddaysgn(self):
        self.__tdelta = (self.__dt2d - self.__dt1d).days
        return(self.__tdelta)
        
    def dstrsgn(self):
        return(self.dstrkomp(self.dseksgn()))
    
    def dsekabs(self):
        self.__tdelta = abs(self.dseksgn())
        return(self.__tdelta)
    
    def ddayabs(self):
        self.__tdelta = abs(self.ddaysgn())
        return(self.__tdelta)
        
    def dstrabs(self):
        return(self.dstrkomp(abs(self.dseksgn())))
        
    def out1dmy(self):
        return(self.__dt1s.strftime('%d.%m.%Y'))
    
    def out1ges(self):
        return(self.__dt1s.strftime('%d.%m.%Y, %H:%M:%S'))

    def out2dmy(self):
        return(self.__dt2s.strftime('%d.%m.%Y'))

    def out2ges(self):
        return(self.__dt2s.strftime('%d.%m.%Y, %H:%M:%S'))
  

class gpxanalyse(object):
    def __init__(self, dname):
        self.dn = dname
        self.dnok = False
        myfile = Path(self.dn)
        if myfile.is_file():
            self.dnok = True
        components = self.dn.split('.')
        if components[-1] != 'gpx':
            self.dnok = False
        self.blst = []
        self.llst = []

    def _ausgplot(self, ylbl=''):
        pltlst = np.array(self.ausglst)
        plt.plot(pltlst)
        if ylbl != '':
            plt.ylabel(ylbl)
        plt.xlabel('Schritt')
        plt.show()

    def _analyse(self, modus):
        """
        Hier findet die eigentliche Analyse der GPX-Datei statt.
        Die Ausgabe der Werte erfolgt in den Funktionen aus_xxx.
        für den Funktionsüarameter <modus> gilt:
        <modus> == 1: Ausgabe der Koordinatenliste
        <modus> == 2: Ausgabe des Höhenverlaufs
        <modus> == 3: Ausgabe der Teildauer einzelner Schritte
        <modus> == 4: Ausgabe der Richtungen
        <modus> == 5: Ausgabe der Teillängen
        <modus> == 6: Ausgabe der Teilleistungen
        <modus> == 7: Ausgabe der Energien
        <modus> == 8: Ausgabe der Steigungen
        <modus> == 9: Ausgabe der Teilgeschwindigkeiten

        Für die Ermittlung der Energie und Leistung werden
        Näherungswerte für Rollwiderstand, Reibungswiderstand,
        Gesamtmasse und cw-Wert eingesetzt.
        Quelle: https://www.leifiphysik.de/mechanik/
        reibung-und-fortbewegung/ausblick/
        reibungskraefte-beim-fahrradfahren
        """
        if self.dnok:
            self.blst = []
            self.llst = []
            self.ausglst = []
            self.elevlst = []
            self.tmelst = []
            self.dstlst = []
            tree = ET.parse(self.dn)
            root = tree.getroot()
            altgbr = altgle = 0
            for gen1 in root:
                for gen2 in gen1:
                    lst1 = gen2.tag.split('}')
                    erstlauf = True
                    if lst1[1] == 'trkseg':
                        for gen3 in gen2:
                            lst2 = str(gen3.attrib).split('\'')
                            gbr = float(lst2[3])
                            gle = float(lst2[7])
                            self.blst.append(gbr)
                            self.llst.append(gle)
                            if modus == 2: #Höhenverlauf
                                for gen4 in gen3: 
                                    if str(gen4.tag).find('ele') >= 0:
                                        elestr = str(gen4.text)
                                        self.ausglst.append(float(elestr))
                                    if erstlauf:
                                        erstlauf = False
                                    else:
                                        dist = self._dist(gbr, gle,
                                                          altgbr, altgle)
                                        self.dstlst.append(dist)
                                    altgbr = gbr
                                    altgle = gle
                            elif modus == 3: #Zeitpunkte/Teildauer
                                for gen4 in gen3: 
                                    if str(gen4.tag).find('time') >= 0:
                                        zeitstr = str(gen4.text)
                                        self.tmelst.\
                                            append(self._zeitwert(zeitstr))
                            elif modus == 5: #Teillängen
                                if erstlauf:
                                    erstlauf = False
                                else:
                                    dist = self._dist(altgbr, altgle,
                                                      gbr, gle)
                                    self.ausglst.append(dist)
                                altgbr = gbr
                                altgle = gle
                            elif modus == 6: #Teilleistungen
                                for gen4 in gen3: 
                                    if str(gen4.tag).find('time') >= 0:
                                        zeitstr = str(gen4.text)
                                        self.tmelst.\
                                            append(self._zeitwert(zeitstr))
                                    if str(gen4.tag).find('ele') >= 0:
                                        elestr = str(gen4.text)
                                        self.elevlst.append(float(elestr))
                                    if erstlauf:
                                        erstlauf = False
                                    else:
                                        dist = self._dist(gbr, gle,
                                                          altgbr, altgle)
                                        self.dstlst.append(dist)
                                    altgbr = gbr
                                    altgle = gle
                            elif modus == 7: #Energie
                                for gen4 in gen3: 
                                    if str(gen4.tag).find('time') >= 0:
                                        zeitstr = str(gen4.text)
                                        self.tmelst.\
                                            append(self._zeitwert(zeitstr))
                                    if str(gen4.tag).find('ele') >= 0:
                                        elestr = str(gen4.text)
                                        self.elevlst.append(float(elestr))
                                    if erstlauf:
                                        erstlauf = False
                                    else:
                                        dist = self._dist(gbr, gle,
                                                          altgbr, altgle)
                                        self.dstlst.append(dist)
                                    altgbr = gbr
                                    altgle = gle
                            elif modus == 8: #Steigungen
                                for gen4 in gen3: 
                                    if str(gen4.tag).find('ele') >= 0:
                                        elestr = str(gen4.text)
                                        hoehe = float(elestr)
                                        dist = self._dist(altgbr,
                                                          altgle, gbr, gle)
                                        if erstlauf:
                                            erstlauf = False
                                        else:
                                            if dist != 0:
                                                stg = 100*(hoehe - h_alt)/dist
                                                self.ausglst.append(stg)
                                        altgbr = gbr
                                        altgle = gle
                                        h_alt = hoehe
                            elif modus == 9: #Teilgeschwindigkeiten
                                for gen4 in gen3: 
                                    if str(gen4.tag).find('time') >= 0:
                                        zeitstr = str(gen4.text)
                                        self.tmelst.\
                                            append(self._zeitwert(zeitstr))
                                    if erstlauf:
                                        erstlauf = False
                                    else:
                                        dist = self._dist(gbr, gle,
                                                          altgbr, altgle)
                                        self.dstlst.append(dist)
                                    altgbr = gbr
                                    altgle = gle
            rwz = 0.00404 #Rollwiderstandzahl
            gerde = 9.81 #Gravitationsstärke der Erde (Oberfläche)
            mass = 95 #Gesamtmasse (Fahrrad + Fahrer)
            rrz = 1 #Rollreibungszahl
            cw = 1.1 #cw-Wert
            rho = 1.2041 #Luftdichte in kg/m³
            flaeche = 0.45 #Stirnfläche Rad + Fahrer im m²
            lwkonst = cw*flaeche*rho/2
            freib = rwz*mass*gerde #Reibungswiderstand in Newton
            froll = 0.2 #Rollwiderstand in Newton
            mfelge = 0.54 #Gewicht einer Felge in kg
            l2speiche = 0.6 #Länge von zwei gegenüberliegenden Speichen
            duspeiche = 0.002 #Durchmesser einer Speiche
            rhostahl = 7850 #Dichte von Stahl in km/m³
            fspeiche = math.pi*duspeiche*duspeiche/4 #Querschnitt Speiche
            jges = 2*(l2speiche**3*mfelge + \
                fspeiche*l2speiche*rhostahl*\
                l2speiche*l2speiche/12) #Trägheitsmoment der Räder
            rreifen = 2.193/(2*math.pi) #Radius mit Reifen 622x38
            if modus == 1: #Koordinaten
                return(self.blst, self.llst)
            elif modus == 2: #Höhenverlauf
                self._ausgplot('Höhe/m')
                return(self.ausglst)
            elif modus == 3: #Zeitpunkte/Teildauer
                for cnt, ele in enumerate(self.tmelst, 0):
                    if cnt > 0:
                        tdelta = (self.tmelst[cnt] - \
                            self.tmelst[cnt - 1]).seconds
                        self.ausglst.append(tdelta)
                self._ausgplot('Dauer/s')
            elif modus == 4: #Richtungen
                lmin = lmax = self.llst[0]
                for ele in self.llst:
                    lmin = min(lmin, ele)
                    lmax = max(lmax, ele)
                korr = math.cos((lmin + lmax)/2*math.pi/180)
                for cnt, ele in enumerate(self.blst, 0):
                    if cnt > 0:
                        dgl = korr*(self.llst[cnt] - glalt)
                        dgb = self.blst[cnt] - gbalt
                        if not((dgl == 0) and (dgb == 0)):
                            if dgb != 0:
                                winkel = 180/math.pi*math.atan(dgl/dgb)
                                if dgb < 0:
                                    winkel = 180.
                            else:
                                if dgl >0:
                                    winkel = 90.
                                else:
                                    winkel = 270.
                            while winkel < 0:
                                winkel += 360
                            while winkel > 360:
                                winkel -= 360
                            self.ausglst.append(winkel)
                    gbalt = self.blst[cnt]
                    glalt = self.llst[cnt]
                self._ausgplot('Richtung/°')
                return(self.ausglst)
            elif modus == 5: #Teillängen
                self._ausgplot('Teillänge/m')
                return(self.ausglst)
            elif modus == 6: #Teilleistungen
                for cnt, ele in enumerate(self.tmelst, 0):
                    if cnt > 0:
                        tdelta = (self.tmelst[cnt] - \
                            self.tmelst[cnt - 1]).seconds
                        if (self.dstlst[cnt - 1] != 0) and (tdelta != 0):
                            geschw = 1000*self.dstlst[cnt - 1]/tdelta #in m/s
                            hdelta = (self.elevlst[cnt] - \
                                self.elevlst[cnt - 1])
                            wi = math.atan(hdelta/self.dstlst[cnt - 1])
                            fsteig = mass*gerde*math.sin(wi*math.pi/180)
                            fges = froll + freib + fsteig + \
                                        lwkonst*geschw*geschw
                            power = fges*geschw
                            self.ausglst.append(power)
                self._ausgplot('Teilleistung/W')
                return(self.ausglst)
            elif modus == 7: #Energie
                for cnt, ele in enumerate(self.tmelst, 0):
                    if cnt > 0:
                        tdelta = (self.tmelst[cnt] - \
                            self.tmelst[cnt - 1]).seconds
                        if (self.dstlst[cnt - 1] != 0) and (tdelta != 0):
                            geschw = 1000*self.dstlst[cnt - 1]/tdelta #in m/s
                            hdelta = (self.elevlst[cnt] - \
                                self.elevlst[cnt - 1])
                            wi = math.atan(hdelta/self.dstlst[cnt - 1])
                            fsteig = mass*gerde*math.sin(wi*math.pi/180)
                            fges = froll + freib + fsteig + \
                                        lwkonst*geschw*geschw
                            work = fges*self.dstlst[cnt - 1]*1000
                            self.ausglst.append(work)
                self._ausgplot('Teilenergie/J')
                return(self.ausglst)
            elif modus == 8: #Steigungen
                self._ausgplot('Steigung/')
                return(self.ausglst)
            elif modus == 9: #Teilgeschwindigkeiten
                for cnt, ele in enumerate(self.tmelst, 0):
                    if cnt > 0:
                        tdelta = (self.tmelst[cnt] - \
                            self.tmelst[cnt - 1]).seconds
                        if tdelta > 0:
                            spd = self.dstlst[cnt - 1]/tdelta
                            self.ausglst.append(spd)
                self._ausgplot('Geschwindigkeit/')
                return(self.ausglst)

    def _dist(self, b1, l1, b2, l2):
        """
        Berechnet die Entfernung zwischen zwei Punkten auf der Erdoberlfäche
        in Kilometern
        Funktionsparameter:
        <b1> geogr. Breite Punkt 1 in Grad
        <l1> geogr. Länge Punkt 1 in Grad
        <b2> geogr. Breite Punkt 2 in Grad
        <l2> geogr. Länge Punkt 2 in Grad
        """
        bmf = math.pi / 180 #Faktor für die Umrechnung in Bogenmaß
        if (b1 == b2) and (l1 == l2): #Null-Distanz vor Berechnung ausfiltern
            return(0)
        else: #Distanz ungleich Null
            b1 *= bmf
            l1 *= bmf
            b2 *= bmf
            l2 *= bmf
            arg = math.cos(l1)*math.cos(b1)*math.cos(l2)*math.cos(b2) + \
                math.sin(l1)*math.cos(b1)*math.sin(l2)*math.cos(b2) + \
                math.sin(b1)*math.sin(b2)
            if arg > 1: #Fehler abfangen
                arg = 1
            elif arg < -1: #Fehler abfangen
                arg = -1
            return(20000 / math.pi*math.acos(arg))

    def _zeitwert(self, dtstr):
        l0 = dtstr.split('T')
        dstr = l0[0]
        dlst = dstr.split('-')
        tstr = l0[1]
        tstr = tstr.replace('Z', '')
        tlst = tstr.split(':')
        seklst = tlst[2].split('.')
        if len(seklst) > 1:
            tlst[2] = seklst[0]
        return dtme.datetime(int(dlst[0]), int(dlst[1]), int(dlst[2]),
                             int(tlst[0]), int(tlst[1]), int(tlst[2]))

    def aus_krd(self, teilgruppe, segnr=-1):
        """
        Ausgabe der Koordinatenliste der einzelnen Punkte für
        Tracks/Tracksegmente, Routen oder Wegpunkte.
        <teilgruppe> == 0 => Ausgabe der Route
        <teilgruppe> == 1 => Ausgabe eines Track(segment)s
        <teilgruppe> == 2 => Ausgabe der Wegpunkte
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        Ohne Angabe von <segnr> werden alle Tracksegement ausgegeben.
        Rückgabe: <self.gblst>, <self.gllst>: Liste der geogr. Längen
        bzw. Breiten.
        """
        self._analyse(1)
        return(self.blst, self.llst)

    def aus_elev(self, segnr=-1):
        """
        Ausgabe der Höhen in Meter der einzelnen Punkte für
        Tracks/Tracksegmente.
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        Rückgabe: <self.elevlst>: Liste der Höhen in Meter.
        """
        self.elevlst = self._analyse(2)
        return(self.elevlst)

    def aus_time(self, segnr=-1):
        """
        Ausgabe der Zeitpunkte der Teilschritte für Tracks/Tracksegmente.
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!).
        Rückgabe: <self.tmelst>: Liste der Zeiten. Die Zeiten werden als
        Strings ausgegeben.
        """
        self.tmelst = self._analyse(3)
        return(self.tmelst)

    def aus_dirs(self, teilgruppe, segnr=-1):
        """
        Ausgabe der Richtungen der Teilschritte für Tracks/Tracksegmente
        oder Routen.
        oder Wegpunkte.
        <teilgruppe> == 0 => Ausgabe der Route
        <teilgruppe> == 1 => Ausgabe eines Track(segment)s
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        Rückgabe: <self.dirlst>: Liste der Richtungen in Grad.
        """
        self.dirlst = self._analyse(4)
        return(self.dirlst)

    def aus_partlen(self, teilgruppe, segnr=-1):
        """
        Ausgabe der Längen der Teilschritte für Tracks/Tracksegmente
        oder Routen.
        <teilgruppe> == 0 => Ausgabe der Route
        <teilgruppe> == 1 => Ausgabe eines Track(segment)s
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        Rückgabe: <self.lenlst>: Liste der Teillängen in Kilometer.
        """
        self.lenst = self._analyse(5)
        return(self.lenst)

    def aus_power(self, segnr=-1, wspd=0, wdir=0):
        """
        Ausgabe der Leistung auf den Teilschritte für Tracks/Tracksegmente
        oder Routen. Für den jeweiligen Teilschritt wird angenommen, dass
        mit konstanter Geschwindigkeit geafhren wird, die Steigung konstant
        ist und sich der Wind nicht ändert.
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        <wspd> == Windgeschwindigkeit in m/s
        <wdir> == Windrichtung in Grad
        Rückgabe: <self.pwrlst>: Liste der Teilleistungen in Watt.
        """
        self.pwrlst = self._analyse(6)
        return(self.pwrlst)
    
    def aus_energy(self, segnr=-1, gewicht=95, wspd=0, wdir=0):
        """
        Ausgabe der Leistung auf den Teilschritte für Tracks/Tracksegmente
        oder Routen. Für den jeweiligen Teilschritt wird angenommen, dass
        mit konstanter Geschwindigkeit geafhren wird, die Steigung konstant
        ist und sich der Wind nicht ändert.
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        <wspd> == Windgeschwindigkeit in m/s
        <wdir> == Windrichtung in Grad
        Rückgabe: <self.nrglst>: Liste der Teilenergien in Joule.
        """
        self.nrglst = self._analyse(7)
        return(self.nrglst)

    def aus_rise(self, segnr=-1):
        """
        Ausgabe der Steigungen der Teilschritte für Tracks/Tracksegmente
        oder Routen.
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        Rückgabe: <self.riselst>: Liste der Steigungen in Grad.
        """
        self.riselst = self._analyse(8)
        return(self.riselst)

    def aus_spds(self, segnr=-1):
        """
        Ausgabe der Geschwindigkeiten der Teilschritte für
        Tracks/Tracksegmente.
        <segnr> == auszugebendes Tracksegment (beginnt mit 0!)
        Rückgabe: <self.spdslst>: Liste der Steigungen in Grad.
        """
        self.spdslst = self._analyse(9)
        return(self.spdslst)

    def _char_rte(self):
        lges = 0
        anzp = 0
        distlst = []
        erstlauf = True
        firstdist = True
        if self.dnok:
            tree = ET.parse(self.dn)
            root = tree.getroot()
            altgbr = altgle = 0
            for gen1 in root:
                for gen2 in gen1:
                    lst1 = gen2.tag.split('}')
                    erstlauf = True
                    if lst1[1] == 'rte':
                        for gen3 in gen2:
                            lst2 = str(gen3.attrib).split('\'')
                            gbr = float(lst2[3])
                            gle = float(lst2[7])
                            anzp += 1
                            if erstlauf:
                                maxn = maxs = gbr
                                maxo = maxw = gle
                                mxnnr = mxonr = mxsnr = mxwnr = anzp
                                erstlauf = False
                            else:
                                if gbr > maxn:
                                    maxn = gbr
                                    mxnnr = anzp
                                if gbr < maxs:
                                    maxs = gbr
                                    mxsnr = anzp
                                if gle > maxo:
                                    maxo = gle
                                    mxonr = anzp
                                if gle < maxw:
                                    maxw = gle
                                    mxwnr = anzp
                                dist = self._dist(altgbr, altgle,
                                                  gbr, gle)
                                if firstdist:
                                    lsmin = lsmax = dist
                                    firstdist = False
                                else:
                                    lsmin = min(lsmin, dist)
                                    lsmax = min(lsmax, dist)
                                distlst.append(dist)
                                lges += dist
                            altgbr = gbr
                            altgle = gle
        qsumme = 0
        if anzp > 1:
            lmittel = lges/(anzp - 1)
            for ele in distlst:
                qsumme += (ele - lmittel)**2
            stdabwdist = math.sqrt(qsumme)
        else:
            stdabwdist = 0
        mxmstr = 'Nördlichster Punk: ' + str(maxn)
        mxmstr += '° (' + str(mxnnr) + '. Punkt)'
        mxmstr += '\nÖstlichster Punkt: ' + str(maxo)
        mxmstr += '° (' + str(mxsnr) + '. Punkt)'
        mxmstr += '\nSüdlichster Punkt: ' + str(maxs)
        mxmstr += '° (' + str(mxonr) + '. Punkt)'
        mxmstr += '\nWestlichster Punkt: ' + str(maxw)
        mxmstr += '° (' + str(mxwnr) + '. Punkt)'
        return(lges, lsmin, lsmax, anzp, stdabw, mxmstr)

    def _char_trk(self):
        lges = 0
        anzp = 0
        tges = 0
        distlst = []
        dauerlst = []
        erstlauf = True
        firstdist = True
        hges = 0
        if self.dnok:
            tree = ET.parse(self.dn)
            root = tree.getroot()
            altgbr = altgle = 0
            for gen1 in root:
                for gen2 in gen1:
                    lst1 = gen2.tag.split('}')
                    erstlauf = True
                    if lst1[1] == 'trkseg':
                        for gen3 in gen2:
                            lst2 = str(gen3.attrib).split('\'')
                            gbr = float(lst2[3])
                            gle = float(lst2[7])
                            for gen4 in gen3: 
                                if str(gen4.tag).find('time') >= 0:
                                    zeitstr = str(gen4.text)
                                if str(gen4.tag).find('ele') >= 0:
                                    elevation = float(str(gen4.text))
                            anzp += 1
                            if erstlauf:
                                erstlauf = False
                                maxn = maxs = gbr
                                maxo = maxw = gle
                                mxnnr = mxonr = mxsnr = mxwnr = anzp
                            else:
                                if gbr > maxn:
                                    maxn = gbr
                                    mxnnr = anzp
                                if gbr < maxs:
                                    maxs = gbr
                                    mxsnr = anzp
                                if gle > maxo:
                                    maxo = gle
                                    mxonr = anzp
                                if gle < maxw:
                                    maxw = gle
                                    mxwnr = anzp
                                dist = self._dist(altgbr, altgle,
                                                  gbr, gle)
                                dauer = (self._zeitwert(zeitstr) - \
                                    self._zeitwert(altzstr)).seconds
                                tges += dauer
                                dauerlst.append(dauer)
                                if elevation > altele:
                                    hges += elevation - altele
                                if firstdist:
                                    lsmin = lsmax = dist
                                    firstdist = False
                                else:
                                    lsmin = min(lsmin, dist)
                                    lsmax = min(lsmax, dist)
                                distlst.append(dist)
                                lges += dist
                            altgbr = gbr
                            altgle = gle
                            altzstr = zeitstr
                            altele = elevation
        qsumme = 0
        if anzp > 1:
            lmittel = lges/(anzp - 1)
            for ele in distlst:
                qsumme += (ele - lmittel)**2
            stdabwdist = math.sqrt(qsumme)
            tmittel = tges/(anzp - 1)
            for ele in dauerlst:
                qsumme += (ele - tmittel)**2
            stdabwtime = math.sqrt(qsumme)
        else:
            stdabwdist = 0
            stdabwtime = 0
        mxmstr = 'Nördlichster Punk: ' + str(maxn)
        mxmstr += '° (' + str(mxnnr) + '. Punkt)'
        mxmstr += '\nÖstlichster Punkt: ' + str(maxo)
        mxmstr += '° (' + str(mxsnr) + '. Punkt)'
        mxmstr += '\nSüdlichster Punkt: ' + str(maxs)
        mxmstr += '° (' + str(mxonr) + '. Punkt)'
        mxmstr += '\nWestlichster Punkt: ' + str(maxw)
        mxmstr += '° (' + str(mxwnr) + '. Punkt)'
        return(lges, lsmin, lsmax, tges, hges, anzp, \
            stdabwdist, stdabwtime, mxmstr)

    def aus_char(self):
        """
        Ausgabe der charakteristischen Werte der GPX-Datei
        Rückgabe:
        <aussstr> String mit den formatierten und
        ausformulierten cahrakteristischen Werten
        """
        if self.dnok:
            ausstr = 'Dateiname: ' + self.dn
            ausstr += '\nDateigröße: '
            ausstr += self._grstring(os.path.getsize(self.dn), True)
            ausstr += '\nletztes Änderungsdatum: '
            dtime = time.localtime(os.path.getmtime(self.dn))
            ausstr += time.strftime("%d.%m.%Y %H:%M:%S", dtime)
            tdlt = tdelta()
            tdlt.file1(self.dn)
            tdlt.now2()
            ausstr += '\nDateialter: ' + tdlt.dstrsgn()
            trkcnt = 0
            rtecnt = 0
            tree = ET.parse(self.dn)
            root = tree.getroot()
            for gen1 in root:
                lst1 = gen1.tag.split('}')
                if lst1[1] == 'rte':
                    rtecnt += 1
                for gen2 in gen1:
                    lst1 = gen2.tag.split('}')
                    if lst1[1] == 'trkseg':
                        trkcnt += 1
            ausstr += '\n\nAnzahl Routen: ' + str(rtecnt)
            ausstr += '\nAnzahl Tracks: ' + str(trkcnt)
            if rtecnt > 0:
                ausstr += '\n\nRoute(n):'
                self.lges, self.lsmin, self.lsmax, self.anzp, \
                    self.stdabw, self.maxminstr = \
                    self._char_rte()
                ausstr += '\nGesamtlänge: '
                ausstr += lcl.format('%0.2f', self.lges, 1) + 'km'
                ausstr += '\nAnzahl Punkte: '
                ausstr += lcl.format('%d', self.anzp, 1) + 'km'
                if self.anzp > 1:
                    ausstr += '\nMittlere Länge je Schritt: '
                    ausstr += lcl.format('%0.2f', self.lges/\
                        (self.anzp - 1), 1) + 'km'
                ausstr += '\nMaximale Länge eines Schrittes: '
                ausstr += lcl.format('%0.2f', self.lsmax, 1) + 'km'
                ausstr += '\nMinimale Länge eines Schrittes: '
                ausstr += lcl.format('%0.2f', self.lsmin, 1) + 'km'
                ausstr += '\nStandardabweichung Länge: '
                ausstr += lcl.format('%0.2f', self.stdabw, 1) + 'km'
                ausstr += '\n' + self.maxminstr
            if trkcnt > 0:
                ausstr += '\n\nTrack(s):'
                self.lges, self.lsmin, self.lsmax, self.tges, \
                    self.hges, self.anzp, self.stdabwdist, self.stabwtime, \
                    self.maxminstr = self._char_trk()
                ausstr += '\nGesamtlänge: '
                ausstr += lcl.format('%0.2f', self.lges, 1) + 'km'
                ausstr += '\nAnzahl Punkte: '
                ausstr += lcl.format('%d', self.anzp, 1) + 'km'
                if self.anzp > 1:
                    ausstr += '\nMittlere Länge je Schritt: '
                    ausstr += lcl.format('%0.2f', self.lges/\
                        (self.anzp - 1), 1) + 'km'
                ausstr += '\nMaximale Länge eines Schrittes: '
                ausstr += lcl.format('%0.2f', self.lsmax, 1) + 'km'
                ausstr += '\nMinimale Länge eines Schrittes: '
                ausstr += lcl.format('%0.2f', self.lsmin, 1) + 'km'
                ausstr += '\nStandardabweichung Länge: '
                ausstr += lcl.format('%0.2f', self.stdabwdist, 1) + 'km'
                ausstr += '\nMaximale Gesamtdauer: '
                ausstr += lcl.format('%d', self.tges, 1) + 's'
                ausstr += '\nAnstieg gesamt: '
                ausstr += lcl.format('%0.2f', self.hges, 1) + 'm'
                ausstr += '\n' + self.maxminstr
            return(ausstr)

    def _grstring(self, ein, plus = False):
        if plus:
            retstr = lcl.format('%d', ein, 1) + ' Byte'
            if abs(ein) >= 10000:
                retstr += ' ('
        else:
            retstr = ''
        if abs(ein) < 10000: #Byte
            if plus == False:
                retstr += lcl.format('%d', ein, 1) + ' Byte'
        elif abs(ein) < 1024 * 1024: #kByte
            retstr += lcl.format('%0.2f', ein / 1024, 1) + ' kB'
        elif abs(ein) < 1024 * 1024 * 1024: #MByte
            retstr += lcl.format('%0.2f', ein / (1024 * 1024), 1) + ' MB'
        else: #GByte
            retstr += lcl.format('%0.2f', ein / (1024 * 1024 * 1024), 1) + ' GB'
        if plus:
            if abs(ein) >= 10000:
                return(retstr + ')')
            else:
                return(retstr)
        else:
            return(retstr)

def selmsg(dn):
    msgstr = 'Aktuelle GPX-Datei: ' + dn
    messagebox.showinfo('Programminformation', msgstr)

def seldn1():
    global gpxdn
    gpxdn = dllst[0]
    selmsg(gpxdn)

def seldn2():
    global gpxdn
    gpxdn = dllst[1]
    selmsg(gpxdn)

def seldn3():
    global gpxdn
    gpxdn = dllst[2]
    selmsg(gpxdn)

def seldn4():
    global gpxdn
    gpxdn = dllst[3]
    selmsg(gpxdn)

def seldn5():
    global gpxdn
    gpxdn = dllst[4]
    selmsg(gpxdn)

def mkchar():  #charakteristische Werte
    gpx = gpxanalyse(gpxdn)
    print(gpx.aus_char())

def mktopo(): #Topologische Darstellung
    gpx = gpxanalyse(gpxdn)
    (gbrlst, glelst) = gpx.aus_krd(1)
    tpo = topo(root, gbrlst, glelst)

def mktstr(): #Länge der Teilstrecken
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_partlen(1)

def mktdura(): #Teildauer
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_time()

def mkspds(): #Geschwindigkeiten
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_spds()

def mkheig(): #Höhneverlauf
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_elev(1)

def mkdirs(): #Richtungen
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_dirs(1)

def mkstgn(): #Steigungen
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_rise()

def mkenrg(): #Energie
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_energy()

def mkpowr(): #Energie
    gpx = gpxanalyse(gpxdn)
    ausglst = gpx.aus_power()

def winddef():
    wdlg = winddialog(root)
    root.wait_window(wdlg.top)
    (wgeschw, wrichtung) = wdlg.ergebnis()
    del(wdlg)

if __name__== "__main__":
    version = '1.35' #globale Versionskonstante
    lcl.setlocale(lcl.LC_NUMERIC, '')
    pfad = 'D:/AK-Dateien/Temp_Desktop/'
    dllst = [pfad + 'Lang1.gpx']
    dllst.append(pfad + 'Roermond_Aug_2018_Angepasst.gpx')
    dllst.append(pfad + 'Roermond_Aug_2018_Orig.gpx')
    dllst.append(pfad + 'Umrandung201014.gpx')
    dllst.append(pfad + 'Solingen_Sinzig.gpx')
    wspd = 0 #Windgeschwindigkeit in m/s
    wdir = 0 #Windrichtung in Grad (von da kommt der Wind)
    root = tk.Tk()
    gpxdn = ''
    seldn3() #gpxdn wird seldn3 gesetzt
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Datei', underline=0, menu = filemenu)
    filemenu.add_command(label=dllst[0], underline=0, command=seldn1)
    filemenu.add_command(label=dllst[1], underline=0, command=seldn2)
    filemenu.add_command(label=dllst[2], underline=0, command=seldn3)
    filemenu.add_command(label=dllst[3], underline=0, command=seldn4)
    filemenu.add_command(label=dllst[4], underline=0, command=seldn5)
    filemenu.add_command(label='Beenden', underline=0,
                         command=root.destroy, accelerator='Alt+F4')
    ausgmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Ausgabe', underline=0, menu = ausgmenu)
    ausgmenu.add_command(label='Charakteristische Werte',
                         underline=0, command=mkchar)
    ausgmenu.add_command(label='Topologie', underline=0, command=mktopo)
    ausgmenu.add_command(label='Teilstrecken', underline=0, command=mktstr)
    ausgmenu.add_command(label='Teildauer', underline=0, command=mktdura)
    ausgmenu.add_command(label='Geschwindigkeiten', underline=0,
                         command=mkspds)
    ausgmenu.add_command(label='Höhen', underline=0, command=mkheig)
    ausgmenu.add_command(label='Richtungen', underline=0, command=mkdirs)
    ausgmenu.add_command(label='Steigung', underline=0, command=mkstgn)
    ausgmenu.add_command(label='Energie', underline=0, command=mkenrg)
    ausgmenu.add_command(label='Leistung', underline=0, command=mkpowr)
    optimenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Einstellungen', underline=0, menu = optimenu)
    optimenu.add_command(label='Wind definieren', underline=0,
                         command=winddef)
    root.config(menu = menubar)
    root.mainloop()