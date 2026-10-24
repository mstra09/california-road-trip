"""Day 2 content (Guerneville -> Jenner -> Bodega Bay -> West Marin / Petaluma -> Muir Woods -> Golden Gate -> SFO).
Writes content/11_sonoma_coast.json, 12_west_marin.json, 13_golden_gate.json. Every fact comes from the listed sources.

Listeners: Mike (driving; operations director at Just Eat, UK), Adam (renewable-energy investment analyst, UK) and
Julia (nuclear fusion startup, San Francisco); all into geography, skiing, infrastructure, sport, politics and
economics. Formats rotate: story, quick-fire facts, recent news, a debate prompt for the car, and a quiz
(question, [[pause N]], answer) in roughly a quarter of clips, never two in a row on the same road."""
import json

W = 'https://en.wikipedia.org/wiki/'
def clip(id, title, lat, lon, roads, text, sources, priority=3, category='history', kind=None, more=None, radius=None, geo=None):
    c = {'id': id, 'priority': priority, 'category': category, 'title': title, 'lat': lat, 'lon': lon, 'roads': roads,
         'text': text.strip(), 'sources': [W + s for s in sources]}
    if geo: c['sources'].append(f'https://macrostrat.org/api/v2/geologic_units/map?lat={geo[0]}&lng={geo[1]}&scale=large')
    if kind: c['kind'] = kind
    if radius: c['radius'] = radius
    if more: c['more'] = {'title': more[0], 'text': more[1].strip(), 'sources': [W + s for s in more[2]]}
    return c

COAST = ['sr116_coast', 'sr1_coast']
SR1 = ['sr1_coast']
TAM = ['sr1_coast', 'valley_ford_101', 'muir_sfo']

