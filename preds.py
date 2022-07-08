import numpy as np
import pandas as pd
from scipy import sparse

def compute_cone_precedence(df_blocks, 
                            angle, 
                            is_equality_in_precedence=False,
                            show_progress_bar=True):
    """ Compute the cone precedence matrix (a cone includes the block at its tip by convention).
    
    Arguments:
    ----------
    df_blocks: pandas DataFrame with the coordinates of each block under the columns "X", "Y", "Z".
    
    angle: 0 < float < 90
        Max slope angle of the pit. The angle is with respect to the horizontal plane.

    is_equality_in_precedence: bool (default: False)
        If True, the convention is that if the angle between two blocks *exactly equals* the one given as input, 
        then the upper block is considered in the predecence.
        
    Returns:
    --------
    LIL sparse matrix
    """
    
    n_blocks = len(df_blocks.index)
    map_X_to_i = {X: i for i, X in enumerate(sorted(set(df_blocks["X"])))}
    sorted_blocks = df_blocks.sort_values(by=['X', 'Y', 'Z'], ascending=True)
    max_length = (max(df_blocks.Z) - min(df_blocks.Z)) / np.tan(np.radians(angle)) # @ZL this is the maximum horizontal distance based on the from a block to the surface given the slope angle
    
    # initialize sparse matrix (format is Lil because it's the most efficient to change the matrix sparsity)
    cone_precedence_matrix = sparse.lil_matrix((n_blocks, n_blocks), dtype='bool')
    
    x, y = None, None
    for i, b in enumerate(sorted_blocks.index):
            
        if df_blocks.X[b] != x:
            change_box = True
            x = df_blocks.X[b]
            blocks_within_x = np.abs(df_blocks.X - x) <= max_length
            
        if df_blocks.Y[b] != y:
            change_box = True
            y = df_blocks.Y[b]
            blocks_within_y = np.abs(df_blocks.Y - y) <= max_length
            
        if change_box:
            blocks_in_box = df_blocks.loc[blocks_within_x & blocks_within_y]
            change_box = False
         
        z = df_blocks.Z[b]
        blocks_in_box = blocks_in_box.loc[blocks_in_box.Z - z >= 0]
        if is_equality_in_precedence:
            is_in_cone = np.sqrt((blocks_in_box.X - x)**2 + (blocks_in_box.Y - y)**2) \
                                    <= (blocks_in_box.Z - z) / np.tan(np.radians(angle))
        else:
            is_in_cone = np.sqrt((blocks_in_box.X - x)**2 + (blocks_in_box.Y - y)**2) \
                                    < (blocks_in_box.Z - z) / np.tan(np.radians(angle))  
        
        blocks_in_cone = blocks_in_box.index[is_in_cone].to_numpy()
        cone_precedence_matrix[b, blocks_in_cone] = True
    
    return cone_precedence_matrix


def compute_cone_successors(df_blocks, 
                            angle, 
                            is_equality_in_precedence=False,
                            show_progress_bar=True):
    """ Compute the cone successors matrix (a successor cone includes the block at its tip by convention).
    
    Arguments:
    ----------
    df_blocks: pandas DataFrame with the coordinates of each block under the columns "X", "Y", "Z".
    
    angle: 0 < float < 90
        Max slope angle of the pit. The angle is with respect to the horizontal plane.

    is_equality_in_precedence: bool (default: False)
        If True, the convention is that if the angle between two blocks *exactly equals* the one given as input, 
        then the upper block is considered in the predecence.
        
    Returns:
    --------
    LIL sparse matrix
    """
    
    n_blocks = len(df_blocks.index)
    map_X_to_i = {X: i for i, X in enumerate(sorted(set(df_blocks["X"])))}
    sorted_blocks = df_blocks.sort_values(by=['X', 'Y', 'Z'], ascending=False)
    max_length = (max(df_blocks.Z) - min(df_blocks.Z)) / np.tan(np.radians(angle)) # @ZL this is the maximum horizontal distance based on the from a block to the surface given the slope angle
    
    # initialize sparse matrix (format is Lil because it's the most efficient to change the matrix sparsity)
    cone_successor_matrix = sparse.lil_matrix((n_blocks, n_blocks), dtype='bool')
    
    x, y = None, None
    for i, b in enumerate(sorted_blocks.index):
        if df_blocks.X[b] != x:
            change_box = True
            x = df_blocks.X[b]
            blocks_within_x = np.abs(df_blocks.X - x) <= max_length
            
        if df_blocks.Y[b] != y:
            change_box = True
            y = df_blocks.Y[b]
            blocks_within_y = np.abs(df_blocks.Y - y) <= max_length
            
        if change_box:
            blocks_in_box = df_blocks.loc[blocks_within_x & blocks_within_y]
            change_box = False
         
        z = df_blocks.Z[b]
        blocks_in_box = blocks_in_box.loc[blocks_in_box.Z <= z]
        if is_equality_in_precedence:
            is_in_cone = np.sqrt((blocks_in_box.X - x)**2 + (blocks_in_box.Y - y)**2) \
                                    <= (z - blocks_in_box.Z) / np.tan(np.radians(angle))
        else:
            is_in_cone = np.sqrt((blocks_in_box.X - x)**2 + (blocks_in_box.Y - y)**2) \
                                    < (z - blocks_in_box.Z) / np.tan(np.radians(angle))  
        
        
        blocks_in_cone = blocks_in_box.index[is_in_cone].to_numpy()
        #blocks_in_cone = blocks_in_box.index.to_numpy() #### REMOVE
        cone_successor_matrix[b, blocks_in_cone] = True
    return cone_successor_matrix
