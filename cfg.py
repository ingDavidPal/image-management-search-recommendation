import os
import uuid
import struct
import zlib

ROOT_DIR = r"generated_images"

IMAGE_DEFAULT = "42be33f4-a5c4-488a-80c1-5d10c713e0dc.png"

DISPLAY_MODE = 1

def get_root() -> str:
    return os.path.realpath(ROOT_DIR)

def get_uuid(filename: str = "") -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, filename))

def get_canonical_pathfile(filename: str) -> str:
    file = os.path.normpath(filename)
    file = file.replace(os.sep, '/')
    return file

def get_one_file(mode: int = 0) -> str:
    return os.path.join(ROOT_DIR, IMAGE_DEFAULT)

def read_png_metadata(filepath: str) -> dict:
    """
    Llegeix metadades PNG (tEXt, zTXt, iTXt) sense utilitzar PIL.
    Fa servir 'struct' i 'zlib' (estàndards) per extreure tota la informació.
    """
    metadata = {}
    if not os.path.exists(filepath):
        return metadata

    try:
        with open(filepath, 'rb') as f:
            if f.read(8) != b'\x89PNG\r\n\x1a\n':
                return {}

            while True:
                # Llegir longitud (4 bytes)
                buf = f.read(4)
                if len(buf) < 4: break
                length = struct.unpack('>I', buf)[0]
                
                # Llegir tipus de chunk (4 bytes)
                chunk_type = f.read(4)
                
                # Llegir dades del chunk
                data = f.read(length)
                
                f.read(4)

                # Processar chunks de text
                if chunk_type == b'tEXt':
                    if b'\x00' in data:
                        key, val = data.split(b'\x00', 1)
                        try:
                            metadata[key.decode('latin-1')] = val.decode('latin-1')
                        except: pass
                
                elif chunk_type == b'zTXt':
                    if b'\x00' in data:
                        key, rest = data.split(b'\x00', 1)
                        if len(rest) > 1 and rest[0] == 0: # 0 = deflate
                            try:
                                val_compressed = rest[1:]
                                val = zlib.decompress(val_compressed)
                                metadata[key.decode('latin-1')] = val.decode('latin-1')
                            except: pass

                elif chunk_type == b'iTXt':
                    try:
                        if b'\x00' in data:
                            key, rest = data.split(b'\x00', 1)
                            if len(rest) > 4:
                                comp_flag = rest[0]
                                parts = rest[2:].split(b'\x00', 2)
                                if len(parts) == 3:
                                    val_bytes = parts[2]
                                    if comp_flag == 1:
                                        val_bytes = zlib.decompress(val_bytes)
                                    metadata[key.decode('utf-8')] = val_bytes.decode('utf-8')
                    except: pass

                elif chunk_type == b'IEND':
                    break
                    
    except Exception:
        pass
        
    return metadata