"""Persona rewrite (23 Oct feedback): warmer NorCal-local voice, quizzes with real pauses.
Same facts as before; only delivery changes. Applies new text to content/01_i80.json."""
import json, sys
sys.path.insert(0, 'scripts')
from rewrite_lib import apply

T = {
'trip_intro': """Good morning, Julia! Good morning, Adam! And a big hello to our trusty driver. I'm your guide for today, a proud NorCal local, and I am stoked to show you around. We're going from the capital to the redwoods: across a floodplain, over the hills into wine country, and down to the Russian River at Guerneville. I'll pipe up when there's something good, and I'll keep quiet when there isn't.

Okay, first quiz of the day, nice and easy. Before the levees went up, Sacramento flooded so often that the city did something kind of wild about it. What do you think they did? [[pause 5]] They raised the streets. A whole storey! That's why there are still tunnels and buried old storefronts under Old Sacramento, the riverside district with all the nineteenth-century brick buildings, the most famous ones built right after a huge fire in 1852.

And that golden lift bridge you might have spotted? That's the Tower Bridge, opened in 1935, with towers 160 feet tall. On opening day they released a thousand homing pigeons to carry the news across California. Pigeons! It got painted gold in 2002 after a public vote, and honestly, some locals are still grumbling about it. Alright, gang. Let's head west.""",
'trip_intro.more': """Okay, here's a name you're going to hear all day: Sam Brannan. Total character. He was a printer and a Mormon elder who sailed a whole shipload of Latter-day Saint emigrants around Cape Horn to California in 1846, and he packed a printing press and an entire flour mill for the trip. He started the California Star, San Francisco's first newspaper, and he's considered the first guy to spread the word about the Gold Rush. Then his stores supplied the rush, and boom: California's first millionaire.

He bought land everywhere, including a hot-springs valley at the top of Napa Valley that he named Calistoga. Hang on to that one. There's a great story coming.

Sadly, it didn't end well for Sam. He helped form San Francisco's first vigilance committee, which got him kicked out of his church. His wife divorced him, and he had to sell off a lot of his land to pay her half. He died poor and pretty much forgotten. His house in Old Sacramento, built in 1853, is still standing, though.""",
'west_sac': """Alright, first town of the day, and what a way to start. Picture it: 1849. A guy named James McDowell starts a bar fight, and loses it fatally. He leaves behind his wife Margaret, three daughters and 600 acres. And Margaret? She doesn't fall apart. She hires a surveyor, carves the land into forty-one blocks, and sells lots in a brand-new town she names the Town of Washington. Total boss move.

That's where you are now: West Sacramento, in Yolo County. Washington became a rest stop for exhausted travellers slogging through the marshes to Sacramento, and a busy fishing town, shipping salmon, sturgeon and crayfish all the way to San Francisco. Later it got renamed Broderick, and in 1987 it finally merged with its neighbours to become one city.

Quick one: West Sacramento is over a hundred miles from the ocean, by river. But it has a port for ocean-going ships. How do the ships get here? [[pause 4]] A 43-mile deep-water channel, dredged all the way up from Suisun Bay, opened in 1963. Mostly they ship out rice.""",
'yolo_bypass': """Okay, look out the windows, both sides. All that flat land? This is one of the cleverest bits of flood control in America, and you're driving right over it on the Yolo Causeway, a three-mile-long bridge.

Here's the trick. Instead of building taller and taller walls around Sacramento, engineers just gave the river somewhere else to go. Upstream there's a concrete spillway called the Fremont Weir. When the Sacramento River gets too high, the extra water simply pours over the top, into this basin. In a big flood this whole area becomes a shallow inland sea, about forty miles long and three miles wide, carrying several times the flow of the river itself. And the causeway keeps you high and dry above it all.

Why bother? Because the floods of 1862 and 1878 absolutely drowned this valley. Congress signed off on the plan in 1911, and the Army Corps of Engineers laid out the bypass in the early thirties.

In the dry months it's mostly farmland. And in winter they flood the rice fields after harvest, so thousands of ducks and shorebirds hang out in plain view of the freeway. So if you see water and birds out there, don't worry. That's the plan working.""",
'yolo_bypass.more': """Want to know who lives under this bridge? Have a guess. [[pause 4]] Bats! Roughly a quarter of a million Mexican free-tailed bats migrate to the Yolo Causeway every June. They squeeze into the expansion joints between the concrete sections and feast on bugs from the wetlands. It's one of the biggest bat colonies in California, and there are actual bat-watching tours at dusk.

Before any causeway existed, crossing this basin in the wet season meant a ferry, or a long detour south through Stockton. In summer, the first vehicle to make it across set the route of the Tule Jake Road. The first causeway opened in 1916 and they threw a three-day party for it. In 1928 it became part of the Lincoln Highway, the first road across America. Today's twin bridges date from 1962, and the traffic reporters call them the long bridge and the short bridge.""",
'davis': """Coming up is Davis, and here's a quiz for you, Adam and Julia. Davis is famous for one particular way of getting around. Any guesses? [[pause 4]] Bikes! It's so flat that it calls itself the bicycling capital of America, and it's even home to the United States Bicycling Hall of Fame.

Davis started out as a railroad stop in 1868, named Davisville after a local farmer, Jerome C. Davis. Then in 1907 the post office got tired of all those extra syllables and just chopped it down to Davis. Classic.

The big deal here is the university. Back in 1905 the state picked Davis from about fifty sites for a university farm, partly because Berkeley's own agriculture dean admitted that foggy Berkeley was terrible for farming. The farm opened in 1908 and grew into UC Davis, and its vet school is the biggest in the country.

And two very Davis oddities. In 1972, students built a little village of fibreglass geodesic domes, inspired by Buckminster Fuller, and people still live in them today. And Muir Commons, finished in 1991, is known as the first newly built cohousing community in the United States. Very Davis.""",
'davis.more': """Okay, wine nerds, this one's for you. UC Davis keeps popping up in the wine story all day. Back in 1903 the federal government set up an experimental vineyard at Oakville, in the Napa Valley, and UC Davis still runs it. In 1935, the Wolfskill family, the farming pioneers of Winters, gave the university a hundred acres of their old ranch for an experimental orchard.

Quiz: in 1951, UC Davis produced its very first graduates in the science of growing grapes and making wine. How many were there? [[pause 4]] Just seven! And one of them, Joe Heitz, went on to make one of Napa's most famous Cabernets, Martha's Vineyard, which was one of the California reds at the legendary 1976 Paris tasting. And since 2008, the campus has had a wine and food institute named after Robert Mondavi, the guy who did more than anyone to put Napa on the map. You'll hear about him soon.""",
'patwin_story': """Let's rewind way, way back. Long before the farms, the freeway and the bikes, this edge of the Sacramento Valley belonged to the Patwin, the southern branch of the Wintun peoples, who've lived around here since roughly the year 500.

They lived in settled villages, fishing, hunting and gathering, and the big one was acorns. All those oak groves on the plains and foothills? That was the harvest. Here's something cool: their group names are still all over today's map. The Ululatos lived where Vacaville is now, around a village on Ulatis Creek. The Labaytos lived along Putah Creek, the Malacas in Lagoon Valley, the Tolenas up the Suisun Valley, and the Suisunes on the Suisun Marsh, which is named after them. One of the most famous Patwin leaders was Sem-Yeto, better known as Chief Solano, a diplomat and a friend of the Mexican general Vallejo.

Then the Gold Rush hit, and it was devastating. Settlers took the oak groves and the water. Smallpox and measles swept through. A lot of Patwin people were forced into unpaid work on ranches and in mines, which historians describe as another form of slavery. By the late 1850s the population had collapsed, and by the 1920s nobody was left along Putah Creek.

But here's the good part: the Patwin are still here. Today they belong to three federally recognised tribes, including the Yocha Dehe Wintun Nation, and the language, listed as at risk in 1997, is being taught to kids again. And near Fairfield, a hillside park that opened in 2024 has a Patwin name: Patwino Worrtla Kodoi Dihi, meaning Southern Rock Home of the Patwin People, run together with the Yocha Dehe.""",
'dixon': """Here's a fun one. Dixon, coming up, is a town that literally picked itself up and moved.

During the Gold Rush there was a little settlement called Silveyville around here, a halfway stop for miners heading between the coast and the gold fields. Then the railroad showed up in 1868, and it missed Silveyville by a few miles. Awkward. So in 1871 the whole town just relocated, buildings and all, to sit next to the tracks. The Methodist church on North Jefferson Street made the trip.

Quiz time. The new town was supposed to be called Dicksville, after Thomas Dickson, who donated the land for the depot. So how did it end up as Dixon? [[pause 5]] A typo! In 1872 the first train shipment from San Francisco arrived addressed to Dixon, and everybody just shrugged and went with it.

A couple more Dixon brags: the Dixon May Fair, started in 1885, is billed as California's oldest fair. A local pumpkin patch keeps breaking the Guinness record for the world's biggest corn maze, one of them sixty acres. And near where Highway 113 meets the interstate, there's a hundred-foot-tall sign for the old Milk Farm Restaurant. The sign went up in 1963, and it's still standing, way after the restaurant closed.""",
'valley_geology': """Okay, geology time, and I promise this one's cool. Question: why is this valley so ridiculously flat? [[pause 4]] Because you're driving across the top of a giant filled-in hole.

Back when dinosaurs were around, between about 150 and 65 million years ago, this whole valley was a seaway. To the east, where the Sierra Nevada is now, there was a chain of volcanoes. To the west, an ocean plate was diving under North America, and the rocks scraped off it piled up into a ridge that worked like a dam. In between was a deep basin, and the volcanoes eroded straight into it, sending mud and sand down underwater canyons. Geologists call the result the Great Valley Sequence, and in places it's around 40,000 feet thick. That's over seven miles of stacked-up sea floor.

And here's the mind-blowing bit. The volcanic top of the ancient Sierra was mostly stripped off and used to fill this valley. You're basically driving over a mountain range that got flattened and poured into a bowl.

Those old sea-floor rocks come up to the surface along the western edge of the valley, in the hills ahead of us. Right under the freeway, the geological maps show the most recent layers: sand and gravel fanned out by creeks, and low ridges called natural levees that rivers build when they flood. So this flat farmland is just the top layer of a seven-mile stack of history.""",
'vacaville': """Coming up is Vacaville, and its founding story is a little shady. Here's how it went down.

In 1841, two guys from New Mexico, Juan Manuel Vaca and Juan Felipe Peña, came to California, and in 1843 they were granted a huge ranch called Rancho Los Putos: over 44,000 acres, stretching almost all the way to Davis. Peña's adobe house, built in 1842, is still standing, the oldest building around here.

Then in 1850, Vaca sold some land to a man named William McDaniel, on the condition that a square mile would become a town called Vacaville. McDaniel's business partner, a lawyer, acted as interpreter, because Vaca couldn't read or write English. Quiz: Vaca thought he was signing away one square mile. How much did he actually sign over? [[pause 5]] Nine! Vaca was furious. He took out a notice in the newspaper warning everyone not to buy land from McDaniel. Peña was mad too, and it wrecked their friendship.

Vacaville grew rich on fruit, with lots of Japanese and Chinese workers in the orchards and packing houses. And a more recent claim to fame: in August 2022, a truck crashed on the freeway here and splattered over 150,000 tomatoes across the eastbound lanes. It made international news. Ketchup, anyone?""",
'nut_tree': """Coming up near the junction with Interstate 505 is the Nut Tree. Today it's a shopping centre, but it used to be a legit California legend.

It opened on the 3rd of July 1921 as a tiny fruit stand on the old Lincoln Highway, run by Helen and Ed Power. It's named after a black walnut tree that grew from a nut a pioneer girl, Sallie Fox, picked up on a trail in Arizona before she got here in 1859.

The stand blew up. By year two it was serving around 950 cars a day. Then it grew into a restaurant with a floor-to-ceiling glass aviary, a bakery, a toy shop, and its own little train out to its own airport. Charles Eames designed the furniture! It's even credited as an early pioneer of California cuisine, all fresh fruit and veg.

Quiz! Reagan, Nixon and Bing Crosby all stopped by the Nut Tree. But in 1983 it catered lunch for someone even fancier. Who? [[pause 5]] Queen Elizabeth the Second! Not bad for a fruit stand. The original closed in 1996.""",
'vaca_mtns': """See that ridge rising up to the west? Those are the Vaca Mountains, the very first wall of California's Coast Ranges, and the thing standing between this flat valley and all the wine country we're about to see.

Quiz: once we cross over those hills, everything gets a lot greener. Why do you think that is? [[pause 5]] Rain shadow! The Vacas are the furthest range from the ocean, so the clouds have already dropped most of their rain on the mountains further west. That's why the ridgetops here are dry chaparral: chamise, manzanita and buckbrush.

The east face of the Vacas shoots straight up, a thousand feet or more above the foothills. The highest point, Mount Vaca, is 2,818 feet, the top of Solano County, and the long, flat backbone is called the Blue Ridge.

Since almost all the rain falls in winter, by late summer and fall these hills are tinder-dry. In August 2020, the Hennessey Fire burned through here and destroyed farms and homes in Vacaville. We'll hear more about those fires later.""",
'travis': """Eyes on the sky, team! If you spot something huge and grey lumbering overhead, it's almost definitely coming from Travis Air Force Base, a few miles east of Fairfield.

Travis calls itself the Gateway to the Pacific, and it moves more cargo and passengers than any other military air terminal in the United States. It flies massive C-5 Galaxies, C-17s and KC-46 tankers, and it's the biggest employer in the whole county.

It started in 1942, ferrying planes and supplies out to the Pacific in the Second World War. After the war it became a bomber base for B-29s, B-36s and later B-52s.

And the name comes from a pretty dramatic story. In August 1950, a B-29 carrying a nuclear bomb, without its nuclear core thank goodness, crashed just after take-off. The fire set off the bomb's regular explosives, killing Brigadier General Robert Travis and eighteen others. The base was named after him the following year.""",
'jelly_belly': """Okay, this is one of my favourites. Fairfield is the home of the Jelly Belly! And the story goes from Germany all the way to the White House.

Gustav Goelitz started a candy business back in 1869, and the family got big making candy corn. His son Herman moved west and ended up in Oakland in 1924. In the 1960s they started making tiny, super-flavourful mini jelly beans. And guess which famous fan got hooked on them? [[pause 4]] Ronald Reagan! He'd quit smoking and taken to sweets instead. As governor in 1973, he wrote to the company that they could hardly start a meeting without passing the jar around.

Then in 1976 a candy guy named David Klein came up with the idea of selling each flavour separately, and he named them Jelly Belly, after the blues singer Lead Belly. Okay, Julia, Adam, let's see how you do. The original eight flavours: name as many as you can. [[pause 7]] Very Cherry, Tangerine, Lemon, Green Apple, Grape, Licorice, Root Beer and Cream Soda! How many did you get? The company's still based right here in Fairfield.""",
'fairfield': """Fun fact about the next two towns: they were both named by the same guy, a clipper ship captain called Robert H. Waterman. He named Fairfield after his hometown back in Connecticut. And in 1853 he started a little settlement he called Bridgeport. When the post office asked for something more original, he renamed it after the most important person in his life. Any guesses? [[pause 4]] His wife, Cordelia! Aww.

Waterman also pulled off a sneaky political move. In 1858 he entered Fairfield in the race to become the county seat, and won it away from Benicia, helped by offering sixteen acres of free land for county buildings. Fairfield's been the county seat ever since.

And one more local secret. In the hills here there used to be a company town called Cement, founded in 1902 to quarry limestone and make cement. At its peak it had more people than Fairfield, Vacaville and Suisun City combined, with a three-storey hotel, a hospital and a baseball diamond. When the limestone ran out it was sold off, in 1927. Its biggest concrete ruin, which locals call The Castle, can be seen from the freeway here in Fairfield. Keep your eyes peeled.""",
'fairfield.more': """Just north of Cordelia, in the Suisun Valley, there's a little stone church with a big story: the Rockville Stone Chapel, built by volunteers in 1856. The stone is volcanic ash rock from the nearby hills, and it's soft and easy to cut when it comes out of the ground, then hardens once it's exposed to air. How handy is that?

The land was donated by Landy Alford, who came west in 1846 in the same wagon train as the famous Donner Party, and his son-in-law later helped rescue the survivors.

Then the Civil War split the church. The congregation divided over slavery, and on Christmas Eve 1863, the northern supporters literally walked out. The southern-leaning members who stayed put up a plaque reading M.D. Church South, and it's still there. The chapel fell apart for decades, got restored in 1940, and it's still in use today.""",
'suisun_marsh': """Off to the south is a place where people tried to farm for about fifty years, and gave up because it got too salty even for the cows. That's the Suisun Marsh, described as the biggest brackish-water marsh on the whole west coast: over a hundred thousand acres of tidal marsh and sloughs, where fresh river water meets the salty bay. It's named after the Suisunes, a Patwin group who lived here.

During the Gold Rush, hunters shot ducks and geese here to sell fresh birds and feathers in San Francisco's markets. From the 1880s, farmers built levees and tried to grow crops, until the soil got too salty even for cattle. Then the big water projects upstream made it saltier still. These days it's home to river otters, native fish and pelicans.""",
'railroad_story': """Okay, here's a story with a twist. Quiz first: when the transcontinental railroad was finished with the famous golden spike in May 1869, where did it actually end? [[pause 5]] Sacramento! Not the Pacific. Getting trains the rest of the way to San Francisco Bay was a whole separate race.

And the tracks beside this freeway? They won a part of that race. They were built by the California Pacific Railroad, to link Vallejo, on the bay, with Sacramento. The line was finished in November 1868, six months before the golden spike, so from early 1869 you could take a ferry from San Francisco to Vallejo and catch the train from there. Towns like Davis and Dixon grew up around its stations, and it even had a branch up the Napa Valley to Calistoga.

Of course the big Central Pacific wanted it. When the owners said no to their offer, Central Pacific threatened to build a rival line right next to it, bought up most of the stock, and took over. Then they built a shortcut across the Suisun Marsh, which took two years because the marsh was so squishy it needed tons of crushed rock. From 1879, entire trains crossed the Carquinez Strait on a giant ferry.

And the line's still busy. Amtrak's Capitol Corridor trains follow the old route, and the California Zephyr and the Coast Starlight roll right through Dixon without stopping.""",
'highway_story': """This road you're on has had a few identities. In 1913, the Lincoln Highway was dedicated: the dream of an Indiana entrepreneur, Carl Fisher, and one of the first highways in America built for cars, running all the way from Times Square in New York to San Francisco. In 1928, it was rerouted across the Yolo Causeway and through Davis, Dixon, Vacaville and Fairfield, pretty much where you are right now.

Then it became Highway 40, and roadside spots like the Nut Tree fruit stand grew up along it. In the fifties and sixties it was rebuilt as Interstate 80, the main coast-to-coast route from New York to San Francisco.

Quick quiz: old Highway 40 used to run through here. Where does it end now? [[pause 5]] Utah! It got cut back that far. And the freeway's still changing: the toll express lanes between Fairfield and Vacaville only opened in December 2025.""",
}

if __name__ == '__main__':
    apply('content/01_i80.json', T)
