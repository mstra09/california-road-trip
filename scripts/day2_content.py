"""Day 2 content (Guerneville -> Jenner -> Bodega Bay -> West Marin / Petaluma -> Muir Woods -> Golden Gate -> SFO).
Writes content/11_sonoma_coast.json, 12_west_marin.json, 13_golden_gate.json. Every fact comes from the listed sources."""
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
Good morning, road-trippers! Julia, Adam, our heroic driver: welcome to day two. And what a day. We're following the Russian River all the way to the ocean. Then it's down the wild Sonoma Coast to Bodega Bay, where Alfred Hitchcock made birds terrifying. After that, either along Tomales Bay and the Point Reyes coast, or inland through Petaluma, to the giant redwoods of Muir Woods. Then over the Golden Gate Bridge and through San Francisco to the airport.

Quick warm-up quiz while you finish your coffee. Today we're going to cross the biggest, most famous fault line in America, more than once. What's it called? [[pause 4]] The San Andreas Fault! And here's the wild bit: by this afternoon we'll have driven on a different tectonic plate. Some of the land we're passing is moving north at about an inch a year. More on that later. Let's go find the ocean!
""", ['Russian_River_(California)', 'San_Andreas_Fault', 'Bolinas,_California'], priority=5, category='geography', kind='intro'),

clip('duncans_mills', 'Monte Rio and Duncans Mills: the railroad to the redwoods', 38.4539, -123.0544, ['sr116_coast'], """
Picture this road with a little narrow-gauge train chugging along beside the river. From the 1870s, the North Pacific Coast Railroad ran from Cazadero, through Monte Rio and Duncans Mills, all the way down to the Sausalito ferry. And you'll hear its name again and again today, because it also stopped at Valley Ford, Tomales, Marshall and Point Reyes Station.

At first it hauled redwood lumber to build San Francisco. In 1877 Alexander Duncan set up a sawmill right here, and the town grew up around it, with two hotels, a saloon, a blacksmith and a livery stable. When the mills moved on, the trains started carrying San Franciscans up to summer cabins instead. Monte Rio, back there, branded itself Vacation Wonderland, and even had a seven-story hotel downtown. Parts of the 1942 Oscar-winning film Holiday Inn were shot at a resort in Monte Rio.

Quiz: the railroad shut down in the 1930s, and Duncans Mills slowly faded. Then, in 1976, something brought it back to life. What do you think? [[pause 5]] America's two-hundredth birthday! A Bicentennial restoration project fixed up the old buildings. And there's still an original depot here, with some of the old railroad cars.
""", ['Duncans_Mills,_California', 'Monte_Rio,_California'], category='history'),

clip('jenner', 'Jenner: the river meets the sea, and a pump made of gold', 38.4497, -123.1157, COAST, """
There it is! The Russian River meets the Pacific Ocean, right here at Jenner. Population: about a hundred and twenty.

Quick reminder of why it's called the Russian River. Russians from the Russian-American Company explored it in the early 1800s, when they set up Fort Ross, about ten miles up the coast. They called it the Slavyanka. The Pomo had much older names for it, including Bidapte, big river.

The town is named after Dr. Elijah Jenner, a dentist and inventor from Vermont who came west for the Gold Rush in 1850. While he was mining, he designed a pump that could lift water a hundred feet. Quiz: when he applied for the patent, he sent a model of the pump. What was so special about it? [[pause 5]] It was made of pure gold! It's the only golden model the Patent Office has ever received. A true Gold Rush flex. By 1854 the family had settled here at the mouth of the river.

And watch the river mouth. In summer, the waves build a sandbar right across it, and the river turns into a lagoon until the water gets high enough to break through. In late fall and winter, when the sandbar's breached, the sheltered beach on the north side is a favourite spot for harbor seals to have their pups.
""", ['Jenner,_California', 'Russian_River_(California)', 'Goat_Rock_Beach'], priority=4, category='history'),

clip('goat_rock', 'Goat Rock: sea stacks, mammoths and the Goonies', 38.4405, -123.1180, SR1, """
Okay, movie quiz! Down on the left is Goat Rock Beach, with that huge flat-topped rock barely hanging on to the land. In 1985, a very famous adventure movie, about a group of kids hunting for pirate treasure, filmed its ending on this beach. Which movie? [[pause 5]] The Goonies! Goonies never say die.

Now look at all those rocks sticking out of the sea. They're called sea stacks, and here's how they got there. For about 170 million years, an ocean plate was diving under North America. It scraped off pillow lava, chert and sandstone, and crushed it all into mélange, which is a jumble of hard blocks floating in a softer, ground-up rock. When the waves hit it, the soft stuff washes away and the hard blocks are left standing in the sea. Goat Rock is one big hard block of greywacke sandstone.

And here's a cool one. About a mile south of the river there's a rock of blueschist with rubbing marks two to four meters up. That's too high for cows. Scientists think mammoths made them, using it as a back-scratcher! Mammoths are believed to have roamed here as recently as 40,000 years ago.

Careful if you stop, though: the beach drops off steeply and there's a nasty rip current.
""", ['Goat_Rock_Beach', 'Sonoma_Coast_State_Park', 'Bodega_Bay,_California'], priority=4, category='geology'),

clip('sonoma_coast', 'Seventeen miles of wild coast', 38.389, -123.087, SR1, """
This is the Sonoma Coast, seventeen miles of state beaches running all the way down to Bodega Head. Little coves, big rocks, cliffs, and fog that can roll in fast.