sonoma_coast = [
clip('day2_start', 'Day two: river, ocean, redwoods, bridge', 38.488, -123.012, ['sr116_coast'], """
Good morning, road-trippers! Day two. Mike's on driving duty, Adam and Julia are in charge of snacks, and I'm in charge of the chat.

Here's the plan. We follow the Russian River to the ocean, then drive down the wild Sonoma Coast to Bodega Bay, where Hitchcock made birds terrifying. Then either along Tomales Bay and Point Reyes, or inland through Petaluma, to the giant redwoods of Muir Woods. And finally over the Golden Gate Bridge, through San Francisco, to the airport.

Big trees first, if you've got an hour before you leave: Armstrong Redwoods is just north of Guerneville. The Parson Jones Tree, a hundred yards from the entrance, is more than 310 feet tall, and the Colonel Armstrong Tree is over 1,400 years old. And Muir Woods is later today. Seafood too: oysters on Tomales Bay, and crab country around Bodega Bay.

I've packed the rest of today with a bit of everything. Earthquakes and geography, obviously, because we'll be driving along the San Andreas Fault for a good chunk of the morning. A nuclear power fight that Julia will enjoy. Offshore wind politics for Adam. Some infrastructure and logistics stories for Mike. A famous sailing comeback, the Olympics that came out of nowhere, and a few things that happened in the news this past year or two. Let's go find the ocean.
""", ['Russian_River_(California)', 'San_Andreas_Fault', 'Armstrong_Redwoods_State_Natural_Reserve'], priority=5, category='geography', kind='intro'),

clip('duncans_mills', 'Monte Rio and Duncans Mills: the railroad to the redwoods', 38.4539, -123.0544, ['sr116_coast'], """
Picture this road with a little narrow-gauge train chugging along beside the river. From the 1870s, the North Pacific Coast Railroad ran from Cazadero, through Monte Rio and Duncans Mills, all the way down to the ferry at Sausalito. Remember that name, because the same railway also stopped at Valley Ford, Tomales, Marshall and Point Reyes Station. We're basically following its ghost all morning.

The business model changed twice. First, it hauled redwood lumber to build San Francisco: in 1877 Alexander Duncan set up a sawmill right here, and a town grew around it, with two hotels, a saloon, a blacksmith and a livery stable. When the timber ran out, the railroad pivoted to tourists, carrying San Franciscans up to summer cabins. Monte Rio, back there, rebranded as Vacation Wonderland, complete with a seven-story hotel downtown, and parts of the 1942 Oscar-winning film Holiday Inn were shot at a resort there.

By the 1930s the trains had stopped and Duncans Mills faded away. It was rescued in 1976 by a Bicentennial restoration project. There's still an original depot here, with some of the old railroad cars parked outside.
""", ['Duncans_Mills,_California', 'Monte_Rio,_California'], category='history'),

clip('jenner', 'Jenner: the river meets the sea', 38.4497, -123.1157, COAST, """
There it is! The Russian River meets the Pacific, right here at Jenner. Population: about a hundred and twenty.

The town is named after Dr. Elijah Jenner, a dentist and inventor from Vermont who came west for the Gold Rush in 1850. While mining, he designed a pump that could lift water a hundred feet. Quiz: when he applied for the patent, he sent in a model of the pump. What was so special about it? [[pause 5]] It was made of pure gold! It's the only golden model the Patent Office has ever received. A proper Gold Rush flex.

Now watch the river mouth. In summer, the waves build a sandbar right across it, and the river backs up into a lagoon until the water gets high enough, somewhere between four and a half and seven feet at the Jenner visitor center, and then it breaks through. In winter, the sheltered beach on the north side is where harbor seals have their pups.
""", ['Jenner,_California', 'Goat_Rock_Beach'], priority=4, category='geography'),

clip('goat_rock', 'Goat Rock: sea stacks, mammoths and the Goonies', 38.4405, -123.1180, SR1, """
Movie quiz! Down on the right is Goat Rock Beach, with that huge flat-topped rock barely hanging on to the land. In 1985, a very famous adventure movie about a group of kids hunting for pirate treasure filmed its ending on this beach. Which one? [[pause 5]] The Goonies! Goonies never say die.

Those rocks out in the sea are called sea stacks. For about 170 million years, an ocean plate was diving under North America, scraping off pillow lava, chert and sandstone and crushing it all into a jumble called mélange: hard blocks floating in softer, ground-up rock. The waves wash away the soft stuff and leave the hard blocks standing. Goat Rock is one big block of greywacke sandstone.

And my favourite fact on this coast: about a mile south of the river there's a blue rock with rubbing marks two to four meters up. Far too high for cows. Scientists think mammoths used it as a back-scratcher, as recently as 40,000 years ago.
""", ['Goat_Rock_Beach', 'Sonoma_Coast_State_Park', 'Bodega_Bay,_California'], priority=4, category='geology'),

clip('sonoma_coast', 'The coast that is falling into the sea', 38.389, -123.087, SR1, """
Quick-fire facts on the Sonoma Coast.

One: it's seventeen miles of state beaches from just north of Jenner down to Bodega Head.

Two: it's disappearing. Those soft bluffs lose one to three feet a year on average, more in a stormy winter.

Three: it's also rising. You're driving on a flat shelf above the beach called a marine terrace. It's old sea floor, lifted up over the ages. Some sea stacks are even stranded up on the terrace, away from the water, because they started life on the sea floor before it rose.

Four: people have lived here a very long time. Dozens of Coast Miwok and Pomo shell middens, basically ancient kitchen rubbish heaps, have been found along here.

Five: keep an eye out to sea for gray whales, harbor seals and sea lions.
""", ['Sonoma_Coast_State_Park', 'Goat_Rock_Beach'], category='geography'),

clip('coastal_act', 'Why Highway 1 will never be a motorway', 38.362, -123.066, SR1, """
Here's a bit of infrastructure politics, Mike, since you're the one stuck behind the camper vans. Ever wondered why Highway 1 is just one lane each way, even on busy summer weekends?

It's the law. The 1976 California Coastal Act specifically bans widening Highway 1 beyond one lane in each direction in the rural parts of the coastal zone. It's enforced by the California Coastal Commission, which has quasi-judicial control over development and public access along 1,100 miles of coastline. Its zone runs inland from about a thousand yards up to five miles. Inside it, almost anything, from a new house to splitting a plot of land or changing how people get to the beach, needs a coastal permit.

It's one of the most powerful land-use bodies in America, and it's in constant fights. In 2019, for example, it allowed a seawall to protect apartments built in 1972, but refused one for townhomes built in 1984, because the Act only protects buildings that existed when it was passed. The townhome owners sued.

Debate for the car: is this brilliant protection of the coast, or a planning system gone too far? You've got until Bodega Bay.
""", ['California_Coastal_Commission'], priority=3, category='politics'),

clip('bodega_bay', 'Bodega Bay: Russians, Spaniards and a lot of movies', 38.3333, -123.0481, SR1, """
Welcome to Bodega Bay! Fishing boats, salty air, and a harbor tucked behind that long headland.

It's named after Juan Francisco de la Bodega y Quadra, a Spanish naval officer who sailed in here in 1775. In 1793 the Spanish parked a little garrison here with four cannons, because they'd heard the English might turn up. They didn't, so the guns went home to Monterey. Then the Russians turned up instead! In 1809 they put up the first Russian buildings in California here, before building Fort Ross, and called the place Port Rumyantsev.

Hollywood loves it too: The Birds, The Fog, I Know What You Did Last Summer, The Russians Are Coming. Quiz: in 2021, a famous American TV comedy needed to film a season in Ireland, but COVID made that impossible, so Bodega Bay played Ireland. Which show? [[pause 5]] It's Always Sunny in Philadelphia! A Californian fishing village pretending to be Ireland. With this fog, it works.
""", ['Bodega_Bay,_California', 'Bodega,_California'], priority=4, category='history'),

clip('seafood', 'Lunch briefing: crab and oysters', 38.347, -123.057, ['sr1_coast'], """
Lunch briefing, since I hear seafood is today's top priority.

Crab first. The working boats in Bodega Bay, coming up, go after Dungeness crab, one of the most important seafood catches on the whole West Coast, found from Alaska's Aleutian Islands down to near Santa Barbara. The fishery was started by San Francisco fishermen back in 1848, the year gold was found. By the early 1900s, rules said you could only keep hard-shelled male crabs at least six inches across, and those are still the rules today. Most are caught in baited wire pots on a buoy, and every pot must be tied on with a biodegradable rot cord, so if it's lost it eventually opens and stops trapping crabs.

Then oysters, on Tomales Bay, about forty minutes further on if you take the coast route. The two big farms, Hog Island and Tomales Bay Oyster Company, both sell to the public with picnic tables by the water, on the east shore near Marshall, right on Highway 1.

Mike, as the operations man: oysters from bay to table in about fifty yards. Hard to beat that supply chain.
""", ['Dungeness_crab', 'Tomales_Bay', 'Bodega_Bay,_California'], priority=4, category='food'),

clip('the_birds', 'The Birds: the true story behind the film', 38.326, -123.040, SR1, """
Story time. In August 1961, the people of Capitola, a seaside town further down this coast, woke up to something out of a nightmare. Thousands of seabirds were dive-bombing their houses, crashing into cars and dropping half-eaten fish on people's lawns.

Alfred Hitchcock read about it. He was already working on a film based on a Daphne du Maurier story about birds attacking people, and he used the Capitola event as research. The result was The Birds, released in 1963 and set right here in Bodega Bay. Tippi Hedren, in her first film, drives up from San Francisco with a pair of lovebirds, and it goes very, very badly: gulls at the dock, crows at the schoolhouse, sparrows pouring down the chimney.

Most of the birds were real. The gulls were caught at the San Francisco rubbish dump, and some of the crows were actually ravens. It took 370 special-effects shots, and the final shot was stitched together from 32 separate pieces.

And what really happened in Capitola? Toxic algae had poisoned the birds. Nobody knew that in the 1960s. A darker footnote: decades later, Tippi Hedren said Hitchcock harassed her during filming. Today it's rated one of the greatest horror films ever made.
""", ['The_Birds_(film)', 'Bodega_Bay,_California'], priority=4, category='culture'),

clip('hole_in_the_head', 'The Hole in the Head: where the anti-nuclear movement was born', 38.3215, -123.035, SR1, """
Julia, this one's for you. Across the harbor is Bodega Head, and it has a hole in it, literally. It's where America's anti-nuclear movement is said to have been born.

In the late 1950s, the utility company PG&E planned to build a nuclear power plant on the headland, meant to be the first commercially viable one in the country. The fishermen worried about their livelihoods. A local landowner, Rose Gaffney, refused to sell, sued the company, and invited government officials to come and look at the fault lines on the site. In June 1963, protesters released 1,500 helium balloons, each carrying the message that it could represent a radioactive molecule of strontium 90 or iodine 131.

The real clincher was geology. The San Andreas Fault runs right between Bodega Head and the mainland. The headland is on the Pacific Plate, the town's on the North American Plate, and in the 1906 earthquake the headland moved about fifteen feet. In 1964, after a negative review by the Atomic Energy Commission, PG&E gave up. By then they'd already dug the pit for the reactor. It filled with water, and the locals call it the Hole in the Head.
""", ['Bodega_Bay_Nuclear_Power_Plant', 'Bodega_Head', 'Bodega_Bay,_California'], priority=4, category='politics',
 more=('From Bodega Head to Diablo Canyon and Livermore', """
So where did California's nuclear story go next? Today it has exactly one working nuclear plant: Diablo Canyon, on the central coast, also run by PG&E. It makes about 8.6 percent of the state's electricity, and nearly a quarter of its carbon-free power. It was built less than a mile from a fault line nobody knew about at the time, and in 1981 nearly two thousand protesters were arrested there in just two weeks.

In 2016, PG&E said it would close it in 2024 and 2025, partly because California's rules give renewables priority. Then the grid operators warned of blackouts, 79 scientists wrote an open letter, and in 2022 a new state law extended it to 2030.

And Julia's world: fusion. At Livermore, on the other side of the Bay, the National Ignition Facility fires the world's most energetic laser at a tiny fuel capsule. On the 5th of December 2022 it got more energy out of the fuel than the laser put in: 3.15 megajoules out, from 2.05 in. The catch: making that laser pulse took about 300 megajoules from the grid. By 2025, shots had reached 8.6 megajoules. Julia, over to you: how far away is a fusion power plant?
""", ['Diablo_Canyon_Power_Plant', 'National_Ignition_Facility'])),

clip('bodega', 'Bodega: rusty cannons and a famous schoolhouse', 38.3449, -122.9719, SR1, """
This little village is Bodega, once called Bodega Corners, to tell it apart from the port down by the water. There were two Coast Miwok villages around here, and then in 1809 the Russians settled in the Salmon Creek valley.

When the Russians left, around 1843, John Sutter bought their land, including this area. The sale included some hunting rights, a small boat, several rusty cannons and some old muskets. Bargain. The same year, a Captain Stephen Smith built the first lumber mill on the West Coast near here. The town proper began in 1853 with a saloon, a blacksmith and a hotel, which is the correct order of priorities.

If the church and the schoolhouse look familiar, that's because they starred in The Birds. They're right here on the Bodega Highway, and the schoolhouse is where the crows gather on the climbing frame.

And underfoot, the geology maps show the Wilson Grove Formation, sea-floor sandstone from the late Miocene and Pliocene, very roughly ten to three million years ago. The same sandstone we met back in Sebastopol.
""", ['Bodega,_California', 'Bodega_Bay,_California', 'The_Birds_(film)'], category='history', geo=(38.33041, -122.99587)),

clip('offshore_wind', 'Why there are no wind turbines out there (yet)', 38.125, -122.862, ['sr1_coast'], """
Adam, this one's yours. Out past Point Reyes is open Pacific, with some of the strongest offshore wind in the country. So where are all the turbines?

The problem is depth. The seabed off California drops away fast, so instead of fixed turbines on the seabed like in the North Sea, it needs floating ones. In 2021 the Biden administration approved large areas off the coast for floating wind farms, and in 2022 California set a target of 25 gigawatts of offshore wind by 2045. Then, this year, in 2026, the second Trump administration negotiated a series of deals that stopped three of the state's five offshore wind projects.

Meanwhile, on land, solar has boomed. By the end of 2023, solar was making 28 percent of California's electricity, the most of any state. And the law says 60 percent of the state's power must be renewable by 2030, and 100 percent by 2045. The headache is the duck curve. Solar floods the grid at midday, then disappears at sunset, just as everyone gets home, so other plants have to ramp up by about five gigawatts an hour. That's why solar with batteries is now worth so much more than solar without.

Over to the analyst: would you rather back floating wind off this coast right now, or batteries?
""", ['Wind_power_in_California', 'Solar_power_in_California'], priority=3, category='economics'),

clip('valley_ford', 'Valley Ford and the Running Fence', 38.3178, -122.9236, ['sr1_coast', 'valley_ford_101'], """
Tiny Valley Ford, population about a hundred and fifty, in rolling dairy country. The Coast Miwok had a village here called Ewapalt. There was a grain mill in the 1850s, and from 1876 the railway stopped here, so ranchers and fishers could ship their produce to San Francisco.

Quiz: in 1976, the artists Christo and Jeanne-Claude built a giant artwork that passed right through Valley Ford, running from Cotati all the way to Bodega Bay. What was it? [[pause 5]] A fence! Running Fence: a long white fabric fence over the hills and down into the ocean.

Two more. Guitarists, take note: Shubb, the company that makes guitar capos, has its headquarters right here. And a grimmer one: run-off from the dairies has put so much nitrate in the groundwater that in 2017 the state warned pregnant women and babies not to drink the town's well water. Some restaurants truck their water in from Petaluma.
""", ['Valley_Ford,_California'], category='culture'),
]

