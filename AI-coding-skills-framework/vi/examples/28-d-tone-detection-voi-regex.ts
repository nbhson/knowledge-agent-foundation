class ClaudeToneDetector {
  // Phát hiện sự ức chế/không hài lòng của user
  frustrationPatterns = [
    /why (is|are) (you|this)/i,
    /stop doing/i,
    /i (told|said) you/i,
    /for the (\d+)(st|nd|rd|th) time/i,
    /just do it/i,
    /seriously\?/i
  ];
  
  detectFrustration(message: string): boolean {
    return this.frustrationPatterns.some(p => p.test(message));
  }
  
  adjustTone(message: string): ToneAdjustment {
    if (this.detectFrustration(message)) {
      return {
        tone: 'apologetic',
        verbosity: 'concise',
        explanation: 'minimal',
        action: 'immediate' // Làm ngay, giải thích sau
      };
    }
    
    return {
      tone: 'helpful',
      verbosity: 'balanced',
      explanation: 'detailed',
      action: 'thoughtful'
    };
  }
}
