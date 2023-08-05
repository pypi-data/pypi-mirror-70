from hnet.hnet import hnet

from hnet.hnet import (
    enrichment,
    compare_networks,
    to_undirected,
    import_example,
    )

from hnet.utils.adjmat_vec import (
    vec2adjmat,
    adjmat2vec,
    )

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '1.0.8'

# module level doc-string
__doc__ = """
HNET - Graphical Hypergeometric networks.
=====================================================================

Description
-----------
Creation of networks from datasets with mixed datatypes and with unknown function.
Input datasets can range from generic dataframes to nested data structures with lists, missing values and enumerations.
HNet (graphical Hypergeometric Networks) is a method where associations across variables are tested for significance by statistical inference.
The aim is to determine a network with significant associations that can shed light on the complex relationships across variables.

Examples
-------
Initialize hnet with default settings
>>> from hnet import hnet
>>> hn = hnet()
>>> # Load example dataset
>>> df = hnet.import_example('sprinkler')

Structure learning
>>> out = hn.association_learning(df)

Plot results:
>>> # Plot dynamic graph
>>> G_dynamic = hn.d3graph()
>>> # Plot static graph
>>> G_static = hn.plot()
>>> # Plot heatmap
>>> P_heatmap = hn.heatmap(cluster=True)

Examine differences between models
>>> import hnet as hnet
>>> [scores, adjmat] = hnet.compare_networks(out['simmatP'], out['simmatP'], showfig=True)
>>> adjmat_undirected = hnet.to_undirected(out['simmatLogP'])

References
----------
* https://erdogant.github.io/hnet/
* https://github.com/erdogant/hnet

"""
