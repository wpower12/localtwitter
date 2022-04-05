from urllib.request import urlopen
import json 
import plotly.express as px
import numpy as np
import pandas as pd
import networkx as nx

import localtwitter

COUNTY_JSON_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
with urlopen(COUNTY_JSON_URL) as response:
	counties = json.load(response)

EDGES_FN = "data/full_mention_edges.csv"
edges_df = pd.read_csv(EDGES_FN)

USER_FIPS_FN = "data/users_with_fips_2022_02_28.csv"
user_fips = localtwitter.read_csv_to_dict(USER_FIPS_FN)
fips_list = set(user_fips.values())

users_in_fips = {}
for _, (user_id, fips_code) in enumerate(user_fips.items()):
	if fips_code not in users_in_fips:
		users_in_fips[fips_code] = [int(user_id)]
	else:
		users_in_fips[fips_code].append(int(user_id))

# source_user,mentioned_user,weight
g = nx.from_pandas_edgelist(edges_df, 
	source='source_user', 
	target='mentioned_user',
	edge_attr=True,
	create_using=nx.DiGraph)
nx.set_node_attributes(g, user_fips)

scc_raws = []
wcc_raws = []

for _, (fips, user_list) in enumerate(users_in_fips.items()):
	fips_g = g.subgraph(user_list)
	
	sccs = list(nx.strongly_connected_components(fips_g))
	if(len(sccs) > 0):
		s_cc = max(sccs, key=len)
		mag_s_cc = len(s_cc)
	else:
		mag_s_cc = 0 
	scc_raws.append([fips, mag_s_cc])

	wccs = list(nx.strongly_connected_components(fips_g))
	if(len(wccs) > 0):
		w_cc = max(wccs, key=len)
		mag_w_cc = len(w_cc)
	else:
		mag_w_cc = 0 
	wcc_raws.append([fips, mag_w_cc])

scc_df = pd.DataFrame(scc_raws, columns=['fips', 'scc_size'])
scc_df['scc_size'] = np.log(scc_df['scc_size']+1)

wcc_df = pd.DataFrame(wcc_raws, columns=['fips', 'wcc_size'])
wcc_df['wcc_size'] = np.log(wcc_df['wcc_size']+1)

fig_scc = px.choropleth(scc_df, 
	geojson=counties, 
	locations='fips',
	color="scc_size",
	color_continuous_scale="Viridis",
	range_color=(0, scc_df['scc_size'].max()),
	scope="usa",
	labels={'scc_size':'Size of SCC'})
fig_scc.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_scc.show()

fig_wcc = px.choropleth(wcc_df, 
	geojson=counties, 
	locations='fips',
	color="wcc_size",
	color_continuous_scale="Viridis",
	range_color=(0, wcc_df['wcc_size'].max()),
	scope="usa",
	labels={'wcc_size':'Size of WCC'})
fig_wcc.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_wcc.show()
