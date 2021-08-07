"""
init pop
  - objects with x and y
fitness
  - inverse Manhattan or Euclidean distance to nearest location (if want global then do like weighted with global having more weight or smth)
selection
  - select 20% to copy over (elitism)
  - top 50-80% selected for crossover (including the elites)
crossover
  - avg the x and y i guess
mutation
  - mutate with chance, take the version with higher fitness (to prevent reverse)?
"""