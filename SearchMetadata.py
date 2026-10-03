import cfg

class SearchMetadata:
    """
    Classe per cercar imatges dins un repositori de metadades.
    Versió optimitzada: Pre-calcula minúscules per evitar Timeouts.
    """

    def __init__(self, repositori_dades):
        self.repositori = repositori_dades
        
        self._cache = {
            "Prompt": [], "Model": [], "Seed": [], "CFG_Scale": [],
            "Steps": [], "Sampler": [], "Created_Date": []
        }

        # Carreguem dades a la memòria cau JA EN MINÚSCULES per velocitat
        for uuid, dada in self.repositori.imatges.items():
            if not dada.get("_carregat"):
                self.repositori.load_metadata(uuid)
            
            meta = self.repositori.imatges[uuid]
            
            # Guardem (uuid, valor_en_minuscules)
            if meta.get("Prompt"): self._cache["Prompt"].append((uuid, str(meta["Prompt"]).lower()))
            if meta.get("Model"): self._cache["Model"].append((uuid, str(meta["Model"]).lower()))
            if meta.get("Seed"): self._cache["Seed"].append((uuid, str(meta["Seed"]).lower()))
            if meta.get("CFG_Scale"): self._cache["CFG_Scale"].append((uuid, str(meta["CFG_Scale"]).lower()))
            if meta.get("Steps"): self._cache["Steps"].append((uuid, str(meta["Steps"]).lower()))
            if meta.get("Sampler"): self._cache["Sampler"].append((uuid, str(meta["Sampler"]).lower()))
            if meta.get("Created_Date"): self._cache["Created_Date"].append((uuid, str(meta["Created_Date"]).lower()))

    def _cercar(self, camp: str, subcadena: str) -> list:
        resultats = []
        subcadena_lower = subcadena.lower()
        
        # Cerca optimitzada (sense conversions .lower() dins del bucle)
        for uuid, valor_lower in self._cache[camp]:
            if subcadena_lower in valor_lower:
                resultats.append(uuid)
        
        return sorted(resultats)

    def prompt(self, subcadena: str) -> list: return self._cercar("Prompt", subcadena)
    def model(self, subcadena: str) -> list: return self._cercar("Model", subcadena)
    def seed(self, subcadena: str) -> list: return self._cercar("Seed", subcadena)
    def cfg_scale(self, subcadena: str) -> list: return self._cercar("CFG_Scale", subcadena)
    def steps(self, subcadena: str) -> list: return self._cercar("Steps", subcadena)
    def sampler(self, subcadena: str) -> list: return self._cercar("Sampler", subcadena)
    def date(self, subcadena: str) -> list: return self._cercar("Created_Date", subcadena)

    def and_operator(self, llista1: list, llista2: list) -> list:
        return sorted(list(set(llista1) & set(llista2)))

    def or_operator(self, llista1: list, llista2: list) -> list:
        return sorted(list(set(llista1) | set(llista2)))

    def __len__(self):
        return len(self.repositori.imatges)

    def __str__(self):
        return f"SearchMetadata: {len(self.repositori.imatges)} imatges disponibles"