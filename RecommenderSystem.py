import json
import os
import math
import heapq
import random
from collections import Counter
from Gallery import Gallery
import cfg

class RecommenderSystem:
    def __init__(self, vectors_path, image_data, image_id):
        self.vectors_path = vectors_path
        self.image_data = image_data
        self.image_id = image_id
        
        self.vectors = {}
        self.all_uuids = [] 
        
        self.map_name_to_id = {} 
        self.loaded = False
        
        self.searcher = None
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'of', 'in', 'on', 'at', 'with', 'is', 'are', 'by', 'to', 'from',
            'it', 'that', 'this', 'for', 'as', 'but', 'not', 'generated', 'image', 'picture', 'photo',
            'style', 'high', 'quality', 'details', 'detail', '4k', '8k', 'hd', 'realistic', 'render',
            'digital', 'art', 'trending', 'artstation', 'concept', 'painting', 'illustration', 'vector',
            'highly', 'detailed', 'intricate', 'sharp', 'focus', 'smooth', 'masterpiece', 'best',
            'ultra', 'resolution'
        }

    def set_search_context(self, searcher, image_data):
        self.searcher = searcher
        self.image_data = image_data

    def preprocess(self):
        if self.loaded: return

        try:
            with open(self.vectors_path, 'r') as f:
                data = json.load(f)
            raw_vectors = data.get("vectors", data)
        except Exception:
            return

        step = 4 

        for uuid_val in self.image_id.mapa_identificadors:
            path_absolut = self.image_id.get_file_from_uuid(uuid_val)
            if not path_absolut: continue
            
            filename_con_ext = os.path.basename(path_absolut)
            filename_sin_ext = os.path.splitext(filename_con_ext)[0]
            
            self.map_name_to_id[filename_sin_ext] = uuid_val
            
            vector_entry = raw_vectors.get(filename_sin_ext)
            if not vector_entry:
                vector_entry = raw_vectors.get(filename_con_ext)

            if vector_entry:
                vec = vector_entry.get("image_embedding") if isinstance(vector_entry, dict) else vector_entry
                
                if vec and len(vec) == 512:
                    small_vec = vec[::step]
                    magnitude = math.sqrt(sum(x*x for x in small_vec))
                    if magnitude > 0:
                        normalized_vec = tuple(x / magnitude for x in small_vec)
                        self.vectors[uuid_val] = normalized_vec
                        self.all_uuids.append(uuid_val)

        self.loaded = True

    def _resolve_id(self, input_id):
        if input_id in self.vectors: return input_id
        if input_id in self.map_name_to_id:
            candidate = self.map_name_to_id[input_id]
            if candidate in self.vectors: return candidate
        return None

    def _get_keywords(self, text):
        if not text: return []
        text = text.lower().replace(',', ' ').replace('.', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ')
        words = text.split()
        return [w for w in words if w not in self.stop_words and len(w) > 3]

    def _get_candidates_by_prompt(self, prompt, limit=200):
        if not self.searcher or not prompt: return []

        keywords = self._get_keywords(prompt)
        if not keywords: return []

        uuid_counts = Counter()
        for word in keywords[:8]:
            matches = self.searcher.prompt(word)
            uuid_counts.update(matches)
            
        if not uuid_counts: return []
        
        most_common = uuid_counts.most_common(limit)
        return [u for u, count in most_common if u in self.vectors]

    def find_similar_images(self, query_uuid, k=10):
        if not self.loaded: self.preprocess()
            
        gallery = Gallery(None, self.image_id)
        if query_uuid not in self.vectors:
            gallery.images = []
            return gallery
            
        q_vec = self.vectors[query_uuid]

        scores = []
        for uid, vec in self.vectors.items():
            if uid == query_uuid: continue
            
            dot = sum(a*b for a, b in zip(q_vec, vec))
            
            if dot > 0.3:
                scores.append((dot, uid))
        
        best = heapq.nlargest(k, scores, key=lambda x: x[0])
        
        gallery.llista = [uid for _, uid in best]
        gallery.images = gallery.llista
        return gallery

    def find_transition_prompts(self, uuid_start, uuid_end):
        if not self.loaded: self.preprocess()
        
        start_id = self._resolve_id(uuid_start)
        end_id = self._resolve_id(uuid_end)
            
        if not start_id or not end_id: return []
            
        target_vector = self.vectors[end_id]
        
        pq = []
        start_sim = sum(a * b for a, b in zip(self.vectors[start_id], target_vector))
        heapq.heappush(pq, (1.0 - start_sim, 0, start_id, [start_id]))
        
        visited = {start_id}
        best_path = []
        min_dist_seen = 2.0
        
        max_steps = 60
        steps = 0
        
        p1 = self.image_data.get_prompt(start_id) or ""
        p2 = self.image_data.get_prompt(end_id) or ""
        combined_prompt = p1 + " " + p2
        
        global_candidates = self._get_candidates_by_prompt(combined_prompt, limit=600)
        candidate_pool = set(global_candidates)
        candidate_pool.add(end_id)
        
        if len(self.all_uuids) > 0:
            random_injection = random.sample(self.all_uuids, min(len(self.all_uuids), 50))
            candidate_pool.update(random_injection)

        pool_list = list(candidate_pool)

        while pq and steps < max_steps:
            estimated_total, cost_so_far, current_uuid, path = heapq.heappop(pq)
            steps += 1
            
            current_vec = self.vectors[current_uuid]
            sim_target = sum(a * b for a, b in zip(current_vec, target_vector))
            dist_to_target = 1.0 - sim_target
            
            if dist_to_target < 0.28 or current_uuid == end_id:
                final_path = path + [end_id] if current_uuid != end_id else path
                return self._uuids_to_prompts(final_path)

            if dist_to_target < min_dist_seen:
                min_dist_seen = dist_to_target
                best_path = path
            
            neighbors = []
            
            sample_size = min(len(pool_list), 250)
            step_candidates = random.sample(pool_list, sample_size)
            if end_id not in step_candidates: step_candidates.append(end_id)

            for cand_uuid in step_candidates:
                if cand_uuid in visited: continue
                
                sim = sum(a * b for a, b in zip(current_vec, self.vectors[cand_uuid]))
                
                if sim > 0.50: 
                    neighbors.append((sim, cand_uuid))
            
            neighbors.sort(key=lambda x: x[0], reverse=True)
            top_neighbors = neighbors[:15] 
            
            for sim, n_uuid in top_neighbors:
                if n_uuid in visited: continue
                visited.add(n_uuid)
                
                dist_local = 1.0 - sim
                new_cost = cost_so_far + dist_local
                
                sim_rem = sum(a * b for a, b in zip(self.vectors[n_uuid], target_vector))
                dist_remaining = 1.0 - sim_rem
                
                priority = new_cost + (dist_remaining * 1.4) + (len(path) * 0.05)
                
                if len(path) < 8: 
                    new_path = list(path)
                    new_path.append(n_uuid)
                    heapq.heappush(pq, (priority, new_cost, n_uuid, new_path))
        
        if best_path:
            return self._uuids_to_prompts(best_path + [end_id])
            
        return self._uuids_to_prompts([start_id, end_id])

    def _uuids_to_prompts(self, uuid_list):
        prompts = []
        clean_uuids = []
        if uuid_list:
            clean_uuids.append(uuid_list[0])
            for i in range(1, len(uuid_list)):
                if uuid_list[i] != uuid_list[i-1]:
                    clean_uuids.append(uuid_list[i])
                    
        for uid in clean_uuids:
            p = self.image_data.get_prompt(uid)
            prompts.append(p if p else "")
        return prompts