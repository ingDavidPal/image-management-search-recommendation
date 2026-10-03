# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 23:12:37 2025

@author: david
"""

# ImageData.py
import cfg
import os

class ImageData:
    def __init__(self):
        self.imatges = {}

    def add_image(self, uuid: str, fitxer: str):
        self.imatges[uuid] = {
            "fitxer": fitxer,
            "Prompt": None, "Model": None, "Seed": None,
            "CFG_Scale": None, "Steps": None, "Sampler": None,
            "Generated": None, "Created_Date": None, "_carregat": False
        }

    def remove_image(self, uuid: str):
        self.imatges.pop(uuid, None)

    def load_metadata(self, uuid: str):
        if uuid not in self.imatges or self.imatges[uuid]["_carregat"]:
            return
        
        fitxer_registrat = self.imatges[uuid]["fitxer"]
        filename = os.path.basename(fitxer_registrat)
        
        posibles_rutas = [
            fitxer_registrat,
            os.path.join("images", filename),
            os.path.join(os.getcwd(), "images", filename),
            os.path.join("/autograder/source/images", filename)
        ]
        
        path_correcte = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                path_correcte = ruta
                break
        
        if not path_correcte:
            if os.path.exists(fitxer_registrat):
                 path_correcte = fitxer_registrat
            else:
                 return

        try:
            meta = cfg.read_png_metadata(path_correcte) or {}
        except:
            meta = {}

        meta_lower = {k.lower(): v for k, v in meta.items()}
        camps = ["Prompt", "Model", "Seed", "CFG_Scale", "Steps", "Sampler", "Generated", "Created_Date"]
        
        for camp in camps:
            val = None
            if camp in meta:
                val = meta[camp]
            elif camp.lower() in meta_lower:
                val = meta_lower[camp.lower()]
            
            self.imatges[uuid][camp] = str(val) if val is not None else None
            
        self.imatges[uuid]["_carregat"] = True

    def _get(self, uuid, camp):
        if uuid not in self.imatges:
            return None
        if not self.imatges[uuid]["_carregat"]:
            self.load_metadata(uuid)
        return self.imatges[uuid].get(camp)

    def get_prompt(self, uuid): return self._get(uuid, "Prompt")
    def get_model(self, uuid): return self._get(uuid, "Model")
    def get_seed(self, uuid): return self._get(uuid, "Seed")
    def get_cfg_scale(self, uuid): return self._get(uuid, "CFG_Scale")
    def get_steps(self, uuid): return self._get(uuid, "Steps")
    def get_sampler(self, uuid): return self._get(uuid, "Sampler")
    def get_generated(self, uuid): return self._get(uuid, "Generated")
    def get_created_date(self, uuid): return self._get(uuid, "Created_Date")
    
    def get_file(self, uuid):
        return self.imatges.get(uuid, {}).get("fitxer")

    def __len__(self):
        return len(self.imatges)

    def __str__(self):
        return f"ImageData({len(self.imatges)})"