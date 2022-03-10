import mysql.connector
from decouple import config

import localtwitter

OUTPUT_FN = 'data/tags_with_seeds.csv'
DATABASE_NAME = "Full_Run_DB_00"
# DATABASE_NAME = "Full_Run_01" # For lab machine
cnx = mysql.connector.connect(user=config('DB_USER'),
					password=config('DB_PASSWORD'),
					host=config('DB_HOST'),
					database=DATABASE_NAME)
cur = cnx.cursor()

raw_lists = {
	'Politics': "#political #politics #trump #politicalmemes #news #republican #election #memes #conservative #democrat #liberal #congress #meme #government #vote #usa #communism #democrats #america #india #socialism #donaldtrump #covid #freedom #biden #maga #rahulgandhi #pol #socialist #bhfyp #leftist #marxism #politicalmeme #bjp #communist #libertarian #art #joebiden #anarchism #narendramodi #politicalart #coronavirus #capitalism #anarchist #republicans #politicalcompass #rightwing #anarchy #antifa #politicalhumor #love #democracy #dankmemes #politicians #funny #politica #berniesanders #president #leftism #blm",
	'Democrats': "#trumpsupporters #resist #bluewave #keepamericagreat #americafirst #trumpmemes #dumptrump #conservatives #socialism #memes #politicalmemes #libertarian #draintheswamp #fucktrump #news #coronavirus #fakenews #president #cnn #congress #repost #dnc #progressive #bernie #presidenttrump #obama #antifa #capitalism #progressives #democraticparty #democrats #trump #republicans #maga #joebiden #republican #politics #biden #usa #democrat #donaldtrump #america #election #vote #conservative #liberal #voteblue #blacklivesmatter #kamalaharris #liberals #makeamericagreatagain #blm #covid #bidenharris #gop #trumptrain #democracy #berniesanders #freedom #bhfyp",
	'Republicans': "#republicans #trump #maga #democrats #republican #conservative #donaldtrump #usa #politics #america #conservatives #gop #makeamericagreatagain #trumptrain #kag #joebiden #americafirst #trumpsupporters #biden #keepamericagreat #democrat #republicanparty #conservativememes #election #draintheswamp #freedom #liberal #rightwing #trumpmemes #bhfyp #liberals #potus #vote #a #covid #patriot #libertarian #prolife #memes #presidenttrump #fakenews #congress #foxnews #walkaway #republicanmemes #politicalmemes #democracy #buildthewall #fucktrump #voteblue #american #news #sleepyjoe #redwave #president #kamalaharris #blm #donaldtrumpjr #ndamendment #socialismsucks",
	'WealthTax': "#wealthtax #taxtherich #capitalism #socialism #tax #taxes #politics #eattherich #oligarchy #wealth #oligarch #hierarchy #greed #economicjustice #plutocracy #endthefed #corporatocracy #workerownedcollective #democraticsocialism #progressive #meritocracy #duopoly #neocolonialism #uniparty #maximumwage #livingwage #financialfreedom #techoligarchs #authoritarianism #bhfyp #economy #billionaire #systemicracism #itoligarchs #neoliberalism #billionaires #corporatism #political #trickledowneconomics #trickledown #congress #biden #occupy #democrats #berniesanders #occupyla #finance #incometax #rich #money #trump #jeffbezos #business #corporatetax #economics #trickledownhoax #workingfamilies #rewardworknotwealth #warren #republicans",
	'GreenEnergy': "#greenenergy #renewableenergy #solarenergy #solar #solarpower #cleanenergy #solarpanels #energy #gogreen #sustainability #gosolar #renewables #solarpanel #climatechange #renewable #solarsystem #environment #ecofriendly #photovoltaic #green #solarpv #solarpowered #sustainableenergy #solarinstallation #sustainable #savetheplanet #sun #electricity #nature #bhfyp #windenergy #windpower #windturbine #offgrid #technology #energiasolar #power #solarcell #energia #globalwarming #engineering #future #wind #energyefficiency #sustainableliving #bhfyp #india #climate #cleantech #savemoney #electricvehicle #windfarm #pv #architecture #love #ev #energie #eco #solarlife #battery",
	'MarriageEquality': "#marriageequality #loveislove #marriage #equality #lovewins #lgbtq #pride #lgbt #gay #marriagegoals #love #instagay #marriageadvice #samesexmarriage #gaymarriage #wedding #samesexwedding #gaywedding #marriagetips #marriagequotes #gayisokay #marriagelife #lesbian #marriageworks #marriagematters #marriages #relationshipquote #twogrooms #mrsandmrs #bhfyp #antidiscrimination #twobrides #antibullying #hkpride #changehk #time #humanbluerobin #thegaypassport #gaypassport #rainbowgorgor #gaymarket #glaad #messmerizingrainbows #messmerizingrainbowman #gaycouple #lesbiancouple #messmerizingrainbowroadmap #marriagematerial #messmerizing #rainbowroadmap #messmerizingrainbow #boytrip #queer #marriageproblems #pridehk #gayhk #marriagetip #marriagecelebrant #hongkonggay #wifeandwife",
	'DefundThePolice': "#defundthepolice #blacklivesmatter #blm #acab #nojusticenopeace #policebrutality #georgefloyd #trump #fuckthepolice #breonnataylor #justiceforbreonnataylor #defundpolice #protest #abolishice #justiceforgeorgefloyd #abolishthepolice #policethepolice #biden #antifa #police #vote #maga #repost #racism #lgbtq #icantbreathe #joebiden #fuck #saytheirnames #bhfyp #whiteprivilege #endpolicebrutality #donaldtrump #eattherich #revolution #fucktrump #art #bluelivesmatter #socialjustice #civilrights #follow #endqualifiedimmunity #resist #socialism #endwhitesupremacy #medicareforall #liberal #democrat #endracism #leftist #systemicracism #policereform #kamalaharris #ftp #abolishpolice #prisonreform #israel #socialist #sayhername #dismantlewhitesupremacy",
	'RacialBias': "#liberals #potus #vote #a #covid #patriot #libertarian #prolife #memes #presidenttrump #fakenews #congress #foxnews #walkaway #republicanmemes #politicalmemes #democracy #buildthewall #fucktrump #voteblue #american #news #sleepyjoe #redwave #president #kamalaharris #blm #donaldtrumpjr #ndamendment #socialismsucks #protectblackwoman #problack #equality #sayhername #socialjustice #racialbarriers #grace #whiteamerica #fuckracism #protest #blackculture #racialdiversity #racismstillexists #breakingbarriers #blackunity #alllivesmatter #africanamericans #womanupliftingwoman #police #blackamerica #racialjustice #southpasadena #whitesupremacy #whitepeoplebelike #trump #reparations #whiteisright #patrolandcontrol #melanin #girlsliftinggirls",
	'WhitePrivelege': "#whiteprivelege #blacklivesmatter #racism #whitesupremacy #blm #amerikkka #antiracist #malcolmx #blackwomen #justice #georgefloyd #vote #freepalestine #thisisamerikkka #breonnataylor #blackteachers #ahmaudarbery #blackeducator #blackauthor #wakeupblackpeople #blackwisdom #antiracism #blackconciousness #commonsense #equality #blackpeople #blackamerica #blackdialogue #blackmen #bhfyp #melanatedminds #blackunification #whileblack #africandiaspora #givemelibertyorgivemedeath #blackminds #justiceforgeorgefloyd #activism #jamesbaldwin #indigenous #trayvonmartin #elijahmcclain #nojusticenopeace #socialjustice #trauma #racialequality #protest #blackpower #takeaknee #karen #whitesupremacists #covid #knowyourrightscamp #repost #racists #woke #whitepeople #femenist #gaslighting #standup"	
}

tags_w_seeds = {}
for _, seed_tag in enumerate(raw_lists):
	for tag in raw_lists[seed_tag].split(" "):
		if tag not in tags_w_seeds:
			tags_w_seeds[tag] = set()
		tags_w_seeds[tag].add(seed_tag)

COUNT_SQL = """
	SELECT COUNT(*) FROM tweethashtags
	WHERE hashtag='{}';
"""

tags_w_counts = {}
for t in tags_w_seeds:
	cur.execute(COUNT_SQL.format(t.strip("#")))
	tag_count = cur.fetchone()[0]
	tags_w_counts[t] = [tag_count, tags_w_seeds[t]]

tags_w_counts = dict(sorted(tags_w_counts.items(), key=lambda t: -1*t[1][0]))
with open(OUTPUT_FN, 'w') as f:
	for t in tags_w_counts:
		f.write("{}, {}, {}\n".format(t, tags_w_counts[t][0], tags_w_counts[t][1]))
		print(t, tags_w_counts[t][0], tags_w_counts[t][1])