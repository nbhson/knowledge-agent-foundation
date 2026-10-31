vm.create_version("1.0.0", tpl_v1, author="ngan", changelog="original")
vm.create_version("2.0.0", tpl_v2, author="ngan", changelog="shorter rules")
test.add_variant("control", tpl_v1, traffic_pct=50)
test.add_variant("variant_a", tpl_v2, traffic_pct=50)
print(test.analyze()["improvement_pct"])
vm.rollback("1.0.0")   # 30 seconds, nothing lost
