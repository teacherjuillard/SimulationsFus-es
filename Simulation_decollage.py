# Simulation d'un decollage de fusee vers Jupiter
# auteur : Paul Juillard 2024
from fusee import *

### Réservoirs

# Rayon des réservoirs en mètres
# solution à effacer
# rayon = 7.7
rayon = ____

reservoir_gauche = Reservoir(rayon, "gauche")
reservoir_droit  = Reservoir(rayon, "droit")

# quantité totale de carburant (en kg)
# solution à effacer
# carburant_total = 560
carburant_total = ___

reservoir_gauche.remplir(carburant_total/2)
reservoir_droit.remplir(carburant_total/2)

### Fusée
ma_fusee = Fusee(reservoir_gauche, reservoir_droit)

### On lance la simulation
simulation(carburant_total, rayon, ma_fusee, reservoir_gauche, reservoir_droit)