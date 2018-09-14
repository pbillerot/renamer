#!/usr/bin/python
# -*- coding:Utf-8 -*-
"""
    Renommage des fichiers des sous-répertoires
"""
from __future__ import division
import shutil
import os
import datetime
import argparse
import glob

class Renamer():
    """ Fonction principale """

    def __init__(self, args):
        """ initialisation """
        # Chargement des paramètres
        self.args = args

        # run
        self.run()

    def display(self, msg):
        """ docstring """
        print(msg)
        # self.crud.logger.info(msg)

    def run(self):
        """ Exécution en cours... """
        racine = os.path.join(os.path.realpath("."), self.args.racine)
        self.traiteDossiers(racine, self.args.niveau)

    def traiteDossiers(self, rep, niv_atraiter=2, niv_courant=0):
        """ Traitement des dossiers """
        entrees = os.listdir(rep)
        # entrees.sort(key=lambda v: v.upper()) # tri sans tenir compte de la casse
        for entree in entrees:
            path = os.path.join(rep, entree)
            if os.path.isdir(path):
                if niv_courant <= niv_atraiter:
                    self.traiteDossiers(path, niv_atraiter, niv_courant+1)
            else:
                if niv_courant == niv_atraiter:
                    self.traiteFichier(path, entree, niv_courant)

    def traiteFichier(self, path, file_name, niveau):
        """ Traitement du fichier """
        # print ("traiteFichier: [%d]%s %s" % (niveau, file_name, path))
        basename = os.path.basename(path)  # os independent
        reps = os.path.dirname(path).split(os.sep)
        rep2 = reps.pop()
        rep1 = reps.pop()
        # rep2 = os.path.split(os.path.dirname(path))
        # rep1 = os.path.split(os.path.dirname(rep2[0]))
        base = basename.split('.')[0]
        ext = '.'.join(basename.split('.')[1:])   # <-- main part
        # if you want a leading '.', and if no result `None`:
        ext = '.' + ext if ext else None
        new_file = "%s-%s-_-%s%s" % (rep1, rep2, base, ext)
        new_path = os.path.join(os.path.dirname(path), new_file)
        if ( file_name.find('-_-') == -1):
            if os.path.isfile(new_path):
                print ("!!! REFUS existe déjà [%s]" % new_path)
            else:
                print ("%s -> %s" % (path, new_path))
                os.rename(path, new_path)
        # print ("")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='renamer')
    # add a -c/--color option
    parser.add_argument('-n', '--niveau', type=int, default=2,
                        help="Niveau du répertoires des fichiers à renommer")
    parser.add_argument('-r', '--racine', default="",
                        help="Répertoire racine")
    print(parser.parse_args())

    Renamer(parser.parse_args())
