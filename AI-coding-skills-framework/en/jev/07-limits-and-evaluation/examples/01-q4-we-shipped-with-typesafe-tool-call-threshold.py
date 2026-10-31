for tau in [0.5, 0.6, 0.7, 0.8, 0.9]:
    auto = [(p, ok) for p, ok in gate if p >= tau]
    print(tau, len(auto)/len(gate),                      # coverage
          sum(ok for _, ok in auto)/len(auto))          # accuracy when acting