Quiz: those bluffs are made of soft soil, and the ocean's chewing away at them. How much land do you think this coast loses in an average year? [[pause 5]] One to three feet a year! More in a stormy winter. It's also rising. Over the ages this land has been pushed up, which is why you're driving on a flat shelf above the beach. It's called a marine terrace: old sea floor, lifted up. Some of those sea stacks are even standing up on the terrace, away from the water, because they started life on the sea floor before it rose.

Look out to sea for gray whales, harbor seals and California sea lions. The Coast Miwok and Pomo lived along here for a very long time, and dozens of their old shell middens, basically ancient kitchen garbage heaps, have been found on this coast. The Russians cut down the old-growth forest above the coastal prairie in the early 1800s, and later it became part of a Mexican ranch called Rancho Bodega.
""", ['Sonoma_Coast_State_Park', 'Goat_Rock_Beach'], category='geography'),

clip('bodega_bay', 'Bodega Bay: Russians, Spaniards and a lot of movies', 38.3333, -123.0481, SR1, """
Welcome to Bodega Bay! Fishing boats, salty air, and a harbor tucked behind that long headland.

The bay is named after Juan Francisco de la Bodega y Quadra, a Spanish naval officer who sailed in here in 1775. In 1793 the Spanish sent a little garrison with four cannons, because they'd heard the English might show up. They didn't, so the guns went back to Monterey. And then guess who did show up? The Russians! In 1809, before they built Fort Ross, they put up the first Russian buildings in California here, and called it Port Rumyantsev, after their foreign minister.

Hollywood loves this town. Hitchcock filmed The Birds here, which I'll tell you about in a second. But there's also The Fog, I Know What You Did Last Summer, and The Russians Are Coming, the Russians Are Coming. Quiz: in 2021, a famous TV comedy needed to film a season in Ireland, but COVID made that impossible. So Bodega Bay played Ireland instead! Which show? [[pause 5]] It's Always Sunny in Philadelphia! A Northern California fishing village pretending to be Ireland. Honestly, with the fog, it works.
""", ['Bodega_Bay,_California', 'Bodega,_California'], priority=4, category='history'),

clip('the_birds', 'The Birds: Hitchcock terrorises Bodega Bay', 38.326, -123.040, SR1, """
Okay, The Birds! In 1963, Alfred Hitchcock made a horror film about birds suddenly, inexplicably attacking the people of Bodega Bay. Tippi Hedren, in her first film, plays a San Francisco socialite who drives up here with a pair of lovebirds, and things go very badly. Gulls at the dock, crows at the schoolhouse, sparrows pouring down the chimney.

Quiz: Hitchcock was partly inspired by a real event in 1961, when thousands of seabirds dive-bombed a California seaside town called Capitola, crashing into cars and dropping half-eaten fish on people's lawns. Gross. What do you think really caused it? [[pause 5]] Toxic algae! It poisoned the birds. But nobody knew that in the 1960s.

And most of the birds in the movie are real. The gulls were caught at the San Francisco garbage dump. Some of the crows were actually ravens. There were 370 special-effects shots, and the final shot was built out of 32 separate pieces.

The film was shot around two places, Bodega Bay and the inland village of Bodega, edited to look like one town. The church and the schoolhouse are just up the road in Bodega. A darker footnote: decades later, Tippi Hedren said Hitchcock harassed her during the filming. Today the film's considered one of the greatest horror movies ever made.
""", ['The_Birds_(film)', 'Bodega_Bay,_California'], priority=4, category='culture'),

clip('hole_in_the_head', 'The Hole in the Head: the nuclear plant that never was', 38.3215, -123.035, SR1, """
Across the harbor is Bodega Head, and it has a hole in it. Literally. Here's the story.

In the late 1950s and early 60s, the utility company PG&E planned to build a nuclear power plant on Bodega Head. It was meant to be the first commercially viable nuclear plant in the United States. The fishermen were worried about their livelihoods. And a local woman, Rose Gaffney, who owned land on the headland, refused to sell, sued the company, and invited government officials to come and see the fault lines on the site for themselves.

Quiz: in June 1963, the protesters released 1,500 of something into the air with a warning message attached. What? [[pause 4]] Helium balloons! The message said each one could represent a radioactive molecule of strontium 90 or iodine 131. In 1964, after a negative review by the Atomic Energy Commission, PG&E gave up. Historians call it the birth of the anti-nuclear movement.

And the real clincher: the San Andreas Fault runs right between Bodega Head and the mainland. Bodega Head is on the Pacific Plate, the town's on the North American Plate. In the 1906 earthquake, the headland jumped about fifteen feet. Its rock is granite, related to the Sierra Nevada, carried north hundreds of miles along the fault. By then they'd already dug the pit for the reactor. It filled with water, and locals call it the Hole in the Head.
""", ['Bodega_Bay_Nuclear_Power_Plant', 'Bodega_Head', 'Bodega_Bay,_California'], priority=4, category='politics'),

clip('bodega', 'Bodega: rusty cannons and a famous schoolhouse', 38.3449, -122.9719, SR1, """
This little village is Bodega, once called Bodega Corners, to tell it apart from the port down by the water. There used to be two Coast Miwok villages in the area. Then the Russians settled in the Salmon Creek valley here in 1809.

Quiz: around 1843, John Sutter bought land from the departing Russians, including this area. What did the deal include? Guess one thing. [[pause 5]] Some hunting rights, a small boat, several rusty cannons and some old muskets! What a bargain.

In 1843 a Captain Stephen Smith also built the first lumber mill on the West Coast near here. Then the town proper began in 1853 with a saloon, a blacksmith and a hotel. Naturally. In 1859, shipbuilders built the Saint Teresa of Avila Church. And if both church and schoolhouse look familiar, that's because the church and schoolhouse in The Birds are right here on the Bodega Highway. That's the school where the crows gather on the jungle gym.

