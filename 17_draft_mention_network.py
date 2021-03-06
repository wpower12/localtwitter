import pandas as pd
import networkx as nx

import localtwitter

EDGES_FN = "data/full_mention_edges.csv"
edges_df = pd.read_csv(EDGES_FN)

USER_FIPS_FN = "data/users_with_fips_2022_02_28.csv"
user_fips = localtwitter.read_csv_to_dict(USER_FIPS_FN)

# source_user,mentioned_user,weight
g = nx.from_pandas_edgelist(edges_df, 
	source='source_user', 
	target='mentioned_user',
	edge_attr=True,
	create_using=nx.DiGraph)

nx.set_node_attributes(g, user_fips)

print(g)

largest_s_cc = max(nx.strongly_connected_components(g), key=len)
largest_w_cc = max(nx.weakly_connected_components(g), key=len)

print("|SCGC|: {}\n|WCGC|: {}".format(len(largest_s_cc), len(largest_w_cc)))