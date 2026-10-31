class ToolDecisionPipeline:
    """
    Complete pipeline: Query → Intent → Tool Selection → Execution → Response
    
    Features:
    - Multi-strategy classification
    - Parameter extraction
    - Guardrails integration
    - Fallback handling
    - Performance tracking
    """
    
    def __init__(self, registry: ToolRegistry, llm_func=None):
        self.registry = registry
        self.classifier = IntentClassifier(llm_func)
        self.executor = ToolExecutor(registry)
        self.llm = llm_func
    
    def process(self, query: str, user_id: str = None, 
                context: Dict = None) -> Dict:
        """Full pipeline"""
        
        # Step 1: Classify intent
        intent = self.classifier.classify(query)
        
        selected_tools = intent.get("tools", [])
        
        if not selected_tools:
            return {
                "tool_used": None,
                "result": "No tool needed — direct response",
                "intent": intent,
                "pipeline_steps": ["classify"],
            }
        
        # Step 2: Try each potential tool
        for tool_name in selected_tools:
            tool = self.registry.get_tool(tool_name)
            if not tool:
                continue
            
            # Step 3: Extract parameters
            params = self._extract_params(query, tool, context)
            
            # Step 4: Execute
            result = self.executor.execute(
                tool_name, params, user_id=user_id
            )
            
            if result["success"]:
                return {
                    "tool_used": tool_name,
                    "result": result["result"],
                    "intent": intent,
                    "params": params,
                    "pipeline_steps": ["classify", "select", "extract", "execute"],
                    "elapsed_ms": result.get("elapsed_ms"),
                }
        
        return {
            "tool_used": None,
            "result": "No tool could process this query",
            "intent": intent,
            "pipeline_steps": ["classify", "select", "execute_failed"],
        }
    
    def process_multi(self, query: str) -> Dict:
        """
        Process query that may require multiple tools
        """
        # Detect multi-intent
        intents = self.classifier.classify_multi_intent(query)
        
        results = []
        for intent in intents:
            for tool_name in intent.get("tools", []):
                tool = self.registry.get_tool(tool_name)
                if not tool:
                    continue
                
                params = self._extract_params(query, tool)
                result = self.executor.execute(tool_name, params)
                
                if result["success"]:
                    results.append({
                        "tool": tool_name,
                        "result": result["result"],
                        "params": params,
                    })
                    break  # Move to next intent
        
        return {
            "tools_used": [r["tool"] for r in results],
            "results": results,
            "total_intents": len(intents),
            "total_success": len(results),
        }
    
    def _extract_params(self, query: str, tool: ToolDefinition, 
                        context: Dict = None) -> Dict:
        """Extract tool parameters from query"""
        if self.llm:
            params_desc = json.dumps(tool.parameters, indent=2, ensure_ascii=False)
            context_text = json.dumps(context, indent=2, ensure_ascii=False) if context else "None"
            
            prompt = f"""Trích xuất parameters cho tool từ query.

Query: "{query}"
Context: {context_text}
Tool: {tool.name}
Description: {tool.description}
Parameters schema: {params_desc}

Output JSON (chỉ parameters, đúng types):"""
            
            response = self.llm(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        # Fallback: put query as first string param
        first_param = list(tool.parameters.keys())[0] if tool.parameters else None
        if first_param:
            return {first_param: query}
        return {}
