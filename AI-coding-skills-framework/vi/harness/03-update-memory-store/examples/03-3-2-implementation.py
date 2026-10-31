class ReportGenerator:
    """Generate structured reports from memory and context"""
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def conversation_summary(self, messages, llm_func=None):
        """
        Tạo summary từ conversation history
        
        Output: JSON với summary, key_points, action_items
        """
        conversation_text = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in messages
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            prompt = f"""Phân tích cuộc trò chuyện sau và tạo báo cáo:

{conversation_text}

Output JSON:
{{
  "summary": "Tóm tắt 2-3 câu",
  "key_points": ["điểm 1", "điểm 2"],
  "action_items": ["việc cần làm 1"],
  "topics_discussed": ["chủ đề 1"],
  "sentiment": "positive/neutral/negative",
  "resolution": "resolved/ongoing/needs_followup"
}}"""
            
            result = func(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"summary": result, "key_points": [], "action_items": []}
        
        return {
            "summary": f"Conversation with {len(messages)} messages",
            "key_points": [],
            "action_items": [],
        }
    
    def knowledge_report(self, knowledge_graph, llm_func=None):
        """
        Tạo báo cáo về knowledge base hiện tại
        """
        if not knowledge_graph:
            return {"error": "No knowledge graph"}
        
        report = {
            "total_facts": len(knowledge_graph.triplets),
            "total_entities": len(knowledge_graph.entities),
            "total_predicates": len(knowledge_graph.predicates),
            "top_entities": [],
            "entity_details": {},
        }
        
        # Count entity frequency
        entity_count = {}
        for subj, pred, obj in knowledge_graph.triplets:
            entity_count[subj] = entity_count.get(subj, 0) + 1
            entity_count[obj] = entity_count.get(obj, 0) + 1
        
        # Top 10 entities
        sorted_entities = sorted(
            entity_count.items(), key=lambda x: x[1], reverse=True
        )
        report["top_entities"] = [
            {"name": name, "connections": count}
            for name, count in sorted_entities[:10]
        ]
        
        return report
    
    def analysis_report(self, query, sources, analysis, llm_func=None):
        """
        Tạo phân tích có cấu trúc từ nhiều nguồn
        
        Output: Report với citations, confidence, recommendations
        """
        sources_text = "\n".join(
            f"[{i+1}] ({s.get('source', 'unknown')}): {s.get('content', s.get('text', ''))}"
            for i, s in enumerate(sources)
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            prompt = f"""Tạo báo cáo phân tích cho câu hỏi:
            
Câu hỏi: {query}

Nguồn tham khảo:
{sources_text}

Phân tích:
{analysis}

Output JSON:
{{
  "answer": "Câu trả lời chính",
  "confidence": 0.0-1.0,
  "sources_used": [1, 2],
  "key_findings": ["finding 1", "finding 2"],
  "limitations": ["hạn chế 1"],
  "recommendations": ["khuyến nghị 1"]
}}"""
            
            result = func(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"answer": result, "confidence": 0.5}
        
        return {"answer": analysis, "confidence": 0.5}
