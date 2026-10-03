# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 23:08:09 2025

@author: david
"""

# ImageFiles.py
import os
import cfg

class ImageFiles:
    def __init__(self):
        """
        Inicialitza les estructures per emmagatzemar arxius.

        Retorna:
            None
        """
        self.arxius_actuals = []      
        self.arxius_anteriors = []    
    
    def reload_fs(self, ruta: str):
            self.arxius_anteriors = list(self.arxius_actuals)
            self.arxius_actuals = []
            
            if not os.path.exists(ruta):
                return
            
            try:
                for directori_actual, subdirectoris, fitxers in os.walk(ruta):
                    for nom_fitxer in fitxers:
                        if nom_fitxer.lower().endswith('.png'):
                            try:
                                ruta_completa = os.path.join(directori_actual, nom_fitxer)
                                
                                if not os.path.isfile(ruta_completa):
                                    continue
                                ruta_relativa = os.path.relpath(ruta_completa, ruta)
                                ruta_relativa = ruta_relativa.replace(os.sep, '/')
                                if os.path.basename(os.path.normpath(ruta)) == 'images':
                                    if not ruta_relativa.startswith('images/'):
                                        ruta_relativa = f"images/{ruta_relativa}"

                                self.arxius_actuals.append(ruta_relativa)                            
                            except Exception:
                                continue
            
            except Exception:
                pass
    
    def files_added(self) -> list:
        """
        Retorna els fitxers nous des del darrer escaneig.

        Retorna:
            list: Fitxers que abans no existien.
        """
        nous_fitxers = []
        for fitxer in self.arxius_actuals:
            if fitxer not in self.arxius_anteriors:
                nous_fitxers.append(fitxer)
        return nous_fitxers
    
    def files_removed(self) -> list:
        """
        Retorna els fitxers eliminats des del darrer escaneig.

        Retorna:
            list: Fitxers que estaven abans però ja no hi són.
        """
        fitxers_esborrats = []
        for fitxer in self.arxius_anteriors:
            if fitxer not in self.arxius_actuals:
                fitxers_esborrats.append(fitxer)
        return fitxers_esborrats
    
    def __len__(self):
        """Retorna el nombre d'arxius actuals."""
        return len(self.arxius_actuals)

    def __str__(self):
        """Retorna la representació textual de l'objecte."""
        return f"ImageFiles: {len(self.arxius_actuals)} arxius"