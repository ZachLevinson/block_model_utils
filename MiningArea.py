from time import time


class MiningArea:
    """
    Build out mining areas - these are rectangular grids from the origin s.t.
    
    ====================↑
    | x - x - x - x - x | 
    | x - x - x - x - x |
    | x - x - b - x - x | width_y
    | x - x - x - x - x |
    | x - x - x - x - x |
    ====================↓   
    ←----- width_x ----→
    
    where b is the origin and the x's denote blocks in a mining area

    Arguments:
    ----------
    m (str): mine name
    blocks (pd.Dataframe): columns = ['X', 'Y', 'Z'] with the blocks of mine m
    mining_width_x (float): mininmum mininng width in x direction
    mining_width_y (float): mininmum mining width in y direction
    """
    def __init__(self, m, blocks, mining_width_x, mining_width_y):
        self.mine = m
        self.mining_width_x = mining_width_x/2
        self.mining_width_y = mining_width_y/2
        self.map_b_to_blocks_in_area = {}
        self.initialize_map_b_to_blocks_in_area(blocks)
    
    def initialize_map_b_to_blocks_in_area(self, blocks):
        start = time()
        for b in blocks.index:
            x, y, z = blocks.iloc[b]

            mask = (blocks.X >= x - self.mining_width_x) \
                & (blocks.X <= x + self.mining_width_x) \
                & (blocks.Y >= y - self.mining_width_y) \
                & (blocks.Y <= y + self.mining_width_y) \
                & (blocks.Z == z)
                
            self.map_b_to_blocks_in_area[b] = blocks.loc[mask].index.to_numpy()
       
        print(f'Initializing map of blocks in mining areas at {self.mine} ({time()-start} s)')

