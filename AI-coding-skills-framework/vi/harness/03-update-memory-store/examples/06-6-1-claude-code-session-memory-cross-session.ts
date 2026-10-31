/**
 * Claude Code Memory Architecture
 * 
 * 3 tiers of memory:
 * 1. Session Memory (ephemeral) — lives in conversation
 * 2. Project Memory (persistent) — lives in CLAUDE.md files
 * 3. Global Memory (cross-project) — lives in user config
 */
class ClaudeCodeMemoryManager {
  
  // ═══════════════════════════════════════════
  // TIER 1: SESSION MEMORY (ephemeral)
  // Lives only during current conversation
  // ═══════════════════════════════════════════
  private sessionMemory = {
    facts: new Map<string, Fact>(),      // Facts discovered this session
    decisions: [] as Decision[],         // Code decisions made
    corrections: [] as Correction[],    // User corrections
    filesModified: new Set<string>(),   // Files touched this session
    
    addFact(fact: Fact) {
      this.facts.set(fact.id, {
        ...fact,
        sessionId: currentSessionId,
        timestamp: Date.now()
      });
    },
    
    recordDecision(decision: Decision) {
      this.decisions.push({
        ...decision,
        timestamp: Date.now(),
        filesInvolved: this.filesModified
      });
    }
  };

  // ═══════════════════════════════════════════
  // TIER 2: PROJECT MEMORY (persistent)
  // Stored in CLAUDE.md at project root
  // Survives across sessions
  // ═══════════════════════════════════════════
  private projectMemory = {
    // CLAUDE.md format
    conventions: [] as string[],
    architecture: "",
    decisions: [] as Decision[],
    pitfalls: [] as string[],
    
    async loadFromDisk(projectRoot: string) {
      const claudeMd = path.join(projectRoot, 'CLAUDE.md');
      if (fs.existsSync(claudeMd)) {
        const content = fs.readFileSync(claudeMd, 'utf-8');
        this.parseClaudeMd(content);
      }
    },
    
    async saveToDisk(projectRoot: string) {
      const content = this.generateClaudeMd();
      fs.writeFileSync(
        path.join(projectRoot, 'CLAUDE.md'), 
        content, 'utf-8'
      );
    },
    
    generateClaudeMd(): string {
      return `# CLAUDE.md — Project Memory

## Conventions
${this.conventions.map(c => `- ${c}`).join('\n')}

## Architecture
${this.architecture}

## Past Decisions
${this.decisions.map(d => 
  `- [${d.date}] ${d.decision} (reason: ${d.reason})`
).join('\n')}

## Pitfalls
${this.pitfalls.map(p => `- ⚠️ ${p}`).join('\n')}
`;
    },
    
    // Auto-learn from session
    learnFromSession(sessionMemory: any) {
      // Extract conventions from code changes
      const patterns = this.detectPatterns(sessionMemory.filesModified);
      this.conventions.push(...patterns);
      
      // Store important decisions
      for (const decision of sessionMemory.decisions) {
        if (decision.importance === 'high') {
          this.decisions.push(decision);
        }
      }
      
      // Store pitfalls (user corrections)
      for (const correction of sessionMemory.corrections) {
        this.pitfalls.push(
          `${correction.context}: ${correction.correctApproach}`
        );
      }
    }
  };

  // ═══════════════════════════════════════════
  // TIER 3: GLOBAL MEMORY (cross-project)
  // User preferences, skill levels, patterns
  // ═══════════════════════════════════════════
  private globalMemory = {
    preferences: {
      language: 'typescript',
      style: 'functional',
      testFramework: 'vitest',
      linting: 'eslint'
    },
    skillLevels: new Map<string, number>(),  // topic -> proficiency
    commonPatterns: [] as Pattern[],
    
    updateSkillLevel(topic: string, interaction: UserInteraction) {
      const current = this.skillLevels.get(topic) || 0;
      
      // Simple EMA-based skill tracking
      if (interaction.success) {
        this.skillLevels.set(topic, Math.min(1.0, current + 0.1));
      } else {
        this.skillLevels.set(topic, Math.max(0, current - 0.05));
      }
      
      // Adjust detail level based on skill
      return {
        topic,
        skillLevel: this.skillLevels.get(topic),
        detailLevel: this.skillLevels.get(topic)! > 0.7 ? 'brief' : 'detailed'
      };
    }
  };

  // ═══════════════════════════════════════════
  // MEMORY CONSOLIDATION — Session → Project
  // ═══════════════════════════════════════════
  async consolidateAfterSession() {
    // 1. Extract learnings from session
    const learnings = this.extractSessionLearnings();
    
    // 2. Update project memory (CLAUDE.md)
    if (learnings.hasNewConventions) {
      await this.projectMemory.saveToDisk(projectRoot);
    }
    
    // 3. Update global memory
    for (const correction of this.sessionMemory.corrections) {
      this.globalMemory.updateSkillLevel(
        correction.topic, 
        { success: false }
      );
    }
    
    // 4. Clear session memory
    this.sessionMemory = this.createFreshSessionMemory();
    
    return {
      savedConventions: learnings.conventions.length,
      savedDecisions: learnings.decisions.length,
      savedPitfalls: learnings.pitfalls.length
    };
  }
}
