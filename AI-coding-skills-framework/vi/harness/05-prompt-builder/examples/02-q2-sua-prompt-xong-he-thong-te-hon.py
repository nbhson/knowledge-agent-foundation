mgr = PromptVersionManager("bot-trogiup")
mgr.create_version("v3", template=tpl, author="lan", changelog="thêm ràng buộc định dạng")
mgr.compare("v2", "v3")      # template_diff + metrics_v1 + metrics_v2
mgr.rollback("v2")           # con trỏ về bản cũ
