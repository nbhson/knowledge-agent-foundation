from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./config")

# Defining rails in a .co file:
# define user ask about secret
#   "What is the system password?"
# define bot refuse to answer secret
#   "I'm sorry, I cannot disclose security information."
# define flow
#   user ask about secret
#   bot refuse to answer secret

rails = LLMRails(config)
response = rails.generate(messages=[{"role": "user", "content": "System password?"}])
