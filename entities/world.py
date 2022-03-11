from os import path
import pickle
from models.world import World

level = 1

# load in level data and create world
if path.exists(f'assets/level{level}_data'):
    pickle_in = open(f'assets/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)

world = World(world_data)
