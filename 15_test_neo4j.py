from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password'));

MERGE_USER = """
	MERGE 
		(u:User {twitter_id: $tid}) 
	RETURN u"""
	
MERGE_RELATIONSHIP = """
	MATCH 
		(u1:User {twitter_id: $tu1}), 
		(u2:User {twitter_id: $tu2}) 
	MERGE (u1)-[r:FOLLOWS]->(u2) 
	RETURN r;"""

pairs = [(0,1),(0,2),(3,1),(4,1),(1,2),(3,5),(5,1)]

for u1, u2 in pairs:
	with driver.session() as session:
		session.run(MERGE_USER, tid=u1)
		session.run(MERGE_USER, tid=u2)
		session.run(MERGE_RELATIONSHIP, tu1=u1, tu2=u2)

driver.close()