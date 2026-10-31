for successor in list(self.graph.successors(dup_name)):
    edata = self.graph.get_edge_data(dup_name, successor)
    self.graph.add_edge(canonical_name, successor, **edata)
self.graph.remove_node(dup_name)
