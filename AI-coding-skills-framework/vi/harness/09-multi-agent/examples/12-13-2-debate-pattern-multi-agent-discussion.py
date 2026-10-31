class DebateProtocol:
    """
    Debate pattern — nhiều agents debate để reach consensus.
    
    Mỗi agent đưa ra quan điểm riêng,
    sau đó các agents phản biện lẫn nhau,
    cuối cùng 1 judge agent quyết định.
    
    Sử dụng khi:
    - Cần design decision quan trọng
    - Không có clear best approach
    - Cần diverse perspectives
    """
    
    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds
        self.debate_history: List[Dict] = []
        self.positions: Dict[str, str] = {}
    
    def conduct_debate(self, topic: str, 
                       agents: List[Dict],
                       judge: Dict) -> Dict:
        """
        Conduct debate về 1 topic.
        
        agents: [{"id": str, "position": str, "arguments": [str]}]
        judge: {"id": str, "criteria": [str]}
        """
        # Round 1: Opening statements
        for agent in agents:
            self.positions[agent["id"]] = agent["position"]
            self.debate_history.append({
                "round": 1,
                "agent": agent["id"],
                "type": "opening",
                "content": agent["position"],
                "arguments": agent.get("arguments", []),
            })
        
        # Round 2: Rebuttals
        for i, agent in enumerate(agents):
            other_agents = [a for a in agents if a["id"] != agent["id"]]
            rebuttal_targets = [a["id"] for a in other_agents]
            
            self.debate_history.append({
                "round": 2,
                "agent": agent["id"],
                "type": "rebuttal",
                "targets": rebuttal_targets,
                "content": f"Rebutting arguments from {rebuttal_targets}",
            })
        
        # Round 3: Closing
        for agent in agents:
            self.debate_history.append({
                "round": 3,
                "agent": agent["id"],
                "type": "closing",
                "content": f"Final position: {agent['position']}",
            })
        
        # Judge decision
        decision = self._judge_decision(judge, agents)
        
        return {
            "topic": topic,
            "rounds": 3,
            "positions": self.positions,
            "winner": decision["winner"],
            "reasoning": decision["reasoning"],
            "full_debate": self.debate_history,
        }
    
    def _judge_decision(self, judge: Dict, 
                        agents: List[Dict]) -> Dict:
        """Judge quyết định winner dựa trên criteria"""
        # Simplified scoring
        scores = {}
        for agent in agents:
            score = 0
            # Count arguments as proxy for depth
            history_entries = [
                h for h in self.debate_history 
                if h["agent"] == agent["id"]
            ]
            for entry in history_entries:
                score += len(entry.get("arguments", []))
                score += len(entry.get("content", "")) / 100
            
            scores[agent["id"]] = score
        
        winner_id = max(scores, key=scores.get)
        
        return {
            "winner": winner_id,
            "scores": scores,
            "reasoning": f"Agent {winner_id} presented the most "
                        f"compelling case with strongest arguments.",
        }
