# python 03-update-memory-store/lab_consolidation.py

from knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()
kg.add_triplet("BHYT", "mức đóng", "4.5%")
kg.add_triplet("BHYT", "mức đóng", "4.5% lương cơ sở")  # Duplicate
kg.add_triplet("BHYT", "mức đóng", "5%")  # Updated

consolidator = MemoryConsolidator(kg)
report = consolidator.generate_memory_report()
print(report)

conflicts = consolidator.conflict_resolution()
print(f"Conflicts: {len(conflicts)}")
for c in conflicts:
    print(f"  {c['subject']} → {c['conflicting_values']}")