Geology note: the geology maps show the rock around here is the Wilson Grove Formation, from the late Miocene and Pliocene, very roughly ten to three million years ago. It's the same sea-floor sandstone we met back in Sebastopol.
""", ['Bodega,_California', 'Bodega_Bay,_California', 'The_Birds_(film)'], category='history', geo=(38.33041, -122.99587)),

clip('valley_ford', 'Valley Ford and the Running Fence', 38.3178, -122.9236, ['sr1_coast', 'valley_ford_101'], """
Tiny Valley Ford, population about a hundred and fifty. Dairy country: rolling green hills and cows.

The Coast Miwok had a village here called Ewapalt. In the 1850s there was a grain mill, and from 1876 the North Pacific Coast Railroad stopped here, so ranchers and fishers could ship their produce down to San Francisco.

Quiz: in 1976, a famous pair of artists, Christo and Jeanne-Claude, built a giant artwork that passed right through Valley Ford, running from Cotati all the way to Bodega Bay. What do you think it was? [[pause 5]] A fence! Running Fence: a long white fabric fence across the hills, all the way to the ocean.

Two more fun facts. If anyone in the car plays guitar: Shubb, the company that makes capos, has its headquarters right here. And a less fun fact: the dairies have put so much nitrate into the groundwater that in 2017 the state warned pregnant women and babies not to drink the town's well water, and some restaurants truck their water in from Petaluma.
""", ['Valley_Ford,_California'], category='culture'),
]

west_marin = [
clip('tomales', 'Tomales: into Marin County', 38.2470, -122.9050, SR1, """
Welcome to Marin County! And to Tomales, population just under two hundred, perched above Keys Creek.

The Coast Miwok had many villages around here, including one called Utumia, near the town. The post office opened in 1854, spelled Tomalles with two L's, and later it lost one. The North Pacific Coast Railroad came through in the 1870s.

Quiz: Tomales sits close to the San Andreas Fault. How can you still see the damage from the 1906 earthquake here? [[pause 5]] In the cemetery! One of the town's two cemeteries is older than the earthquake, and the old graves are still damaged. It shows how far the shaking reached.

Speaking of Marin: Vallejo, the general from yesterday in Sonoma, said the county was named after Marin, a Coast Miwok leader. More on him later.
""", ['Tomales,_California', 'Marin_County,_California'], category='history'),

clip('tomales_bay', 'Tomales Bay: the fault you can sail on', 38.205, -122.925, SR1, """
That long, skinny bay is Tomales Bay: about fifteen miles long, only a mile wide, and shallow, about eighteen feet deep on average. Quiz: in 1603, Spanish explorers from the Vizcaíno expedition found this bay. What did they think it was? [[pause 4]] A river! They called it the Rio Grande de San Sebastián. Easy mistake, look at it.

But it's not a river, it's a fault! Tomales Bay sits on a drowned stretch of the San Andreas Fault. Everything on the far side, the Point Reyes Peninsula, is on the Pacific Plate. You're on the North American Plate. The fault cuts through the peninsula, from Tomales Bay in the north to Bolinas Lagoon in the south, and we'll follow it nearly the whole way.

The Coast Miwok had villages all around the bay. Shells and clams from the bay's shore weren't just food: they were used as money. And just across the peninsula, the English captain Francis Drake is thought to have landed in 1579. That story's coming up.
""", ['Tomales_Bay', 'Point_Reyes_National_Seashore'], priority=4, category='geology'),

clip('marshall', 'Marshall: oysters and a creamery', 38.1617, -122.8930, SR1, """
This stretch of shoreline is Marshall, and if anyone's hungry, you're in luck: oysters!

The town is named after the Marshalls, four brothers who started dairy farming here in the 1850s. The railroad stopped here from the 1870s too. There's still some dairy, with the Straus Family Creamery based here. But these days the big business is oysters and clams.

Quiz: oyster farming is a major industry on Tomales Bay. Can you name either of the two biggest producers? I'll give you a hint: one of them is named after an animal. [[pause 5]] Hog Island Oyster Company, and Tomales Bay Oyster Company! Both sell to the public, and both have picnic grounds on this east shore. If you stop, the classic move is a bag of oysters at a picnic table by the water.

The cows on the hills across the bay graze on ranches leased from Point Reyes National Seashore, and that's a whole controversy for another day.
""", ['Marshall,_California', 'Tomales_Bay'], category='food'),

clip('point_reyes_station', 'Point Reyes Station: the town that changed its name three times in a year', 38.0693, -122.8068, SR1, """
Welcome to Point Reyes Station, the little hub town for the Point Reyes peninsula.

It started as the railroad's terminus stop. When the trains arrived in 1875 it was called Olema Station. Quiz: in 1891 alone, how many times did the town's name change? [[pause 4]] Three times! First to Marin, then back to Point Reyes, then finally to Point Reyes Station. Make up your mind!

Fun fact: it used to be a real port on Tomales Bay. But cattle and European grasses caused erosion, and silt, little dams and landfill for farming raised up the old salt marshes. Now the town is nearly a mile from the nearest tidal flats.

And it sits just east of the San Andreas Fault. Over at the Bear Valley Visitor Center, near Olema, there's the Earthquake Trail, where you can see a rift left by the 1906 earthquake.
""", ['Point_Reyes_Station,_California', 'Tomales_Bay'], category='history'),

clip('olema', 'Olema: coyote valley and the hippie song', 38.0410, -122.7886, SR1, """
This crossroads is Olema. Quiz: the name comes from a Coast Miwok place name. It's an animal, plus valley. Which animal? [[pause 4]] Coyote! Olema means coyote valley.

