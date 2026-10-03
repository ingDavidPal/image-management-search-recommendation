# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 23:13:12 2025

@author: david
"""

import cfg
import os

class ImageViewer:
    def __init__(self, repositori_dades):
        self.repositori = repositori_dades
    
    def print_image(self, identificador: str):
        separador = "=" * 60
        print(f"\n{separador}")
        print(f"UUID: {identificador}")
        print(f"Fitxer: {self.repositori.get_file(identificador)}")
        print(f"Prompt: {self.repositori.get_prompt(identificador)}")
        print(f"Model: {self.repositori.get_model(identificador)}")
        print(f"Seed: {self.repositori.get_seed(identificador)}")
        print(f"CFG Scale: {self.repositori.get_cfg_scale(identificador)}")
        print(f"Steps: {self.repositori.get_steps(identificador)}")
        print(f"Sampler: {self.repositori.get_sampler(identificador)}")
        print(f"Generated: {self.repositori.get_generated(identificador)}")
        print(f"Data: {self.repositori.get_created_date(identificador)}")
        print(f"{separador}\n")
    
    def show_file(self, fitxer: str):
        # MOCK: No fem servir PIL perquè està prohibit a la segona entrega
        print(f"[ImageViewer] Visualització deshabilitada al servidor: {fitxer}")
    
    def show_image(self, identificador: str, mode: int):
        if mode == 0:
            self.print_image(identificador)
        elif mode == 1:
            self.print_image(identificador)
            fitxer = self.repositori.get_file(identificador)
            self.show_file(fitxer)
        elif mode == 2:
            fitxer = self.repositori.get_file(identificador)
            self.show_file(fitxer)
    
    def __len__(self):
        return len(self.repositori.imatges)  
    
    def __str__(self):
        return "ImageViewer"