west_marin = [
clip('tomales', 'Tomales: into Marin County', 38.2470, -122.9050, SR1, """
Welcome to Marin County, and to Tomales, population just under two hundred.

The Coast Miwok had villages all around here, including one called Utumia, near the town. The post office opened in 1854, spelled Tomalles, with two L's, and later lost one. And the North Pacific Coast Railroad came through in the 1870s.

Tomales sits close to the San Andreas Fault, and you can still see the 1906 earthquake here, in the cemetery. One of the town's two cemeteries is older than the earthquake, and the damage to the old graves shows just how far the shaking reached.
""", ['Tomales,_California'], category='history'),

clip('tomales_bay', 'Tomales Bay: the fault you can sail on', 38.205, -122.925, SR1, """
That long, skinny bay is Tomales Bay: fifteen miles long, about a mile wide, and only eighteen feet deep on average. In 1603, Spanish explorers from the Vizcaíno expedition saw it, assumed it was a river, and named it the Rio Grande de San Sebastián.

But it's not a river. It's a fault. Tomales Bay is a drowned stretch of the San Andreas Fault. Everything on the far side, the Point Reyes Peninsula, is on the Pacific Plate. You're on the North American Plate. The fault runs from here down the Olema Valley to Bolinas Lagoon, and this road follows it nearly the whole way.

The Coast Miwok had villages all around the bay. And the shells and clams from its shores weren't just food: they were used as money.
""", ['Tomales_Bay'], priority=4, category='geology'),

clip('marshall', 'Marshall: oysters and a creamery', 38.1617, -122.8930, SR1, """
This stretch of shore is Marshall, and if anyone's hungry: oysters.

The town is named after four Marshall brothers who started dairy farming here in the 1850s. There's still dairy, with the Straus Family Creamery based here, but the big business now is oysters and clams. The two biggest producers on Tomales Bay are Hog Island Oyster Company and Tomales Bay Oyster Company, and both sell straight to the public, with picnic tables right on this shore. If you stop, the local move is a bag of oysters at a table by the water.

Mike, a supply-chain footnote. Just across the peninsula, the Drakes Bay Oyster Company farmed oysters inside the national seashore until the government refused to renew its permit in 2012. It fought all the way to the US Supreme Court, which declined to hear the case in 2014, and the farm closed at the end of that year.
""", ['Marshall,_California', 'Tomales_Bay', 'Point_Reyes_National_Seashore'], category='food'),

clip('point_reyes_station', 'Point Reyes Station: the town that could not pick a name', 38.0693, -122.8068, SR1, """
Welcome to Point Reyes Station, the little hub town for the Point Reyes peninsula.

It started as the end of the railway line. When the trains arrived in 1875, it was called Olema Station. Then, in 1891 alone, the name changed three times: first to Marin, then back to Point Reyes, then finally Point Reyes Station.

It used to be a real port on Tomales Bay, too. But cattle and European grasses caused erosion, and silt, small dams and landfill for farming raised the old salt marshes. Now the town is nearly a mile from the nearest tidal flats.
""", ['Point_Reyes_Station,_California'], category='history'),

clip('olema', 'Olema: coyote valley, and the ranches coming out', 38.0410, -122.7886, SR1, """
This crossroads is Olema, from a Coast Miwok name meaning coyote valley. For years people believed it was the epicenter of the 1906 earthquake, because the ground moved so much here. Scientists now think the epicenter was offshore, near Daly City.

Now some very recent news. Those green hills inside Point Reyes National Seashore have been cattle ranches for well over a century, about 28,000 acres of dairy and beef, leased back to the ranchers when the park was created. But the ranches have been accused of polluting the creeks and Tomales Bay with E. coli, and a 2022 inspection found raw sewage leaking from some of them.

In January 2025, a deal brokered by The Nature Conservancy bought out most of the ranchers. Cattle numbers are being cut from about 10,000 to 200, and most of the park goes back to wilderness. Debate for the car: a win for nature, or the end of a working landscape?
""", ['Olema,_California', 'Point_Reyes_National_Seashore', '1906_San_Francisco_earthquake'], priority=3, category='politics'),

clip('drake_story', 'Francis Drake, New Albion and the porcelain clue', 38.10, -122.87, SR1, """
Story time. On the 17th of June, 1579, the English captain Francis Drake sailed into a sheltered cove just over those hills. His ship, the Golden Hind, needed repairs after months of raiding Spanish towns and treasure ships up the Pacific coast, and he was about to sail home the long way, right round the world.

He stayed about five weeks, and got on well with the Coast Miwok who lived here. He named the land New Albion, partly because its white cliffs reminded him of England, and claimed it for Queen Elizabeth the First, nailing up a brass plate with a sixpence showing her face. On the 23rd of July he sailed away, without leaving a colony.

For centuries, people argued about exactly where he'd landed. Quiz: one of the best clues came from archaeologists, who found nearly a hundred pieces of something near the cove that had to have come from Drake. What? [[pause 6]] Chinese porcelain! Broken dishes that Drake had taken from a Spanish treasure ship and dumped here while lightening his ship for repairs. In 2021, California officially recognised Drake's Cove, inside the national seashore, as the site of New Albion.
""", ['New_Albion', 'Point_Reyes_National_Seashore'], priority=4, category='history', kind='story', radius=20000),

clip('point_reyes_wild_story', 'Point Reyes: elk, elephant seals and the foggiest lighthouse', 38.03, -122.82, SR1, """
Out on the Point Reyes peninsula is one of the wildest corners of California, and it's full of comeback stories.

Quiz: when Europeans arrived, there were maybe half a million tule elk in California. By the 1870s, people thought they were extinct. How many were found, hiding in a marsh in the Central Valley? [[pause 5]] A single breeding pair! In 1978, ten tule elk were brought here to Tomales Point and fenced in. They thrived, then nearly half died in the drought of 2012 to 2015, and in 2020 activists illegally carried water to them. In December 2024, the Park Service finally breached the fence, and now they roam free.

Then the elephant seals came back, starting a colony in 1981. During the government shutdown of January 2019, with no rangers around, they moved onto Drakes Beach and had their pups in the car park.

And at the very tip is the Point Reyes Lighthouse, first lit in 1870, officially the windiest and foggiest spot on the Pacific coast. Unusually, it's built low, down about three hundred steps, to get the light below the fog.
""", ['Tule_elk', 'Point_Reyes_National_Seashore', 'Point_Reyes_Lighthouse'], priority=3, category='nature', kind='story', radius=20000),

clip('san_andreas_story', 'Riding the San Andreas Fault', 38.00, -122.76, ['sr1_coast', 'muir_sfo'], """
Right now we're driving almost exactly along the San Andreas Fault. This straight valley is the fault zone. To the north it sinks under Tomales Bay; to the south it runs under Bolinas Lagoon. Then it heads out to sea and comes back on land near Daly City, which we'll pass this afternoon.

Some numbers. The fault runs about 750 miles through California. The Pacific Plate, on your right, slides north about an inch a year compared with the North American Plate. But it doesn't slide smoothly. It sticks, builds up strain for decades, then lets go. In 1906, the ground along the fault shifted by up to twenty feet.

After that earthquake, a Berkeley geology professor, Andrew Lawson, mapped all the fences and roads that had been sliced in half and shifted. They made an almost perfect line along a fault he'd found back in 1895. He named it after the San Andreas Valley, down the peninsula. We'll drive right past it near the airport. And the granite of Point Reyes, over there, matches the Sierra Nevada. It's been carried hundreds of miles north along this fault.
""", ['San_Andreas_Fault', '1906_San_Francisco_earthquake', 'Point_Reyes_National_Seashore', 'Bodega_Head'], priority=4, category='geology', kind='story', radius=25000),

clip('bolinas', "Bolinas: the town that doesn't want to be found", 37.935, -122.695, SR1, """
Somewhere across the lagoon is Bolinas, and you won't see a sign for it, because the locals keep tearing them down. Every road sign on Highway 1 pointing the way has been removed by residents. The county even put it to a vote, and the voters said: no more signs, thank you.

It's a famously private little town of about fourteen hundred people. It also has a great property story. In 1927, an old dairy farm on the mesa was split into more than five thousand tiny lots, and a San Francisco newspaper sold many of them for 69 dollars and fifty cents each, as a subscription promotion. Buy the paper, get some land. Some of those streets have since fallen into the sea. And in March 2023, the town's post office closed, so the residents are petitioning to get it back.

The water you're passing is Bolinas Lagoon, on the international list of important wetlands. The fault runs right down the middle of it, so Bolinas is on the Pacific Plate, creeping north away from Stinson Beach.
""", ['Bolinas,_California', 'Bolinas_Lagoon'], category='culture'),

clip('stinson_beach', 'Stinson Beach and the craziest race in America', 37.9007, -122.6443, SR1, """
Stinson Beach! A long sandy beach that San Franciscans have been escaping to for 150 years. It started as Willow Camp, tents among the willows. After the 1906 earthquake, refugees from the city came out and opened some of its first businesses, and in 1916 it was renamed after the biggest landowners, Rose and Nathan Stinson.

Sports fans: this is the finish line of the Dipsea, the oldest trail race in America. Since 1905, runners have raced seven and a half miles from Mill Valley, over the shoulder of Mount Tam, to this beach, with about 2,200 feet of climbing. You can take shortcuts with names like Suicide and the Swoop, and the oldest and youngest runners get up to a 25-minute head start. Quiz: so how young was the youngest-ever winner? [[pause 5]] Eight years old! Winners have been as old as 72. And Jack Kirk, the Dipsea Demon, finished 67 in a row and started his last one aged 96.

One warning if you fancy a swim: these waters are in the Red Triangle, known for great white sharks.
""", ['Stinson_Beach,_California', 'Dipsea_Race', 'Bodega_Head'], priority=4, category='sport'),
]

