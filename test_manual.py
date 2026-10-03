import json
from pathlib import Path

# Rutas
vectors_path = Path(r"\Users\david\OneDrive\Pictures\Documentos\Data engineering\2on Curs\1er semestre\Estructura de dades\proyecto\autograder\clip_vectors_private.json")
ground_truth_path = Path(r"\Users\david\OneDrive\Pictures\Documentos\Data engineering\2on Curs\1er semestre\Estructura de dades\proyecto\autograder\ground_truth.json")

# Cargar datos
with open(vectors_path, 'r') as f:
    vectors_data = json.load(f)
    raw_vectors = vectors_data.get("vectors", vectors_data)

with open(ground_truth_path, 'r') as f:
    ground_truth = json.load(f)

print("=== VERIFICACIÓN DE UUIDs ===")
print(f"Vectores en JSON: {len(raw_vectors)}")
print(f"Queries en ground truth: {len(ground_truth)}")

# Verificar algunos UUIDs del ground truth
sample_queries = list(ground_truth.keys())[:5]
print("\nPrimeras 5 queries del ground truth:")
for query in sample_queries:
    print(f"  {query}")
    
    # Verificar si está en vectores
    if query in raw_vectors:
        print(f"    ✓ ENCONTRADO en vectores")
    else:
        print(f"    ✗ NO encontrado en vectores")
        
        # Buscar variantes
        found = False
        for vector_key in raw_vectors.keys():
            if query in vector_key or vector_key in query:
                print(f"    ? Posible match: {vector_key}")
                found = True
                break
        
        if not found:
            print(f"    ✗ No hay coincidencias cercanas")

print("\nPrimeras 5 claves de vectores:")
for i, key in enumerate(list(raw_vectors.keys())[:5]):
    print(f"  {i+1}. {key}")