For years people believed Olema was the epicenter of the great 1906 earthquake, because the ground nearby moved so much. The rifts are still visible on a hiking path. Modern research points to an epicenter offshore, near Daly City, which we'll drive through this afternoon.

A bit of music history: Olema got its own song in the late 1960s, Hippie from Olema, by The Youngbloods, a cheeky reply to Merle Haggard's Okie from Muskogee.

And just up Bear Valley Road, a quarter mile from town, is the visitor center for Point Reyes National Seashore, with Kule Loklo, a reconstructed Coast Miwok village. The Coast Miwok's descendants formed the Federated Indians of Graton Rancheria, which won federal recognition in 2000, and they hold ceremonies at Kule Loklo.
""", ['Olema,_California', '1906_San_Francisco_earthquake', 'Point_Reyes'], category='culture'),

clip('drake_story', 'Francis Drake, New Albion and the porcelain clue', 38.10, -122.87, SR1, """
Okay, story time. On the 17th of June, 1579, the English sea captain Francis Drake sailed into a sheltered cove just over those hills. His ship, the Golden Hind, needed repairs. He'd spent months raiding Spanish towns and treasure ships along the Pacific coast, and he was about to sail home the long way, right round the world.

He stayed about five weeks, and got on well with the Coast Miwok who lived here. He named the land New Albion, partly because the white cliffs reminded him of England, and claimed it for Queen Elizabeth the First. He nailed up a brass plate with a sixpence showing the Queen's face. Then on the 23rd of July he sailed away, without leaving a colony, and got back to England in September 1580.

People argued about exactly where he landed for centuries. Quiz: one of the best clues came from archaeologists. Nearly a hundred pieces of something were found near the cove, which had to have come from Drake. What do you think? [[pause 6]] Chinese porcelain! Broken dishes that Drake had taken from a Spanish treasure ship and dumped here while lightening his ship for repairs. In 2021 California officially named Drake's Cove, inside Point Reyes National Seashore, as the site of New Albion.

And the name Point Reyes? On the 6th of January 1603, Sebastián Vizcaíno sighted the headland on Three Kings' Day, so he called it la Punta de los Reyes, the Point of the Kings.
""", ['New_Albion', 'Point_Reyes_National_Seashore', 'Point_Reyes'], priority=4, category='history', kind='story', radius=20000),

clip('point_reyes_wild_story', 'Point Reyes: elk, elephant seals and the foggiest lighthouse', 38.03, -122.82, SR1, """
Out there on the Point Reyes peninsula is one of the wildest corners of California. A congressman named Clem Miller wrote the bill in 1962 to protect it, because developers wanted to build on the slopes above Drakes Bay. Now about half of it is wilderness.

Quiz: when Europeans arrived, there were maybe half a million tule elk in California. By the 1870s, people thought they were extinct. How many do you think were found, hiding in a marsh in the Central Valley? [[pause 5]] One breeding pair! Just two! Genetic studies fit the idea that today's tule elk all descend from that tiny group. In 1978, ten were brought to Tomales Point here, and after a rough start, from 1981 they were breeding at full speed.

Then the elephant seals came back too. They started a breeding colony in 1981. And here's my favourite: in January 2019, during a government shutdown, with no rangers working, the elephant seals moved onto Drakes Beach and had their pups. In the parking lot!

And at the very end of the point is the Point Reyes Lighthouse, first lit in 1870. Official records call it the windiest and foggiest spot on the Pacific Coast, with gales up to a hundred miles an hour. Quiz: most lighthouses are built up high so ships can see them from far away. This one is built low, down a cliff, at the bottom of about three hundred steps. Why? [[pause 5]] To get the light below the fog! Up top it would just disappear into the clouds.
""", ['Point_Reyes_National_Seashore', 'Tule_elk', 'Point_Reyes_Lighthouse'], priority=3, category='nature', kind='story', radius=20000),

clip('san_andreas_story', 'Riding the San Andreas Fault', 38.00, -122.76, ['sr1_coast', 'muir_sfo'], """
Right now we're driving almost exactly along the San Andreas Fault. This straight valley, with Olema Creek, is the fault zone. To the north it sinks under Tomales Bay; to the south it runs under Bolinas Lagoon. Then it heads out to sea and comes back on land near Daly City.

The fault runs about 750 miles through California. It's where two plates slide past each other. Quiz: the Pacific Plate, on your right, is moving north compared to the North American Plate. Roughly how fast? [[pause 5]] About an inch a year. But it doesn't slide smoothly. It sticks, builds up strain for decades, and then lets go all at once. In 1906, the ground along the fault shifted by up to twenty feet.

After the 1906 earthquake, a Berkeley professor, Andrew Lawson, mapped all the fences and roads that had been sliced in half and shifted. They made an almost perfect line, right along a fault he'd found in 1895. He named it after the San Andreas Valley, down the peninsula. And that rock on the far side, the granite of Point Reyes and Bodega Head, is related to the Sierra Nevada. It's been carried hundreds of miles north along this fault.
""", ['San_Andreas_Fault', '1906_San_Francisco_earthquake', 'Point_Reyes_National_Seashore', 'Bodega_Head', 'Bolinas,_California'], priority=4, category='geology', kind='story', radius=25000),

clip('bolinas', "Bolinas: the town that doesn't want to be found", 37.935, -122.695, SR1, """
Somewhere off to the right, across the lagoon, is Bolinas. You probably won't see a sign for it. Quiz: why not? [[pause 4]] Because the locals keep tearing them down! Every sign on Highway 1 pointing the way to Bolinas has been removed by residents. The county even put it to a vote, and the voters said, no more signs, thank you.