marin_sf = [
clip('mount_tam', 'Mount Tam: the crookedest railroad and the first mountain bikes', 37.8867, -122.6236, TAM, """
The big mountain above us is Mount Tamalpais, Mount Tam to the locals, 2,571 feet at the East Peak.

Myth-busting first. You'll hear that Tamalpais means Sleeping Maiden, from a Miwok legend about the mountain's profile. It doesn't. That legend was invented in Victorian times by a playwright, for a play at the mountain's outdoor theatre. The name really comes from the Coast Miwok támal pájis, meaning west hill.

From 1896 to 1930, a railway wound up from Mill Valley to the summit, with so many bends it was nicknamed the Crookedest Railroad in the World.

And here's one for sports fans: this mountain is the birthplace of mountain biking. In the 1970s, riders bolted fat tyres and better brakes onto old 1930s and 40s Schwinn bikes and bombed down the fire roads. Their downhill races near Fairfax were called the Repack races, because the coaster brakes got so hot that the grease burned off, and riders had to repack their wheel bearings after every run. Gary Fisher, Charlie Kelly and Joe Breeze were among the pioneers.
""", ['Mount_Tamalpais', 'Mountain_biking'], priority=3, category='sport'),

clip('muir_woods', 'Muir Woods: the man who gave away a forest', 37.8935, -122.5774, TAM, """
Welcome to Muir Woods, one of the last old-growth redwood forests in the Bay Area, in a canyon on the side of Mount Tam that's wrapped in fog all summer. The redwoods drink that fog during the dry season.

Here's how it survived. Mount Tam's redwoods were logged heavily to build San Francisco, and again to rebuild it after 1906. But the trees in this canyon were too hard to reach. In 1905, William Kent and his wife Elizabeth bought 611 acres of it for 45,000 dollars, with money borrowed from a banker friend. Then a water company tried to take part of it to build a dam and reservoir. So Kent used a brand-new law, the Antiquities Act, and offered the land to the nation. President Theodore Roosevelt accepted, and in January 1908 it became a national monument.

The name first suggested was the Kent Monument, but Kent insisted on honouring the naturalist John Muir. The two later fell out, because Kent backed the dam that flooded Yosemite's Hetch Hetchy Valley. Kent went on to sponsor the law that created the National Park Service in 1916. He was also a loud supporter of anti-Asian immigration laws, so he's a complicated hero.

The tallest tree here is 258 feet, most are 500 to 800 years old, and they grow from a seed the size of a tomato seed.
""", ['Muir_Woods_National_Monument', 'William_Kent_(American_politician)'], priority=5, category='nature',
 more=('Muir Woods and the founding of the United Nations', """
One more Muir Woods story. In April 1945, delegates from 50 countries gathered in San Francisco to write the Charter of the United Nations. President Franklin Roosevelt was due to open the conference, but he died on the 12th of April, just before it began. So on the 19th of May, the delegates came out here to Cathedral Grove and held a ceremony in his memory among the redwoods, and left a plaque in his honour. It's still there.

And a practical note: Muir Woods gets up to six thousand visitors a day at peak times, and since 2018 you need a reservation to park or take the shuttle.
""", ['Muir_Woods_National_Monument'])),

clip('redwoods_story', 'Coast redwoods: the tallest living things on Earth', 37.89, -122.60, ['sr1_coast', 'valley_ford_101', 'muir_sfo', 'sr116_coast'], """
Five things about coast redwoods.

One: they're the tallest living trees on Earth. The record holder, up in Humboldt County, is about 381 feet.

Two: they can live about 2,000 years and grow 29 feet across.

Three: they only grow in a narrow strip along the coast, from south of Big Sur up to the corner of Oregon, because they need fog. In dry summers they drink moisture straight out of the air.

Four: before the Gold Rush they covered about two million acres. Today only about five percent of the old-growth forest is left.

And five: the oldest, tallest trees tend to survive in deep, steep canyons, partly because loggers simply couldn't get them out. That's exactly how Muir Woods made it.
""", ['Sequoia_sempervirens', 'Muir_Woods_National_Monument'], priority=3, category='nature', kind='story', radius=15000),

clip('petaluma', 'Petaluma: the Egg Capital of the World', 38.2330, -122.6400, ['valley_ford_101'], """
Welcome to Petaluma! Quiz: Petaluma's old nickname was the Egg Capital of the World, and it had a second nickname, a pun on the town's name. Any guesses? [[pause 5]] Chickaluma! This town was all about chickens. It had the only known poultry drugstore, a chemist's for chickens, and in 1879 Lyman Byce invented the coal-lamp egg incubator here. They still hold a Butter and Eggs Day parade.

The land was part of Rancho Petaluma, granted in 1834 to our old friend General Vallejo from Sonoma. In 1836 he built a huge adobe ranch house just east of town, the largest privately owned adobe ever built in California.

And a lucky break: in 1906, Petaluma was barely damaged, thanks to solid bedrock, so it became the base for rescue and relief across the county. That's also why downtown still has its old iron-fronted buildings and Victorian houses.
""", ['Petaluma,_California', 'Rancho_Petaluma_Adobe'], priority=4, category='history'),

clip('chief_marin', 'Chief Marin and the naming of Marin County', 38.00, -122.535, ['valley_ford_101'], """
We're passing San Rafael, the county seat of Marin. So who was Marin?

The Coast Miwok have lived here for about 6,500 years, and more than 600 of their village sites have been found. According to General Vallejo, who chaired the committee that named California's counties in 1850, this one was named after Marin, a great Coast Miwok chief. His birth name was Huicmuse. He was baptised Marino around the age of twenty, in 1801, and lived for years at Mission Dolores in San Francisco. Vallejo believed he'd fought fierce battles against the Spanish.

There's a rival theory: in 1775 the Spanish named the bay here after Our Lady of the Rosary, la Marinera, and Marin might just be short for that. I'm sticking with the chief.

And a movie footnote: before it moved to the Presidio in San Francisco, George Lucas's company Lucasfilm had its headquarters here in San Rafael.
""", ['Marin_County,_California', 'Mill_Valley,_California', 'Presidio_of_San_Francisco'], category='history'),

clip('palisades_story', 'The Olympics that came out of nowhere', 37.96, -122.52, ['valley_ford_101', 'muir_sfo'], """
Skiers, this one's for you. If you live in San Francisco, your nearest big mountains are around Lake Tahoe. And the biggest ski resort there has quite a story.

In 1956, Squaw Valley had one chairlift, two rope tows and a fifty-room lodge. And yet it won the right to host the 1960 Winter Olympics. Its founder, Alexander Cushing, sold it as a blank canvas, and California poured in money for roads, bridges, water and power. At the 1956 Games, there wasn't even a mayor to hand the Olympic flag to, because Squaw Valley wasn't a town. The 1960 Games were the first Winter Olympics televised live, with CBS paying just 50,000 dollars for the US rights. It's also the only Winter Olympics with no bobsled, because the organisers decided a bobsled run wasn't worth building for the nine countries planning to enter.

Today it's the biggest ski area around Lake Tahoe, joined to Alpine Meadows by a gondola. And in 2021 it changed its name to Palisades Tahoe, because the word squaw is a slur. Debate for the car: best ski resort any of you has ever skied. Go.
""", ['Palisades_Tahoe', '1960_Winter_Olympics'], priority=3, category='sport', kind='story', radius=30000),

clip('mill_valley', 'Mill Valley, Chief Marin and the Blind Pig', 37.8800, -122.5200, ['muir_sfo', 'valley_ford_101'], """
This junction, where Highway 1 meets 101, sits at the edge of Mill Valley, the town tucked into the redwood canyons on Mount Tam.

People have lived here a very long time. Fourteen Coast Miwok village sites have been found around Mill Valley, with huge shell mounds along Richardson Bay. One, dug up in 1907, was twenty feet high. A plaque in a Mill Valley pavement marks the spot believed to be Chief Marin's birthplace, in 1781.

And right around this intersection, in 1916, a roadhouse called the Blind Pig was built just outside the town limits, where the dry laws weren't enforced as strictly. During Prohibition, the roadhouses around here were known as gin joints, and worse.
""", ['Mill_Valley,_California'], category='history'),

clip('sausalito', 'Sausalito: streets under the bay', 37.858, -122.500, ['muir_sfo'], """
Down to the left is Sausalito, on Richardson Bay. The name is Spanish for little willow grove, and it's been spelled about a dozen ways over the years.

Before the bridge, Sausalito was the end of the line. Trains from up north, including that North Pacific Coast Railroad from the Russian River, met the ferries here. The car ferry to San Francisco took about twenty minutes and cost a dollar a car. In World War Two it became a shipbuilding town, and afterwards it went arty and wealthy, and famous for its houseboats.

Quiz: when Sausalito was laid out, planners assumed it would grow by filling in the bay, like San Francisco did. So what's odd about some of its streets? [[pause 5]] They're underwater! Streets with names like Pescadero, Eureka and Teutonia were mapped out, but they're still under Richardson Bay. More than a fifth of the city is water.
""", ['Sausalito,_California', 'Golden_Gate_Bridge'], category='history'),

clip('marin_headlands', 'The Marin Headlands: the city that never got built', 37.840, -122.486, ['muir_sfo'], """
Those wild green hills on the right are the Marin Headlands. They look untouched, but they came close to becoming a city.

In the 1960s, the government sold more than 2,000 acres here to a developer who planned a new town called Marincello, for 30,000 people, in 50 apartment towers, with housing estates, a shopping centre and a hotel. In 1970 the developer lost a lawsuit, and the land went to the Golden Gate National Recreation Area instead.

The hills are also full of old forts and gun batteries from the 1890s to World War Two, built to keep enemy ships out of the bay, plus a Cold War Nike missile site. And every autumn, tens of thousands of hawks, falcons and eagles funnel down the peninsula over Hawk Hill, because they hate flying over open water.
""", ['Marin_Headlands'], category='nature'),

clip('golden_gate_bridge', 'The Golden Gate Bridge', 37.8199, -122.4783, ['muir_sfo'], """
Here it is, everyone! The Golden Gate Bridge! Cameras out, passengers.

When it opened in 1937, it was the longest and tallest suspension bridge in the world: towers 746 feet tall, a main span of 4,200 feet. Plenty of experts said it couldn't be built at all, because of the wind, the fog and the tides.

Quiz: the colour is International Orange, chosen by the architect Irving Morrow. But the US Navy wanted something more visible to ships. What did they suggest? [[pause 5]] Black and yellow stripes! A giant bumblebee. Thank goodness for Morrow.

Some infrastructure numbers for the engineers in the car. The two main cables contain about 80,000 miles of steel wire, more than three times round the Earth. Each tower has about 600,000 rivets. And the chief engineer, Joseph Strauss, insisted on safety nets under the workers. Nineteen men survived falls into them and formed the Half Way to Hell Club. Sadly, eleven men still died, ten in a single accident in February 1937.
""", ['Golden_Gate_Bridge'], priority=5, category='infrastructure',
 more=('How the bridge was paid for, and why Marin has no BART', """
Now the economics. After the 1929 crash, the bridge district couldn't sell its 30-million-dollar bond issue. Then in 1932, Amadeo Giannini, founder of Bank of America, agreed to buy the whole lot to help the local economy. And the bonds were paid off in 1971, entirely from tolls.

Those tolls, charged on the southbound side only, are still the district's main income, and that had a big side effect. In the 1950s and 60s, the district opposed running BART trains across the bridge, because it didn't want to lose toll money. That helped push Marin County out of the BART system altogether. So the reason there's no train from Marin to the city is basically a toll booth.

One more for the road: for the bridge's 50th birthday in 1987, they let pedestrians on, and around 300,000 people packed the deck at once. The arch in the middle flattened out under their weight. Engineers say it was designed to flex, but they haven't tried it again.
""", ['Golden_Gate_Bridge', 'Golden_Gate_Bridge,_Highway_and_Transportation_District'])),

clip('presidio', "The Presidio, and the greatest comeback in sailing", 37.800, -122.468, ['muir_sfo'], """
Off the end of the bridge we're driving through the Presidio, a military base for 219 years. The Spanish founded it in 1776, the same year as the American Declaration of Independence, then it passed to Mexico, then to the US Army in 1848, and in 1994 to the National Park Service. Lucasfilm now has its headquarters here. And the road you're on, the Presidio Parkway, replaced an old viaduct that wasn't safe in an earthquake. It cost 1.1 billion dollars, and the tunnels have a 14-acre park on their roof called Presidio Tunnel Tops.

Down on the water is where the 2013 America's Cup was raced, in giant foiling catamarans that averaged about 30 knots and topped 40, as much as twice the speed of the wind. Quiz, sports fans: in a first to nine wins, Emirates Team New Zealand led Oracle Team USA 8 to 1. What happened next? [[pause 5]] Oracle won eight races in a row and kept the Cup! One of the greatest comebacks in sport, right there in the bay.
""", ['Presidio_of_San_Francisco', '2013_America%27s_Cup'], priority=4, category='sport'),

clip('golden_gate_park', 'Golden Gate Park and the world’s weirdest race', 37.7695, -122.4769, ['muir_sfo'], """
Nineteenth Avenue runs right through Golden Gate Park: 1,017 acres and about 24 million visitors a year. It was built from the 1870s on the Outside Lands, and three-quarters of it was sand dunes. Engineer William Hammond Hall and gardener John McLaren spent years planting grass and trees to hold the sand in place. At the ocean end there are two Dutch-style windmills from 1903 that used to pump water around the park.

And this is where one of the world's weirdest races finishes. Bay to Breakers started on New Year's Day 1912, to show the rest of the country, buried in snow, that San Francisco was sunny. It runs 7.46 miles from near the bay to the breakers on Ocean Beach, finishing at the Great Highway, just past this park. People run it in fancy dress. In 1986 it set a Guinness world record as the biggest footrace on Earth, with 110,000 runners. Fancy-dress ideas for the three of you, if you ever enter, are welcome.
""", ['Golden_Gate_Park', 'Bay_to_Breakers'], category='sport'),

clip('sf_story', 'San Francisco: Gold Rush ships to the richest city in America', 37.757, -122.4765, ['muir_sfo'], """
Welcome to San Francisco, Julia's home turf. A bit of its story, by the numbers.

1847: the town was a little trading post called Yerba Buena, with about 459 people. That January, its American mayor renamed it San Francisco, partly because General Vallejo was planning a town called Francisca after his wife. San Francisco grabbed the name, so Vallejo's town became Benicia.

1848 to 1849: the Gold Rush. From about 1,000 people to 25,000 in under two years. Ships' crews deserted to go dig for gold, leaving around 500 empty ships in the harbour. Some became warehouses, saloons and hotels, and some were deliberately sunk to claim the underwater land. Then the cove was filled in, so parts of downtown sit on top of Gold Rush ships.

1873: the first cable cars climb Clay Street.

And 2024: San Francisco's economy was worth 268 billion dollars, about 324,000 dollars per person. That's the highest per-capita output of any big American city. Adam, there's your economics stat of the day.
""", ['San_Francisco'], priority=4, category='economics'),

clip('delivery_wars', 'Mike’s corner: the delivery wars', 37.736, -122.4755, ['muir_sfo'], """
Mike, this one's for you. You're driving through the home turf of your biggest rivals.

In January 2013, four Stanford students launched a site called PaloAltoDelivery.com, down the Peninsula in Palo Alto. That summer, the startup accelerator Y Combinator gave them 120,000 dollars for seven percent of the company, and they renamed it DoorDash. Today DoorDash has 56 percent of the American food delivery market, it entered the Fortune 500 in 2024, and through Deliveroo and Wolt it now operates all over Europe, including, of course, the UK.

Meanwhile, from your side of the Atlantic: in 2020, Just Eat Takeaway agreed to buy Grubhub, one of DoorDash's American rivals, in a deal valuing it at 7.3 billion dollars. In November 2024 it sold Grubhub to Wonder Group for 650 million dollars. And in October 2025, Just Eat Takeaway itself was bought by the investment firm Prosus.

I won't ask you to comment on that while driving. But the floor is open: who wins the delivery wars?
""", ['DoorDash', 'Just_Eat_Takeaway'], priority=4, category='economics'),

clip('sf_1906_story', '5:12 a.m., April 18, 1906', 37.725, -122.472, [], """
Story time: the morning San Francisco fell down. At 5:12 a.m. on the 18th of April, 1906, the San Andreas Fault ruptured along about 280 miles of coast, the same fault we followed past Tomales Bay and Bolinas this morning. A foreshock first, then about 42 seconds of violent shaking. Magnitude about 7.9.

Then came the fires, burning for days. More than 3,000 people died, the deadliest earthquake in American history, and over 80 percent of the city was destroyed. At the time, San Francisco was the biggest city on the West Coast.

Remember all the places it touched today: refugees opening businesses in Stinson Beach, Petaluma becoming the relief base, redwoods logged to rebuild the city. And the epicenter is now thought to have been just offshore from Mussel Rock, by Daly City, which is coming up next.
""", ['1906_San_Francisco_earthquake', 'San_Andreas_Fault', 'Daly_City,_California'], priority=4, category='history', kind='story', radius=6000),

clip('daly_city', 'Daly City: little boxes on the hillside', 37.706, -122.469, ['muir_sfo'], """
We're crossing into Daly City. After the 1906 earthquake, thousands of homeless San Franciscans headed south to the ranches here, including one belonging to John Daly, a dairyman who had married his boss's daughter. The town grew out of those refugees and took his name.

From the late 1940s, developer Henry Doelger built Westlake, one of the first big planned suburbs, with rows and rows of near-identical houses up the hills. It inspired Malvina Reynolds' 1962 folk song Little Boxes, which pokes fun at exactly that.

And a sadder side: Filipino American families who wanted to buy here in the 1950s were barred from Westlake by racial covenants, so they bought homes east of Junipero Serra Boulevard instead.
""", ['Daly_City,_California'], category='culture'),

clip('colma', 'Colma: where the dead outnumber the living', 37.680, -122.455, ['muir_sfo'], """
Here's the strangest town of the whole trip: Colma. Most of its land is cemeteries.

In 1900, San Francisco banned new burials in the city, and in 1912 it evicted most of its existing cemeteries. About 150,000 bodies were dug up and moved down here, at ten dollars per grave. Nearly everyone famous who died in San Francisco ended up here.

Quiz: the dead here outnumber the living. By roughly how much? [[pause 5]] About a thousand to one! There are around one and a half million people buried in Colma. It's been called the City of the Silent, and its unofficial motto is: It's great to be alive in Colma.
""", ['Colma,_California'], priority=3, category='culture'),

clip('san_andreas_lake', 'San Andreas Lake: Yosemite in your tap', 37.630, -122.430, ['muir_sfo'], """
Off to the right, just south of here, is San Andreas Lake, the lake in the valley that gave the San Andreas Fault its name. The fault runs straight down it, and its earth dam, built in 1868, sits right on top of the fault. It survived 1906.

It's also part of one of the great feats of American water engineering. Julia, your tap water in San Francisco comes from Yosemite. The Hetch Hetchy Valley was dammed under a law passed in 1913, the Raker Act, after a huge political fight. John Muir was against it, and William Kent of Muir Woods supported it, which ended their friendship. Today, the Hetch Hetchy system sends water 167 miles across the Central Valley, and supplies 80 percent of the water for 2.6 million people.

And the water is so clean, from bare Sierra granite, that San Francisco is one of only six American cities not required by law to filter its tap water. The dam also makes hydropower, which the city sold to PG&E, leading to decades of legal battles.
""", ['San_Andreas_Lake', 'Hetch_Hetchy', 'San_Andreas_Fault', 'Muir_Woods_National_Monument'], priority=3, category='infrastructure'),

clip('sweeney_ridge', 'Discovering San Francisco Bay', 37.640, -122.455, ['muir_sfo'], """
On the hills to the west is Sweeney Ridge, where Europeans first laid eyes on San Francisco Bay.

In 1769, a Spanish expedition under Gaspar de Portolá was heading up the coast. Portolá sent scouts under Sergeant José Ortega north to find the Point Reyes headlands, which we drove past this morning. Ortega came back and said he couldn't get there, because the Golden Gate was in the way. And from Sweeney Ridge, on the 4th of November 1769, the expedition saw San Francisco Bay, although the scouts had spotted it a few days before.

Think about that. Drake in 1579 and Vizcaíno in 1603 sailed right past one of the greatest harbours on Earth and never noticed it, hidden behind the fog.
""", ['Sweeney_Ridge', 'Golden_Gate', 'New_Albion', 'Point_Reyes_National_Seashore'], category='history'),

clip('sfo', 'SFO: from cow pasture to the world', 37.6213, -122.3790, ['muir_sfo'], """
And here we are: San Francisco International. Last quiz of the trip: when the city opened its airport here in May 1927, what was the land being used for? [[pause 4]] It was a cow pasture! 150 acres, leased from the Mills family as a temporary, experimental airfield called Mills Field. The city bought it in 1931, and the word International was added after World War Two. Funny detail: it's owned by San Francisco, but it's actually in San Mateo County.

So, Mike, Adam, Julia: that's a wrap! From the Gold Rush and Napa's vineyards to the Russian River, the Sonoma Coast, Point Reyes, the redwoods and the Golden Gate. Earthquakes, fusion, floating wind, delivery wars, and a town where the dead outnumber the living. It's been an honour being your guide. Safe flight, come back soon, and remember: Goonies never say die!
""", ['San_Francisco_International_Airport'], priority=5, category='history'),
]

