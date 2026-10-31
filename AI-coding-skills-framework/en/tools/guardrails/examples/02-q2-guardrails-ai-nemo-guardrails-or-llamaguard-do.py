from nemoguardrails import RailsConfig, LLMRails
rails = LLMRails(RailsConfig.from_path("./config"))
rails.generate(messages=[{"role":"user","content":"System password?"}])
