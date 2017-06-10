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

import re
import pywikibot

def main():
    site = pywikibot.Site('madripedia', 'wikiscc')
    page = pywikibot.Page(site, "User:Madripediabot/Spam")
    wtext = page.text
    spamtitles = re.findall(r"\[\[([^\[\]]*?)\]\]", wtext)
    spamtitles.sort()
    spamtitles2 = spamtitles
    for spamtitle in spamtitles:
        spampage = pywikibot.Page(site, spamtitle)
        if spampage.exists():
            print("\n\n%s\n== %s ==" % ('#'*50, spamtitle))
            if re.search("(?im)bien?venid?[ao]", spampage.text):
                print("\n%s\nParece que le dieron la {{bienvenida}}, saltando..." % ('-'*50))
                continue
            print(spampage.text)
            print("\n%s\n" % ('-'*50))
            delete = input("* Borrar esta pagina? (Por defecto es [S]i. Para mantener, [N]o. Puedes [T]erminar el script y continuar despues): ")
            if delete == "" or delete.lower() in ['s', 'si', 'y', 'yes']:
                print("OK, borrando pagina...")
                spampage.delete(reason="BOT - Borrando spam", prompt=False)
                spamtitles2.remove(spamtitle)
            elif delete.lower() in ['t', 'terminar']:
                print("OK, terminando script...")
                break
        else:
            spamtitles2.remove(spamtitle)
    print("Actualizando pagina de spam. Quitando los borrados...")
    page.text = "\n".join(["# [[%s]]" % (x) for x in spamtitles2])
    page.save("BOT - Actualizando lista")

if __name__ == '__main__':
    main()
