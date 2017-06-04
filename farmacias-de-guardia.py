#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import datetime
import urllib.request
import pywikibot

zonas = {
    "ARAVACA": "[[Barrio de Aravaca|Aravaca]]", 
    "BARAJAS-ALAMEDA DE OSUNA": "[[Distrito de Barajas|Barajas]]-[[Barrio de Alameda de Osuna|Alameda de Osuna]]", 
    "CARABANCHEL-LATINA": "[[Distrito de Carabanchel|Carabanchel]]-[[Distrito de La Latina|Latina]]", 
    "CENTRO": "[[Distrito de Centro|Centro]]", 
    "CHAMARTIN-HORTALEZA": "[[Distrito de Chamartín|Chamartín]]-[[Distrito de Hortaleza|Hortaleza]]", 
    "CHAMBERI-MONCLOA": "[[Distrito de Chamberí|Chamberí]]-Moncloa", 
    "CIUDAD LINEAL-SAN BLAS": "[[Distrito de Ciudad Lineal|Ciudad Lineal]]-[[Distrito de San Blas|San Blas]]", 
    "FUENCARRAL-BARRIO DEL PILAR": "[[Distrito de Fuencarral-El Pardo|Fuencarral]]-[[Barrio del Pilar]]", 
    "PUEBLO DE VALLECAS": "[[Distrito de Villa de Vallecas|Pueblo de Vallecas]]", 
    "PUENTE DE VALLECAS-ENTREVIAS": "Puente de Vallecas-Entrevías", 
    "RETIRO-ARGANZUELA": "[[Distrito de Retiro|Retiro]]-[[Distrito de Arganzuela]]", 
    "SALAMANCA-VENTAS": "[[Distrito de Salamanca|Salamanca]]-[[Barrio de Ventas|Ventas]]", 
    "TETUAN-CUATRO CAMINOS": "[[Distrito de Tetuán|Tetuán]]-[[Barrio de Cuatro Caminos|Cuatro Caminos]]", 
    "USERA-VILLAVERDE": "[[Distrito de Usera|Usera]]-[[Distrito de Villaverde|Villaverde]]", 
    "VICALVARO": "[[Distrito de Vicálvaro|Vicálvaro]]", 
}

def main():
    site = pywikibot.Site('madripedia', 'wikiscc')
    farmacias = []
    csvurl = "http://datos.madrid.es/egob/catalogo/214440-0-farmacias-guardia.csv"
    with urllib.request.urlopen(csvurl) as f:
        reader = csv.reader(f.read().decode("latin-1").splitlines(), delimiter=';', quotechar='"')
        for row in reader:
            farmacias.append(row)
    
    servicios = {
        "SERVICIO 24 HORAS (DE 9'30 A 9'30)": { "tabla": [], "setinternal": [], "pagina": "Farmacias de Guardia 24 HORAS en Madrid" }, 
        "SERVICIO DE 7'00 A 23'00 HORAS": { "tabla": [], "setinternal": [], "pagina": "Farmacias abiertas hoy de 07:00 a 23:00 en Madrid" }, 
        "SERVICIO DIURNO (DE 9'30 A 21'30)": { "tabla": [], "setinternal": [], "pagina": "Farmacias abiertas hoy de 09:30 a 21:30 en Madrid" }, 
        "SERVICIO DIURNO (DE 9'30 A 23'00)": { "tabla": [], "setinternal": [], "pagina": "Farmacias abiertas hoy de 09:30 a 23:00 en Madrid" }, 
        "SERVICIO NOCTURNO (DE 23'00 A 9,30)": { "tabla": [], "setinternal": [], "pagina": "Farmacias abiertas hoy de 23:00 a 09:30 en Madrid" }, 
    }
    hoy = datetime.datetime.today().strftime("%d/%m/%Y")
    for localidad, barrio, fecha, farmacia, direccion, duracion, telefono in farmacias:
        direccionlimpia = direccion.split('(')[0].strip()
        if fecha == hoy:
            zonaenlace = zonas[barrio]
            servicios[duracion]["tabla"].append("\n|-\n| %s || %s || 91%s " % (zonaenlace, direccion, telefono))
            servicios[duracion]["setinternal"].append("{{#set_internal:farmaciadeguardia\n|dirección=%s\n|teléfono=%s\n|coordenadas={{#geocode:%s, Madrid}}\n|horario=%s\n}}""" % (direccion, telefono, direccionlimpia, duracion))
    
    for servicio, props in servicios.items():
        output = """
<center>
{| class="wikitable" style="width: 100%%;"
! Horarios: [[Farmacias abiertas hoy de 07:00 a 23:00 en Madrid|07:00-23:00]]{{·}} [[Farmacias abiertas hoy de 09:30 a 21:30 en Madrid|09:30-21:30]]{{·}} [[Farmacias abiertas hoy de 09:30 a 23:00 en Madrid|09:30-23:00]]{{·}} [[Farmacias abiertas hoy de 23:00 a 09:30 en Madrid|23:00-09:30]]{{·}} [[Farmacias de Guardia 24 HORAS en Madrid|24 HORAS]]
|}
{{#ask: [[farmaciadeguardia::+]] [[horario::%s]]
|?dirección
|?teléfono
|?coordenadas
|format=leaflet
}}
{| class="wikitable sortable"
|+ %s (%s)
|-
! Zona !! Dirección !! Teléfono""" % (servicio, props["pagina"], hoy)
        output += ''.join(props["tabla"])
        output += """
|}

Origen de los datos: Ayuntamiento de Madrid (<span class="plainlinks">[http://datos.madrid.es datos.madrid.es]</span>)

</center>"""
        setinternal = ''.join(props["setinternal"])
        output = setinternal + output
        page = pywikibot.Page(site, props["pagina"])
        page.text = output
        page.save("BOT - Actualizando")
    
if __name__ == '__main__':
    main()
