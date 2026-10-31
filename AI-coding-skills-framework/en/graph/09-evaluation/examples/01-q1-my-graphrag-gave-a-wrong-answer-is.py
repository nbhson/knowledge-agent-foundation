gq = 1 - isolated_rate - invalid_rate   # graph
rm = retrieval["MRR"]                    # retrieval
gm = generation["faithfulness"]          # generation
overall = mean([s for s in (gq, rm, gm) if s > 0])
