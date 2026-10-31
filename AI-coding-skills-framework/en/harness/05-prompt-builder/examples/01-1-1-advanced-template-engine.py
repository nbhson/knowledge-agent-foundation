from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import re
import json
import hashlib

@dataclass
class PromptTemplate:
    """
    Production-grade prompt template with:
    - Variable validation
    - Conditional sections
    - Loops for dynamic content
    - Versioning
    - Metadata tracking
    """
    name: str
    template: str
    variables: List[str] = field(default_factory=list)
    required_variables: List[str] = field(default_factory=list)
    optional_variables: List[str] = field(default_factory=list)
    default_values: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""
    
    def render(self, **kwargs) -> str:
        """
        Render template with variables.
        Supports: {var}, {{#if var}}...{{/if}}, {{#each var}}...{{/each}}
        """
        result = self.template
        
        # Apply defaults
        context = {**self.default_values, **kwargs}
        
        # Validate required variables
        missing = [v for v in self.required_variables if v not in context]
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
        
        # Process conditional blocks: {{#if var}}...{{/if}}
        result = self._process_conditionals(result, context)
        
        # Process loop blocks: {{#each items}}...{{/each}}
        result = self._process_loops(result, context)
        
        # Process simple variables: {var}
        for key, value in context.items():
            result = result.replace(f"{{{key}}}", str(value))
        
        return result
    
    def _process_conditionals(self, template: str, context: Dict) -> str:
        """Process {{#if var}}...{{/if}} blocks"""
        pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
        
        def replace_conditional(match):
            var_name = match.group(1)
            content = match.group(2)
            if var_name in context and context[var_name]:
                return content
            return ""
        
        return re.sub(pattern, replace_conditional, template)
    
    def _process_loops(self, template: str, context: Dict) -> str:
        """Process {{#each items}}...{{/each}} blocks"""
        pattern = r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}'
        
        def replace_loop(match):
            var_name = match.group(1)
            content = match.group(2)
            items = context.get(var_name, [])
            
            if not isinstance(items, list):
                return str(items)
            
            result_parts = []
            for i, item in enumerate(items):
                item_str = content
                if isinstance(item, dict):
                    for k, v in item.items():
                        item_str = item_str.replace(f"{{{{{k}}}}}", str(v))
                else:
                    item_str = item_str.replace("{item}", str(item))
                item_str = item_str.replace("{index}", str(i + 1))
                result_parts.append(item_str)
            
            return "\n".join(result_parts)
        
        return re.sub(pattern, replace_loop, template)
    
    def validate(self, **kwargs) -> Dict:
        """Validate all variables are provided"""
        all_vars = set(self.required_variables)
        missing = [v for v in all_vars if v not in kwargs]
        extra = [v for v in kwargs if v not in self.variables and v not in self.default_values]
        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "extra": extra,
            "coverage": f"{len(kwargs) - len(extra)}/{len(all_vars)}",
        }
    
    def fingerprint(self) -> str:
        """Generate unique hash for this template version"""
        content = f"{self.name}:{self.template}:{self.version}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "template": self.template,
            "variables": self.variables,
            "required_variables": self.required_variables,
            "version": self.version,
            "fingerprint": self.fingerprint(),
        }
