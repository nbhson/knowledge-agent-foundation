class KnowledgeGraph:
    """Simple in-memory knowledge graph"""
    
    def __init__(self):
        self.triplets = []
        self.entities = set()
        self.predicates = set()
    
    def add_triplet(self, subject, predicate, obj):
        self.triplets.append((subject, predicate, obj))
        self.entities.add(subject)
        self.entities.add(obj)
        self.predicates.add(predicate)
    
    def add_from_text(self, text, llm_func):
        """
        Extract triplets from text using LLM
        
        Input: "gemma3:12b là model LLM 12B chạy trên Ollama"
        Output: [("gemma3:12b", "is_a", "LLM"),
                 ("gemma3:12b", "has_size", "12B"),
                 ("gemma3:12b", "runs_on", "Ollama")]
        """
        prompt = f"""Extract entity-relationship triplets from the following text.
Format: (subject, predicate, object)

Text: {text}

Triplets:"""
        
        response = llm_func(prompt)
        
        # Parse triplets
        import re
        triplet_pattern = r'\(([^,]+),\s*([^,]+),\s*([^)]+)\)'
        matches = re.findall(triplet_pattern, response)
        
        for subject, predicate, obj in matches:
            self.add_triplet(
                subject.strip(), 
                predicate.strip(), 
                obj.strip()
            )
        
        return matches
    
    def query_entity(self, entity, max_hops=2):
        """Find all triplets related to an entity (up to max_hops)"""
        results = []
        visited = set()
        queue = [(entity, 0)]
        
        while queue:
            current, depth = queue.pop(0)
            if depth > max_hops or current in visited:
                continue
            
            visited.add(current)
            
            for subj, pred, obj in self.triplets:
                if subj == current:
                    results.append((subj, pred, obj, depth))
                    if depth < max_hops:
                        queue.append((obj, depth + 1))
                elif obj == current:
                    results.append((obj, pred, subj, depth))
                    if depth < max_hops:
                        queue.append((subj, depth + 1))
        
        return results
    
    def find_path(self, start, end, max_depth=5):
        """Find shortest path between two entities"""
        from collections import deque
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == end:
                return path
            
            if len(path) > max_depth:
                continue
            
            for subj, pred, obj in self.triplets:
                next_entity = None
                edge = None
                
                if subj == current:
                    next_entity = obj
                    edge = f"--{pred}-->"
                elif obj == current:
                    next_entity = subj
                    edge = f"<--{pred}--"
                
                if next_entity and next_entity not in visited:
                    visited.add(next_entity)
                    queue.append((next_entity, path + [edge, next_entity]))
        
        return None  # No path found
    
    def community_detection(self):
        """
        Detect communities (nhóm entities liên quan)
        
        Simple approach: Connected components
        """
        visited = set()
        communities = []
        
        for entity in self.entities:
            if entity not in visited:
                community = []
                queue = [entity]
                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue
                    visited.add(current)
                    community.append(current)
                    
                    for subj, pred, obj in self.triplets:
                        if subj == current and obj not in visited:
                            queue.append(obj)
                        elif obj == current and subj not in visited:
                            queue.append(subj)
                
                communities.append(community)
        
        return communities
    
    def summarize_community(self, community, llm_func):
        """Generate summary for a community of entities"""
        # Gather all facts about entities in community
        facts = []
        for entity in community:
            for subj, pred, obj in self.triplets:
                if subj == entity or obj == entity:
                    facts.append(f"{subj} {pred} {obj}")
        
        prompt = f"""Tóm tắt các thông tin sau về một nhóm entities liên quan:

{chr(10).join(facts)}

Tóm tắt:"""
        
        return llm_func(prompt)
