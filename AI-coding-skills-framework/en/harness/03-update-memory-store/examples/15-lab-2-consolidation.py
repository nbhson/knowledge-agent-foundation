# python 03-update-memory-store/lab_consolidation.py

from knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()
kg.add_triplet("health insurance", "contribution rate", "4.5%")
kg.add_triplet("health insurance", "contribution rate", "4.5% of base salary")  # Duplicate
kg.add_triplet("health insurance", "contribution rate", "5%")  # Updated

consolidator = MemoryConsolidator(kg)
report = consolidator.generate_memory_report()
print(report)

conflicts = consolidator.conflict_resolution()
print(f"Conflicts: {len(conflicts)}")
for c in conflicts:
    print(f"  {c['subject']} → {c['conflicting_values']}")
