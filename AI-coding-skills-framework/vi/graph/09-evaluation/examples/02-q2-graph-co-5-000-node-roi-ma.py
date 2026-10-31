metrics = evaluate_graph_quality(G_labeled)
# {'nodes':34,'edges':78,'density':0.139,'avg_degree':4.59,
#  'connectivity':1.0,'isolated_rate':0.0}
evaluate_coverage(["Alice","Bob","Phoenix","Alice Nguyen"],
                  ["Alice","Bob","Phoenix","Atlas"])
# precision 0.75, recall 0.75, missed:['atlas'], hallucinated:['alice nguyen']