It's a famously reclusive little town, about fourteen hundred people. And it has a fun real-estate story. In 1927 an old dairy farm on the mesa was divided into more than five thousand tiny lots, and a San Francisco newspaper sold a lot of them for 69 dollars and fifty cents each, as a promotion for subscriptions. Buy the paper, get some land! Some of those streets have since fallen into the sea.

This is Bolinas Lagoon, a tidal estuary on the official list of wetlands of international importance. And yes, the San Andreas Fault runs right down the middle of it. Bolinas, over there, is on the Pacific Plate, sliding north from Stinson Beach at about an inch a year.
""", ['Bolinas,_California', 'Bolinas_Lagoon'], category='culture'),

clip('stinson_beach', 'Stinson Beach and the craziest race in America', 37.9007, -122.6443, SR1, """
Stinson Beach! A long, sandy beach that San Franciscans have been escaping to for about 150 years.

It started as Willow Camp, a tent settlement among the willows after the first coast road was built in 1870. After the 1906 earthquake, refugees from San Francisco came out and opened some of the first businesses, and in 1916 it was renamed after the biggest landowners, Rose and Nathan Stinson.

Now: the Dipsea. Since 1905, runners have raced from Mill Valley, over the shoulder of Mount Tam, down to Stinson Beach. It's seven and a half miles with about 2,200 feet of climbing, and it's the oldest trail race in America. Runners can take shortcuts with names like Suicide and the Swoop. And older and younger runners get a head start of up to 25 minutes. Quiz: because of that handicap system, how young do you think the youngest winner was? [[pause 5]] Eight years old! And winners have been as old as seventy-two. Jack Kirk, the Dipsea Demon, ran 67 Dipseas in a row, and started his last one at 96.

One word of warning: the water off here is in the Red Triangle, an area with unusually many great white shark attacks.
""", ['Stinson_Beach,_California', 'Dipsea_Race', 'Bodega_Head'], priority=4, category='culture'),
]

marin_sf = [
clip('mount_tam', 'Mount Tam: the crookedest railroad and the first mountain bikes', 37.8867, -122.6236, TAM, """
The big mountain above us is Mount Tamalpais, Mount Tam to the locals, 2,571 feet at the East Peak.

Quiz: you might hear that Tamalpais means Sleeping Maiden, after a Miwok legend about the mountain's profile looking like a sleeping girl. True or false? [[pause 4]] False! That legend was made up in Victorian times, by a playwright for a play at the mountain's outdoor theatre. The name actually comes from the Coast Miwok támal pájis, meaning west hill.

From 1896 to 1930 a railroad wound up from Mill Valley to the summit, with so many bends it was nicknamed the Crookedest Railroad in the World. And in the 1970s, this mountain gave the world something new: the mountain bike. Riders bolted fat tires and better brakes onto old 1930s and 40s Schwinn bikes and bombed down the fire roads. Quiz: they held downhill races near Fairfax called the Repack races. Why Repack? [[pause 5]] Because the coaster brakes got so hot on the way down that the grease burned, and riders had to repack their wheel bearings after every race! Gary Fisher, Charlie Kelly and Joe Breeze were among the pioneers riding here.
""", ['Mount_Tamalpais', 'Mountain_biking'], priority=3, category='culture'),

clip('muir_woods', 'Muir Woods: the man who gave away a forest', 37.8935, -122.5774, TAM, """
Welcome to Muir Woods, one of the last old-growth redwood forests in the Bay Area. It's a narrow canyon on the slope of Mount Tam, wrapped in summer fog, which these trees drink up during the dry season.

Here's how it survived. Mount Tam's redwoods were logged heavily to build San Francisco, and again to rebuild it after 1906. But the trees in this canyon, then called Redwood Canyon, were too hard to reach. In 1905, William Kent and his wife Elizabeth bought 611 acres of it for 45,000 dollars, with money borrowed from a banker friend, to save it. Then a water company tried to take part of it to build a dam and a reservoir. So Kent used a brand-new law, the Antiquities Act, and offered to donate the land to the nation. President Theodore Roosevelt accepted, and in January 1908 it became a national monument.

Quiz: the name first suggested was the Kent Monument. What did Kent want instead? [[pause 4]] He insisted it be named after John Muir, the great naturalist! And the twist: Kent and Muir later fell out over damming the Hetch Hetchy valley, which Kent supported. Kent went on to Congress and sponsored the law creating the National Park Service in 1916. He was also, honestly, a loud supporter of anti-Asian immigration laws, so he's a complicated hero.

The tallest tree here is 258 feet, most are 500 to 800 years old, and the oldest is at least 1,200. Quiz: how big is the seed a redwood grows from? [[pause 4]] About the size of a tomato seed! Tiny seed, giant tree.
""", ['Muir_Woods_National_Monument', 'William_Kent_(American_politician)'], priority=5, category='nature',
 more=('Muir Woods and the founding of the United Nations', """
One more Muir Woods story. In April 1945, delegates from 50 countries gathered in San Francisco to write the Charter of the United Nations. President Franklin Roosevelt was supposed to open the conference, but he died on the 12th of April, just before it started. So on the 19th of May, the delegates came out here to Cathedral Grove and held a ceremony in his memory, among the redwoods, and placed a plaque in his honor. It's still there.

And a practical note: Muir Woods gets up to six thousand visitors a day at busy times, and parking is so limited that since 2018 you need a reservation to park or take the shuttle.
""", ['Muir_Woods_National_Monument'])),

clip('redwoods_story', 'Coast redwoods: the tallest living things on Earth', 37.89, -122.60, ['sr1_coast', 'valley_ford_101', 'muir_sfo', 'sr116_coast'], """
Let's talk about the coast redwood, Sequoia sempervirens. Quiz: how tall do you think the tallest living redwood is? [[pause 5]] About 381 feet! That's the tallest living tree on Earth, way up in Humboldt County. They can live about 2,000 years, and the trunks can be 29 feet across.

