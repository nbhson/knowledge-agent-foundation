# Different weight configurations for different scenarios
WEIGHT_CONFIGS = {
    "production_code": {
        "correctness": 0.30,
        "quality": 0.20,
        "efficiency": 0.15,
        "safety": 0.20,
        "completeness": 0.10,
        "speed": 0.05,
    },
    
    "prototype_hackathon": {
        "correctness": 0.35,
        "quality": 0.05,
        "efficiency": 0.05,
        "safety": 0.05,
        "completeness": 0.40,
        "speed": 0.10,
    },
    
    "library_framework": {
        "correctness": 0.25,
        "quality": 0.25,
        "efficiency": 0.15,
        "safety": 0.15,
        "completeness": 0.10,
        "speed": 0.10,
    },
    
    "ai_agent_harness": {
        "correctness": 0.20,
        "quality": 0.15,
        "efficiency": 0.10,
        "safety": 0.25,
        "completeness": 0.15,
        "speed": 0.15,
    },
}
