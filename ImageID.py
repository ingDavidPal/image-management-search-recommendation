# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 23:11:35 2025

@author: david
"""

# ImageID.py
import cfg

class ImageID:
    def __init__(self):
        """
        Inicialitza el registre d'identificadors.

        Retorna:
            None
        """
        self.mapa_identificadors = {}  
    
    def generate_uuid(self, fitxer: str) -> str:
        """
        Crea un identificador únic per a un fitxer.

        Args:
            fitxer (str): Ruta canònica del fitxer.

        Retorna:
            str: UUID generat, o None si hi ha col·lisió.
        """
        identificador_nou = str(cfg.get_uuid(fitxer))
        
        if identificador_nou in self.mapa_identificadors:
            print(f"[ERROR] Identificador duplicat: {identificador_nou}")
            print(f"  Fitxer original: {self.mapa_identificadors[identificador_nou]}")
            print(f"  Fitxer ignorat: {fitxer}")
            return None
        
        self.mapa_identificadors[identificador_nou] = fitxer
        return identificador_nou
    
    def get_uuid(self, fitxer: str) -> str:
        """
        Consulta l'identificador d'un fitxer ja registrat.

        Args:
            fitxer (str): Ruta canònica del fitxer.

        Retorna:
            str: UUID si existeix, None altrament.
        """
        identificador_potencial = str(cfg.get_uuid(fitxer))
        
        if identificador_potencial in self.mapa_identificadors:
            return identificador_potencial
        
        return None
    
    def remove_uuid(self, identificador: str):
        """
        Elimina un identificador del registre actiu.

        Args:
            identificador (str): UUID a eliminar.

        Retorna:
            None
        """
        if identificador in self.mapa_identificadors:
            del self.mapa_identificadors[identificador]
    
    def get_file_from_uuid(self, identificador: str) -> str:
        """
        Obté la ruta de fitxer associada a un UUID.

        Args:
            identificador (str): UUID de la imatge.

        Retorna:
            str: Ruta del fitxer o None.
        """
        return self.mapa_identificadors.get(identificador, None)
    
    def __len__(self):
        """Retorna el nombre d'identificadors registrats."""
        return len(self.mapa_identificadors)
    
    def __str__(self):
        """Retorna la representació textual del registre."""
        return f"ImageID: {len(self.mapa_identificadors)} UUIDs registrats"