Redwoods have been around a very long time. Their relatives' fossils go back to the age of the dinosaurs. They only grow in a narrow strip along the coast, from Big Sur up to the corner of Oregon, because they need that fog. In the dry summers, they drink moisture straight out of the fog.

Before the Gold Rush, they covered about two million acres. Then the logging started, to build San Francisco and the towns all around it, including the Russian River towns we left this morning. Today only about 5 percent of the old-growth forest is left. The tallest and oldest trees survived in deep, steep canyons, partly because loggers simply couldn't get to them. That's exactly how Muir Woods made it.
""", ['Sequoia_sempervirens', 'Muir_Woods_National_Monument'], priority=3, category='nature', kind='story', radius=15000),

clip('petaluma', 'Petaluma: the Egg Capital of the World', 38.2330, -122.6400, ['valley_ford_101'], """
Welcome to Petaluma! Quiz: Petaluma's old nickname was the Egg Capital of the World. And it had another nickname, a pun on the name. Can you guess it? [[pause 5]] Chickaluma! This town was all about chickens. It had the only known poultry drugstore, a pharmacy for chickens. And in 1879, Lyman Byce invented the coal-lamp egg incubator here. They still celebrate with a Butter and Eggs Day parade.

The land was part of Rancho Petaluma, given in 1834 to our old friend General Vallejo from Sonoma. In 1836 he built a huge adobe ranch house just east of town, the largest privately owned adobe ever built in California. It's a state historic park now.

And here's a lucky break. In the 1906 earthquake, Petaluma was hardly damaged, thanks to stable bedrock underneath. So it became the base for rescue and relief across the county. That's also why downtown still has old iron-front buildings and Victorian houses. During the Depression nobody had the money to knock them down, and later people moving out from San Francisco restored them.
""", ['Petaluma,_California', 'Rancho_Petaluma_Adobe'], priority=4, category='history'),

clip('chief_marin', 'Chief Marin and the naming of Marin County', 38.00, -122.535, ['valley_ford_101'], """
We're coming through San Rafael, the county seat of Marin. So who was Marin?

The Coast Miwok have lived in Marin for about 6,500 years, and more than 600 of their village sites have been found. According to General Vallejo, who chaired the committee that named California's counties in 1850, this county was named after Marin, a great Coast Miwok chief. His birth name was Huicmuse. He was baptized Marino at about the age of twenty, in 1801, and lived at Mission Dolores in San Francisco for years, often serving as godfather at baptisms. Vallejo believed he'd fought fierce battles against the Spanish.

Quiz: there's a rival theory for the county's name, involving the bay. What do you think? [[pause 5]] In 1775 the Spanish named the bay here Bahía de Nuestra Señora del Rosario la Marinera, and Marin might just be short for that! Personally I'm going with the chief.

And a movie fact: before moving to the Presidio in San Francisco, George Lucas's company Lucasfilm had its headquarters here in San Rafael.
""", ['Marin_County,_California', 'Mill_Valley,_California', 'Presidio_of_San_Francisco'], category='history'),

clip('mill_valley', 'Mill Valley, Chief Marin and the Blind Pig', 37.8800, -122.5200, ['muir_sfo', 'valley_ford_101'], """
This junction, where Highway 1 meets 101, is at the edge of Mill Valley, the town tucked into the redwood canyons on the side of Mount Tam.

People have lived here a very long time. Fourteen Coast Miwok village sites have been found in the Mill Valley area, with huge shell mounds along Richardson Bay. One mound, excavated in 1907, was twenty feet high. And a plaque in a Mill Valley sidewalk marks the spot believed to be the birthplace of Chief Marin, in 1781.

Quiz: right around this intersection, in 1916, a roadhouse was built that became famous during Prohibition. It was called the Blind Pig. Why do you think it was built here, outside the town? [[pause 5]] Because it was outside the dry laws, which were enforced more strictly inside the city itself. The roadhouses around here were known as gin joints, and worse.

Mill Valley's also where the Dipsea Race starts, and where the Crookedest Railroad began its climb up Mount Tam.
""", ['Mill_Valley,_California', 'Dipsea_Race', 'Mount_Tamalpais'], category='history'),

clip('sausalito', 'Sausalito: streets under the bay', 37.858, -122.500, ['muir_sfo'], """
Down to the left is Sausalito, on Richardson Bay. The name is Spanish for small willow grove, and it's been spelled about a dozen different ways over the years.

Before the bridge, Sausalito was the end of the line: trains from up north, including that North Pacific Coast Railroad from the Russian River, met the ferries here. The car ferry to San Francisco took about twenty minutes and cost a dollar per car. In World War Two it became a shipbuilding center, and afterwards it turned arty and wealthy, famous for its houseboats.

Quiz: when Sausalito was laid out, planners assumed the town would one day expand by filling in the bay, like San Francisco did. So what's strange about some of Sausalito's streets? [[pause 5]] They're underwater! Streets with names like Pescadero, Eureka and Teutonia were mapped out but are still under Richardson Bay. More than a fifth of the city is water.
""", ['Sausalito,_California', 'Golden_Gate_Bridge'], category='history'),

clip('marin_headlands', 'The Marin Headlands: the city that never got built', 37.840, -122.486, ['muir_sfo'], """
Those wild green hills on your right, at the very tip of Marin, are the Marin Headlands. They look untouched, but they came close to being a city.

