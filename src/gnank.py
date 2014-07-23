#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

# Gnank - cercador d'horaris de la FIB
# Copyright (C) 2006, 2007  Albert Gasset Romo
#
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


import sys
import os
from os.path import dirname, join
import logging
from traceback import format_exception


FORMAT_REGISTRE = '%(asctime)s %(levelname)-8s %(message)s'


def configura_registre():
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    handler.setFormatter(logging.Formatter(FORMAT_REGISTRE))
    logger.addHandler(handler)


def configura_registre_fitxer(fitxer):
    try:
        handler = logging.FileHandler(fitxer)
    except IOError as e:
        logging.warning("Error en obrir el registre: %s", e)
    else:
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(FORMAT_REGISTRE))
        logging.getLogger("").addHandler(handler)


def registra_excepcio(tipus, value, tb):
    text = "".join(format_exception(tipus, value, tb))
    logging.error("S'ha produït una excepció.\n%s", text)


def configura_directori():
    gnank_dir = os.environ.get("GNANK_DIR")
    if gnank_dir is None:
        if sys.platform == "win32":
            gnank_dir = dirname(sys.argv[0])
        else:
            prefix = dirname(dirname(__file__))
            gnank_dir = join(prefix, "share", "gnank")
        os.environ["GNANK_DIR"] = gnank_dir
    sys.path.insert(0, gnank_dir)


def main():
    configura_registre()
    sys.excepthook = registra_excepcio

    configura_directori()
    import config
    config.crea_dir_usuari()
    configura_registre_fitxer(config.REGISTRE_USUARI)

    try:
        import psyco
        psyco.full()
        logging.info("S'ha activat el mòdul Psyco.")
    except ImportError:
        # hack per evitar el missatge d'error en tancar gnank a Windows
        if sys.platform != "win32":
            logging.warning("No s'ha trobat el mòdul Psyco.")

    logging.info("S'iniciarà l'aplicació.")
    import gui
    gui.inicia()
    logging.info("Es tancarà l'aplicació.")

    logging.shutdown()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