def write(path, area_id, area_name, clips):
    json.dump({'area': {'id': area_id, 'name': area_name}, 'clips': clips}, open(path, 'w'), indent=1, ensure_ascii=False)
    print(path, len(clips), 'clips,', sum('[[pause' in c['text'] for c in clips), 'with a quiz')

write('content/11_sonoma_coast.json', 'sonomacoast', 'Russian River mouth & Sonoma Coast', sonoma_coast)
write('content/12_west_marin.json', 'westmarin', 'Tomales Bay, Point Reyes & Stinson Beach', west_marin)
write('content/13_golden_gate.json', 'goldengate', 'Mount Tam, Muir Woods, Golden Gate & San Francisco', marin_sf)

# Existing clips that also belong on the new roads.
add = {'content/03_russian_river.json': {'bohemian_grove': ['sr116_coast'], 'pomo_story': ['sr116_coast']},
       'content/08_west_county.json': {'coast_miwok_story': ['sr1_coast', 'valley_ford_101']},
       'content/10_stories.json': {'russians_story': ['sr116_coast', 'sr1_coast']}}
for path, m in add.items():
    doc = json.load(open(path))
    for c in doc['clips']:
        if c['id'] in m: c['roads'] = list(dict.fromkeys(c['roads'] + m[c['id']]))
    json.dump(doc, open(path, 'w'), indent=1, ensure_ascii=False)
