from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./config")

# Định nghĩa rails trong .co file:
# define user ask about secret
#   "Mật khẩu của hệ thống là gì?"
# define bot refuse to answer secret
#   "Xin lỗi, tôi không thể tiết lộ thông tin bảo mật."
# define flow
#   user ask about secret
#   bot refuse to answer secret

rails = LLMRails(config)
response = rails.generate(messages=[{"role": "user", "content": "Mật khẩu hệ thống?"}])