Quiz: in the 1960s, the government sold more than 2,000 acres here to a developer who planned a whole new city called Marincello. How many people do you think it was meant for? [[pause 5]] 30,000! In 50 apartment towers, with houses, a shopping center and a hotel. In 1970 the developer lost a lawsuit, and the land was sold to the Golden Gate National Recreation Area instead. Phew.

The headlands are dotted with old forts and gun batteries from the 1890s through World War Two, all built to keep enemy ships out of the bay, plus a Nike missile site from the Cold War.

And Hawk Hill, 920 feet up, is the best place in the Pacific states to watch birds of prey. Every fall, tens of thousands of hawks, falcons, eagles and vultures funnel down the peninsula here, because they hate flying over water.
""", ['Marin_Headlands'], category='nature'),

clip('golden_gate_bridge', 'The Golden Gate Bridge', 37.8199, -122.4783, ['muir_sfo'], """
Here it is, everybody! The Golden Gate Bridge! Cameras up, passengers!

It opened in 1937, and at that point it was the longest and tallest suspension bridge in the world. The towers are 746 feet tall, and the main span is 4,200 feet. Lots of experts said it couldn't be built, because of the wind, the fog, and the swirling tides.

Quiz: the colour is called International Orange, chosen by the architect Irving Morrow. But the U.S. Navy had a different suggestion, to make it more visible to ships. What do you think the Navy wanted? [[pause 5]] Black and yellow stripes! Like a giant bumblebee. Thank goodness for Morrow.

The chief engineer, Joseph Strauss, insisted on movable safety nets under the workers. Nineteen men were saved by those nets, and they formed a club, called the Half Way to Hell Club. Sadly eleven men did die, ten of them in a single accident in February 1937.

And the numbers are wild. The two main cables contain about 80,000 miles of steel wire, enough to go around the Earth three times. Each tower has about 600,000 rivets. And 38 painters work on it all year round.
""", ['Golden_Gate_Bridge'], priority=5, category='history',
 more=('Roller skates, bankers and a flattened bridge', """
A few more bridge stories. During the Depression, the bridge district couldn't sell its bonds to pay for construction. Then in 1932, Amadeo Giannini, the founder of Bank of America, bought the whole lot himself, to help the local economy.

The day before cars were allowed on it, in May 1937, 200,000 people walked across. Some on roller skates! And for the fiftieth birthday in 1987, they closed it to cars again. Up to a million people showed up, around 300,000 crammed onto the bridge at once, and the curve in the middle of the deck actually flattened out under their weight. Engineers say it was designed to flex like that, but they haven't tried it again since.

And the name of the strait came first. In 1846, John Frémont named it Chrysopylae, Golden Gate, after the Golden Horn harbor of Byzantium, as a golden gate to trade with Asia. The first Europeans known to sail through it were Juan de Ayala's crew, in 1775.
""", ['Golden_Gate_Bridge', 'Golden_Gate'])),

clip('presidio', 'The Presidio: from Spanish fort to Lucasfilm', 37.800, -122.468, ['muir_sfo'], """
Off the end of the bridge we're driving through the Presidio, a big wooded park that was a military base for 219 years.

The Spanish founded it on the 17th of September, 1776. That's the same year as the American Declaration of Independence, on the other side of the continent. Then it passed to Mexico, then in 1848 to the U.S. Army, and in 1994 the Army handed it to the National Park Service. Congress told the Presidio to pay for itself, and it did, eight years early.

Quiz: one of the Presidio's tenants makes some of the most famous movies in the world. George Lucas built his company's headquarters here, on the site of an old army hospital. Which company? [[pause 4]] Lucasfilm! Star Wars, from the Presidio.

And the road we're on is the Presidio Parkway. The old Doyle Drive viaduct here was judged unsafe in an earthquake, so it was replaced with tunnels through the bluffs, for 1.1 billion dollars, finished in 2015. On top of the tunnels they built a 14-acre park called Presidio Tunnel Tops. So right now, people may be having a picnic on the roof of your road.
""", ['Presidio_of_San_Francisco'], priority=4, category='history'),

clip('golden_gate_park', 'Golden Gate Park: a park built on sand dunes', 37.7695, -122.4769, ['muir_sfo'], """
Nineteenth Avenue cuts right through Golden Gate Park. It's 1,017 acres, and gets about 24 million visitors a year.

Quiz: before the park was built in the 1870s, what do you think covered three-quarters of this land? [[pause 4]] Sand dunes! This whole western side of the city was called the Outside Lands. Engineer William Hammond Hall and gardener John McLaren spent years planting grasses and trees to hold the sand in place. Hall later became California's first state engineer, and designed flood control for the Sacramento Valley, where this whole trip began.

At the ocean end there are two Dutch-style windmills from 1903, which used to pump water around the park. Inside there's the de Young Museum, the California Academy of Sciences and the Japanese Tea Garden. And the Outside Lands music festival borrows that old name.
""", ['Golden_Gate_Park'], category='history'),

clip('sf_story', 'Yerba Buena, the Gold Rush, and a city built on ships', 37.775, -122.472, [], """
Welcome to San Francisco! Quick question: was this city always called San Francisco? [[pause 4]] Nope! It was a little trading settlement called Yerba Buena, Spanish for good herb. In January 1847, the American mayor renamed it San Francisco, after the mission founded here in 1776. And here's a callback for you: one reason was that General Vallejo was planning a town called Francisca, after his wife. San Francisco grabbed the name first, so Vallejo's town became Benicia instead, after his wife's middle name.

