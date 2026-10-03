import json
import cfg
import os


class Gallery:
    def __init__(self, visualitzador, gestor_ids):
        """
        Constructor de la galeria.

        Args:
            visualitzador: Objecte encarregat de mostrar imatges.
            gestor_ids: Gestor dels UUIDs de les imatges.
        """
        self.viewer = visualitzador
        self.gestor = gestor_ids
        self.nom = ""
        self.descripcio = ""
        self.data = ""
        self.llista = []

    def load_file(self, arxiu: str):
        """
        Carrega una galeria des d’un fitxer JSON.

        Si el fitxer no existeix o està buit, inicialitza la galeria com a buida.
        Si conté imatges repetides, només es manté una instància per UUID.

        Args:
            arxiu (str): Ruta del fitxer JSON.
        """
        # Netejar l’estat anterior
        self.nom = ""
        self.descripcio = ""
        self.data = ""
        self.llista = []

        if not os.path.exists(arxiu):
            # Si el fitxer no existeix, la galeria queda buida
            return

        try:
            with open(arxiu, 'r', encoding='utf-8') as f:
                dades = json.load(f)

            # Assignació segura dels camps
            self.nom = dades.get('gallery_name', '')
            self.descripcio = dades.get('description', '')
            self.data = dades.get('created_date', '')

            for ruta in dades.get('images', []):
                uuid = self._buscar_uuid(ruta)
                if uuid and uuid not in self.llista:  # Evita duplicats
                    self.llista.append(uuid)

        except Exception:
            # Si hi ha error, la galeria queda buida
            self.nom = ""
            self.descripcio = ""
            self.data = ""
            self.llista = []

    def _buscar_uuid(self, ruta: str) -> str:
        """
        Troba el UUID associat a una ruta d’imatge.

        Args:
            ruta (str): Ruta original de la imatge.

        Retorna:
            str: UUID si es troba, sinó None.
        """
        ruta = ruta.strip()

        # Intent directe
        uuid = self.gestor.get_uuid(ruta)
        if uuid:
            return uuid

        # Normalització
        try:
            ruta_norm = cfg.get_canonical_pathfile(ruta)
            uuid = self.gestor.get_uuid(ruta_norm)
            if uuid:
                return uuid
        except Exception:
            pass

        # Treure prefixos habituals
        for prefix in [
            cfg.ROOT_DIR + '/',
            'generated_images/',
            cfg.ROOT_DIR + '\\',
            'generated_images\\'
        ]:
            if ruta.startswith(prefix):
                ruta_neta = ruta[len(prefix):].replace('\\', '/')
                uuid = self.gestor.get_uuid(ruta_neta)
                if uuid:
                    return uuid

        # Normalitzar barres
        ruta_barres = ruta.replace('\\', '/')
        uuid = self.gestor.get_uuid(ruta_barres)
        if uuid:
            return uuid

        # Buscar per nom de fitxer (últim recurs)
        nom = os.path.basename(ruta)
        for uid, fitxer in self.gestor.mapa_identificadors.items():
            if os.path.basename(fitxer) == nom:
                return uid

        return None

    def show(self):
        """
        Mostra tota la informació de la galeria i visualitza les imatges.
        """
        print(f"\n{'='*60}")
        print(f"GALERIA: {self.nom}")
        print(f"Descripció: {self.descripcio}")
        print(f"Data: {self.data}")
        print(f"Total: {len(self.llista)}")
        print(f"{'='*60}\n")

        for i, uuid in enumerate(self.llista, 1):
            print(f"\n--- Imatge {i}/{len(self.llista)} ---")
            self.viewer.show_image(uuid, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid: str):
        """
        Afegeix una imatge al final de la galeria si no hi és ja.

        Args:
            uuid (str): Identificador de la imatge.
        """
        if uuid not in self.llista:
            self.llista.append(uuid)

    def remove_first_image(self):
        """
        Elimina la primera imatge de la galeria.
        """
        if self.llista:
            self.llista.pop(0)

    def remove_last_image(self):
        """
        Elimina l’última imatge de la galeria.
        """
        if self.llista:
            self.llista.pop()

    def __len__(self):
        """Retorna el nombre d’imatges a la galeria."""
        return len(self.llista)

    def __str__(self):
        """Retorna la representació textual de la galeria."""
        return f"Gallery '{self.nom}': {len(self.llista)} imatges"