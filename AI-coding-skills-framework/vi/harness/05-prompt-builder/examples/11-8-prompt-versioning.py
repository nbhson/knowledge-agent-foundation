from dataclasses import dataclass, field
from typing import Optional
import json

@dataclass
class PromptVersion:
    version: str
    template: str
    created_at: str
    author: str
    changelog: str
    metrics: Dict = field(default_factory=dict)
    is_active: bool = True
    tags: List[str] = field(default_factory=list)

class PromptVersionManager:
    """
    Version control for prompt templates
    
    Features:
    - Track all versions
    - Compare versions
    - Rollback
    - A/B testing support
    - Metrics per version
    """
    
    def __init__(self, prompt_name: str):
        self.prompt_name = prompt_name
        self.versions: List[PromptVersion] = []
        self.active_version: Optional[str] = None
    
    def create_version(
        self, 
        version: str, 
        template: str, 
        author: str = "system",
        changelog: str = "",
        tags: List[str] = None,
    ) -> PromptVersion:
        """Create a new version"""
        new_version = PromptVersion(
            version=version,
            template=template,
            created_at=datetime.now().isoformat(),
            author=author,
            changelog=changelog,
            tags=tags or [],
        )
        self.versions.append(new_version)
        self.active_version = version
        return new_version
    
    def get_active(self) -> Optional[PromptVersion]:
        """Get currently active version"""
        for v in self.versions:
            if v.version == self.active_version:
                return v
        return None
    
    def rollback(self, version: str) -> bool:
        """Rollback to a previous version"""
        for v in self.versions:
            if v.version == version:
                self.active_version = version
                return True
        return False
    
    def compare(self, v1: str, v2: str) -> Dict:
        """Compare two versions"""
        ver1 = next((v for v in self.versions if v.version == v1), None)
        ver2 = next((v for v in self.versions if v.version == v2), None)
        
        if not ver1 or not ver2:
            return {"error": "Version not found"}
        
        return {
            "version_1": ver1.version,
            "version_2": ver2.version,
            "template_diff": self._diff(ver1.template, ver2.template),
            "metrics_v1": ver1.metrics,
            "metrics_v2": ver2.metrics,
            "created_v1": ver1.created_at,
            "created_v2": ver2.created_at,
        }
    
    def _diff(self, text1: str, text2: str) -> Dict:
        """Simple text diff"""
        lines1 = text1.split('\n')
        lines2 = text2.split('\n')
        
        added = [l for l in lines2 if l not in lines1]
        removed = [l for l in lines1 if l not in lines2]
        
        return {
            "added_lines": len(added),
            "removed_lines": len(removed),
            "added": added[:5],
            "removed": removed[:5],
        }
    
    def update_metrics(self, version: str, metrics: Dict):
        """Update metrics for a version"""
        for v in self.versions:
            if v.version == version:
                v.metrics.update(metrics)
                return True
        return False
    
    def list_versions(self) -> List[Dict]:
        """List all versions"""
        return [
            {
                "version": v.version,
                "created_at": v.created_at,
                "author": v.author,
                "changelog": v.changelog,
                "is_active": v.version == self.active_version,
                "metrics": v.metrics,
            }
            for v in self.versions
        ]