In 1847 the town had about 459 people. Then gold was found, and it went from about 1,000 people in 1848 to 25,000 by December 1849. Ships arrived, and their crews deserted to go dig for gold, leaving a forest of empty masts in the harbor. Quiz: what happened to those roughly 500 abandoned ships? [[pause 5]] Some became warehouses, saloons and hotels. Many just rotted. And some were deliberately sunk, to claim the underwater land! Then the cove was filled in, so parts of downtown are literally built on top of Gold Rush ships.

The cable cars started climbing Clay Street in 1873. The Beats took over North Beach in the 1950s, hippies flocked to Haight-Ashbury for the 1967 Summer of Love, and the city's been a magnet for misfits and dreamers ever since.
""", ['San_Francisco'], priority=4, category='history', kind='story', radius=6000),

clip('sf_1906_story', '5:12 a.m., April 18, 1906', 37.725, -122.472, [], """
Okay, let's talk about the morning San Francisco fell down. At 5:12 a.m. on the 18th of April, 1906, the San Andreas Fault ruptured along about 280 miles of the coast. That's the same fault we followed past Tomales Bay and Bolinas this morning. A foreshock hit first, and then the main shaking lasted about 42 seconds. Magnitude about 7.9.

Then came the fires, which burned for days. More than 3,000 people died, the deadliest earthquake in American history, and over 80 percent of the city was destroyed. At the time, San Francisco was the biggest city on the West Coast.

Quiz: for years people thought the epicenter was up at Olema. Where do scientists now think it was? [[pause 5]] Offshore, near Mussel Rock by Daly City, the next town we drive through! And remember all the places we heard about today: refugees who started Stinson Beach businesses, Petaluma's relief efforts, the redwoods logged to rebuild the city. That earthquake shaped this whole region.
""", ['1906_San_Francisco_earthquake', 'San_Andreas_Fault', 'Daly_City,_California', 'Stinson_Beach,_California'], priority=4, category='history', kind='story', radius=6000),

clip('daly_city', 'Daly City: little boxes on the hillside', 37.706, -122.469, ['muir_sfo'], """
We're crossing into Daly City. After the 1906 earthquake, thousands of homeless San Franciscans headed south to the ranches here, including a big one belonging to John Daly, a dairyman who'd married his boss's daughter. The town grew from those refugees and took his name.

Then, from the late 1940s, a developer called Henry Doelger built Westlake, one of the first big planned suburbs, with rows and rows of similar houses up the hillsides. Quiz: Westlake inspired a famous 1962 folk song by Malvina Reynolds, poking fun at rows of identical suburban houses. What's it called? [[pause 4]] Little Boxes!

A sad note too: Filipino American families who wanted to buy here in the 1950s were barred from Westlake by racial covenants, so they bought homes east of Junipero Serra Boulevard instead.
""", ['Daly_City,_California'], category='culture'),

clip('colma', 'Colma: where the dead outnumber the living', 37.680, -122.455, ['muir_sfo'], """
Here's the weirdest town on our whole trip: Colma. Most of its land is cemeteries.

In 1900, San Francisco banned new burials inside the city, and in 1912 it evicted most of its existing cemeteries. So about 150,000 bodies were dug up and moved down here, at ten dollars per grave. Nearly everyone famous who died in San Francisco ended up here.

Quiz: the dead here outnumber the living. By roughly how much? [[pause 5]] About a thousand to one! Somewhere around one and a half million people are buried here. It's been called the City of the Silent, and its unofficial motto is: It's great to be alive in Colma.
""", ['Colma,_California'], priority=3, category='culture'),

clip('sweeney_ridge', 'Discovering San Francisco Bay', 37.640, -122.430, ['muir_sfo'], """
On the hills to the west is Sweeney Ridge. And something big happened up there.

In 1769, the Spanish explorer Gaspar de Portolá was leading an expedition up the coast. He sent a scouting party, led by Sergeant José Ortega, north to find the Point Reyes headlands, which we drove past this morning. Ortega came back and reported he couldn't get there. Quiz: why not? [[pause 4]] Because the Golden Gate was in the way! He'd found the strait. And from Sweeney Ridge, on the 4th of November 1769, the expedition became the first Europeans known to see San Francisco Bay. Well, the scouts had actually spotted it a few days earlier.

Amazing to think that all those sailors, Drake in 1579, Vizcaíno in 1603, sailed right past one of the greatest harbors on Earth and never noticed it, hidden in the fog.
""", ['Sweeney_Ridge', 'Golden_Gate', 'New_Albion', 'Point_Reyes_National_Seashore'], category='history'),

clip('sfo', 'SFO: from cow pasture to the world', 37.6213, -122.3790, ['muir_sfo'], """
And here we are: San Francisco International Airport. Quiz, one last time: when the city opened its airport here in May 1927, what was the land being used for? [[pause 4]] It was a cow pasture! 150 acres, leased from the Mills family estate, as a temporary, experimental airport called Mills Field. In 1931 the city bought the land and named it San Francisco Airport, and international was added after World War Two. Pan Am moved its flying boats here in 1944. Funny detail: it's owned by San Francisco, but it's actually in San Mateo County.

So, Julia, Adam, our heroic driver: that's a wrap! From Sacramento's Gold Rush to Napa's vineyards, the Russian River's redwoods, the Sonoma Coast, Point Reyes, Muir Woods and the Golden Gate. Volcanoes, earthquakes, Russians, Hitchcock and an egg capital. It's been an honour being your tour guide. Safe travels, come back soon, and remember: Goonies never say die!
""", ['San_Francisco_International_Airport'], priority=5, category='history'),
]

def write(path, area_id, area_name, clips):
    json.dump({'area': {'id': area_id, 'name': area_name}, 'clips': clips}, open(path, 'w'), indent=1, ensure_ascii=False)
    print(path, len(clips))

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
