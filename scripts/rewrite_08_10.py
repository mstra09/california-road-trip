"""Persona rewrite for content/08_west_county.json, 09_napa_hills.json and 10_stories.json."""
import sys
sys.path.insert(0, 'scripts')
from rewrite_lib import apply

WC = {
'sebastopol': """Welcome to Sebastopol, which has one of the best name stories on the map. Quiz: the town was originally called Pine Grove. Then in the late 1850s, a bar fight broke out. And somehow that led to the new name. How? [[pause 6]] A bystander said the long, drawn-out brawl was like the siege of Sevastopol, a Russian port in the Crimean War. And the name stuck! Remember Yountville? It was going to be called Sebastopol too, but this town got there first.

The Coast Miwok and Pomo were here first, and the town sits on top of several of their village sites. Later there was a busy Chinatown downtown from the 1880s.

Then came the apples. Sebastopol called itself the Gravenstein Apple Capital of the World. The Gravenstein is an old Danish apple, from the 1600s or earlier: tart, juicy, perfect for apple sauce and cider, but it doesn't keep, so you can only get it in season. There's still a Gravenstein Apple Fair every August. These days the old apple warehouses have turned into The Barlow, full of tasting rooms and restaurants.""",
'sebastopol.more': """Luther Burbank, our potato guy, needed more space than his Santa Rosa garden, so in 1885 he bought a farm here in the Gold Ridge area. Quiz: at its peak, how many plant experiments do you think he had going on this farm at once? [[pause 5]] Over 60,000, by some estimates! Three acres of it survive, with more than 250 of his plants, looked after entirely by volunteers.

And Sebastopol used to have electric trolleys! From 1903 to 1947, the Petaluma and Santa Rosa Railway ran around the county, partly to break the big railroad's monopoly. All that's left is one passenger car in a museum, and its old stone power house on Petaluma Avenue, which has, very fittingly, been turned into a series of brew pubs.""",
'wilson_grove': """Here's a surprise for a town twenty miles from the ocean. The geology maps show that Highway 116 north of Sebastopol runs for more than ten kilometres across an old sea floor! It's called the Wilson Grove Formation: pale sandstone laid down in the sea between about eleven and three million years ago, and in places it's full of broken-up seashells.

So all this gentle Gold Ridge country around Sebastopol used to be under the ocean, and got lifted up as the Coast Ranges rose. To the east, the Santa Rosa plain is made of gravel washed out of the hills. And as we head north toward the river, the road crosses into much older, harder rock from that geological junk drawer, the Franciscan Complex.""",
'graton': """Graton, just off the highway, is a little apple town that turned into a wine town. And quiz: it was once at the very edge of an empire. Which one? [[pause 5]] The Russian Empire! Graton is about as far south and east as Russian colonisation in the Americas ever reached. The Russians at Fort Ross on the coast needed food, so in 1836 their farm expert, Yegor Chernykh, set up a farm between here and Occidental, with barracks, vegetables, wheat, and a big vineyard. So Russians helped plant some of the first vines around here!

There's a sadder story in these hills too. In 1851, many California tribes signed treaties promising them land, but the U.S. never ratified them. In 1920 the government bought fifteen acres near here for the homeless Coast Miwok and Pomo people of the area. When seventy-five people tried to move in, they found only three acres were livable. And in 1958, the government ended the rancheria altogether.""",
'freestone': """Freestone, population about thirty-two, is the gateway to the Bohemian Highway. It's named after a sandstone quarry, and it was the first historic district Sonoma County ever named, in 1974.

And it has my favourite crime story of the trip. In 1876, a farmer built the Hinds Hotel here when he heard the railroad was coming, and the carpenters building the railway line stayed there. Quiz: according to first-hand reports, the innkeeper came up with a sneaky plan to keep his guests around longer. What did he do? [[pause 6]] He had parts of the bridge they were building secretly burned at night, so the job would take longer! He went to jail for it. Customer retention, Wild West style.

And in the 1970s, the old hotel was the party headquarters for the artists Christo and Jeanne-Claude while they built their famous Running Fence.""",
'occidental': """This next town has a creek named after a sailor who jumped ship, and a commune that tried to give its land to God. Welcome to Occidental!

It was founded in 1876 as a stop on a railroad from the Sausalito ferry up to the redwoods. A local landowner, a Danish sailor known as Dutch Bill Howard, who'd jumped ship in San Francisco Bay in 1849, gave the railroad its right-of-way. In return he got a free lifetime train pass, and the station was named after him. The creek next to the road is still Dutch Bill Creek. The railroad started a timber boom, and by 1877 there were six sawmills here.

Then, a hundred years later: hippies! In 1966 Lou Gottlieb, from the folk band the Limeliters, bought land near here, and in 1967 he opened it to anyone who wanted to live there. Morning Star Ranch drew hundreds of people from San Francisco's Haight-Ashbury, and the county answered with arrests and bulldozers. Quiz: in 1969, Gottlieb tried to transfer the land to a new owner, to get the county off his back. Who? [[pause 5]] God! He deeded the land to God. The courts did not accept God as the owner.""",
'camp_meeker': """Quiz: how much would you pay for a plot of land twenty-five feet by twelve, with a one-room cabin on it? [[pause 4]] In 1898, right here, it cost seventy-five dollars. This is Camp Meeker, named after Melvin Cyrus Meeker, a lumber baron who opened mills here around 1866. These redwoods built San Francisco, and then, after 1906, rebuilt it. Meeker is the same guy who sold the Bohemian Grove land to the Bohemian Club. Once the trees were cut down, he chopped the land into those tiny lots and sold them to San Franciscans wanting a summer escape.

Now it's a little village of about 425 people tucked among the new redwoods, with some roads so steep and narrow they feel like old railway tracks. And the creek has become a happy conservation story: wild coho salmon came back to spawn in 2001, young salmon have been released here since 2006, and in 2009 an old swimming-hole dam, one of the worst salmon blockers in the whole watershed, was swapped for a footbridge.""",
'coast_miwok_story': """The land from the Golden Gate up to the Sonoma coast, and east to Sonoma Creek, was home to the Coast Miwok. That includes the hills around Sebastopol and Freestone and the lower Sonoma Valley.

They lived in small bands with no central government. In spring they headed to the coast for salmon, shellfish and seaweed. The rest of the year, acorns were the staple, plus deer and rabbit. Quiz: Coast Miwok hunters had a clever trick for sneaking up on deer. What do you think they did? [[pause 5]] They rubbed themselves with a plant called Brewer's angelica to hide their scent! They also drank yerba buena tea as medicine, made tattoo ink from burned poison oak, and built cone-shaped houses called kotcha from tule reeds or redwood bark. Amazing basket makers too.

The word Miwok just means people. Within a couple of generations of the Spanish arriving, the people of this region lost their land and were devastated by disease. Later, broken federal treaties left them landless. If you ever visit Point Reyes, there's a recreated Coast Miwok village there called Kule Loklo.""",
}
NH = {
'silverado_trail': """You're on the Silverado Trail, the quieter road up the east side of the Napa Valley, 29 miles long. And quiz: back in the 1880s, travellers on this road had to watch out for a famous someone. Who? [[pause 4]] A stagecoach robber called Black Bart! He preyed on travellers here. Things got safer when a motor bus service started in 1910.

The road started in 1852 as a trail used when floods made the main valley road impassable. Later it became the wagon road for the mercury mines on Mount Saint Helena, and the first permanent road between Napa and Calistoga. Silver was found in the valley in 1858. Today there are at least forty wineries along it, and every March it hosts the Napa Valley Marathon.

The hills just east of Napa are called Coombsville, after Nathan Coombs, the guy who founded Napa. Volcanic soil, and fog that rolls in early and hangs around late.""",
'stags_leap': """Okay, wine fans, sit up! You're about to pass the vineyard that beat the French. This is the Stags Leap District, a tiny pocket of land only about one mile by three, with hills on three sides.

Here's the story. Warren Winiarski fell in love with wine while spending a year in Italy studying Machiavelli. He moved his family to Napa in 1968 and worked at Robert Mondavi's new winery. Then he tasted a homemade wine from a neighbour, Nathan Fay, and thought, this is it. In 1970 he bought the 44 acres next door. Quiz: what was growing on the land when he bought it? [[pause 5]] Prunes, cherries and walnuts! He ripped them out and planted Cabernet. And his 1973 Cabernet went to Paris in 1976 and took first place, beating Château Mouton-Rothschild and Haut-Brion. The magazine Decanter called it a victory that put California on the winemaking map.

And the soil here is special: clay from the Napa River mixed with volcanic stuff washed down from the Vaca Mountains.""",
'frogs_heitz': """Two wineries along here tell two sides of the Napa story.

First, Frog's Leap, started in 1981 by a doctor and a winemaker at a spot known as Frog Farm. Quiz: the winemaker got his start at a very famous winery nearby. Can you guess which, from the name? [[pause 4]] Stag's Leap! Frog Farm plus Stag's Leap equals Frog's Leap. And the corks say Ribbit. But behind the jokes, it's serious stuff: it was the first Napa winery to use certified organic grapes, the vines aren't irrigated, and since 2005 solar panels supply most of its power.

Then Heitz Cellar, from 1961, back when Napa had only about two dozen wineries left. Joe Heitz, a farm boy from Illinois, was one of the first seven people ever to graduate from UC Davis in winemaking, in 1951. He trained under the legendary Tchelistcheff, bought a little vineyard for 5,000 dollars, and his Martha's Vineyard Cabernet became a Napa legend. It was even one of the reds tasted in Paris in 1976.""",
'howell_mtn': """Look east around St. Helena. That forested ridge is Howell Mountain. And here's a surprise: Napa was winning medals in Paris long before 1976!

Two French winemakers set up there in 1877, and Charles Krug planted about a hundred acres by 1884. Then a man called W. S. Keyes planted his vineyard in 1880. Quiz: at the Paris Exposition of 1899, what did his wines win? [[pause 4]] Gold and bronze medals! And in 1904, his claret won the grand prize at the St. Louis World's Fair. So 1976 wasn't the first time Napa impressed the French. It was just the most famous.""",
'white_sulphur': """Mark Twain and Clark Gable both came to soak in springs near here. Near St. Helena was White Sulphur Springs, said to be the oldest warm-spring resort in Northern California, opened in 1852. Native people used the springs long before that.

In the late 1800s, rich San Franciscans got here by steamboat, then train, then stagecoach. Quiz: at its peak, how many guests could the grand hotel hold? [[pause 4]] A thousand! After the 1906 earthquake it housed refugees. Sadly, fire was always its enemy: three grand hotels burned over the years, and the 2020 Glass Fire destroyed most of what was left.""",
'spring_mtn_district': """You're climbing Spring Mountain Road into the Mayacamas. Quiz: where's the actual Spring Mountain? [[pause 4]] Trick question! There isn't one. Spring Mountain was the name for a whole green, well-watered area of hills full of springs and little streams, not one peak.

It was one of the first places in Napa recognised for grapes. The first documented vineyard was Charles Lemme's La Perla, planted in 1874, and in the 1880s the Beringer brothers planted up here too. The vineyards are on steep slopes, so the crops are small: it makes less than two percent of Napa's wine. Up over the county line, the road becomes St. Helena Road and drops down toward the start of Mark West Creek.""",
'mayacamas': """You're crossing a mountain range that the federal government couldn't decide how to spell! These are the Mayacamas Mountains, 52 miles long, separating the Napa and Sonoma valleys. The highest point is Cobb Mountain, 4,724 feet, and the rain that falls up here ends up in Putah Creek, Sonoma Creek, Santa Rosa Creek and Mark West Creek.

The name probably comes from a Wappo village called Maiya'kma, near Calistoga. Quiz: the federal naming board made one decision on the spelling, then reversed it in 1941. Which spelling did they finally pick? [[pause 5]] Mayacmas! Without the second a. And plenty of people still write Mayacamas. And there's still a creek called Maacama. So, honestly, spell it however you like.

The road you're on crosses a volcanic landscape: white pumice from an eruption about 4.84 million years ago, grey lava from about 7.9 million, and swirly glassy lava from about 5.3 million. And about ten million years ago, these mountains were probably covered in cypress forest.""",
'appellation_politics': """Two wineries went to war with the federal government over one word: Calistoga!

Here's the deal. Official wine regions are created by the federal government, and once one exists, wineries have to use mostly grapes from that area to put its name on the label. In 2003, Bo Barrett of Chateau Montelena asked for a Calistoga wine region. But two wineries, Calistoga Cellars and Calistoga Estate, already had Calistoga in their brand names. Quiz: what do you think they'd have to do if the region was approved? [[pause 5]] Either use at least 85 percent Calistoga grapes, or change their names! They fought it hard. It finally got approved in 2009, and they got three years to comply.

Next door, Diamond Mountain had a fight over one word too, and the owners of a winery with that trademark won, so it's officially the Diamond Mountain District. And in Sonoma, a giant region called Northern Sonoma was created in 1985 largely because of the huge Gallo winery.""",
}
ST = {
'goldrush_story': """Okay, let's talk about the event that made Sacramento, and, honestly, most of what you'll see today.

On the 24th of January 1848, James Marshall was building a sawmill for the pioneer John Sutter, up the American River, when he spotted something shiny in the water. Gold! Sutter tried to keep it secret, because he was worried a rush would wreck his plans for a farming empire. Quiz: who do you think spread the news anyway? Hint: you've already met him today. [[pause 5]] Sam Brannan! And about 300,000 people poured into California. San Francisco went from about 200 people in 1846 to around 36,000 by 1852, and California became a state in 1850.

The Gold Rush echoes through this whole trip. West Sacramento was a rest stop for miners. Dixon started as a halfway stop for them. Alfred Tubbs made his fortune selling rope to the rush, then founded Chateau Montelena. Dr. Bale of the grist mill went off mining and died of a fever. And all those new people were thirsty, so vineyards spread across Napa and Sonoma in the 1850s.

But it was a catastrophe for Native Californians. Disease, hunger and violence made their populations collapse, and whole tribes were driven from their land, including the Patwin of this valley.""",
'delta_story': """South of the freeway, out of sight, is one of the most important places in California: the Sacramento-San Joaquin River Delta. The Yolo Bypass floods drain into it, and so does about half of all the water that runs off California's land.

Here's how it formed. Around 560,000 years ago, water broke through the coastal mountains and carved the Carquinez Strait and San Francisco Bay. All the rivers had to squeeze out through that one narrow gap, which slowed them down. The tides pushed back up and slowed them even more, so the rivers dropped their mud and built a huge freshwater marsh full of channels and peat islands.

Then people drained it. Today there are about 57 reclaimed islands, ringed by 1,100 miles of levees. Quiz: when you drain peat soil, something weird happens to the land. What? [[pause 5]] It sinks! The peat breaks down and blows away, so a lot of the Delta now sits below sea level, behind its levees. That's why it's nicknamed California's Holland. And giant pumps at the south end send Delta water to farms and to the cities of Southern California. So pretty much every California water fight ends up here.""",
'tule_fog': """Here's a handy one if you ever drive this valley in winter. From November to March, after the first big rains, the Central Valley gets something called tule fog, named after the tule reeds that used to cover the wetlands.

On long, still winter nights, the damp ground cools fast, and the cold air near the ground gets trapped under warmer air above, until it turns into a thick, low blanket of fog. It can stretch over 400 miles, from Bakersfield to Red Bluff. Quiz: in 2005, tule fog was the number one cause of what in California? [[pause 4]] Weather-related car accidents! So if you ever see this valley disappear into a white wall on a winter morning, slow way down. Today, in late October, we're just ahead of the season. Phew.""",
'farm_labour_story': """Every vineyard and orchard you pass depends on people who rarely show up in the wine brochures. Here's their story.

The first workers were Native Californians, often forced. The Patwin were made to work for free on ranches and in mines, and by 1870 only a few Native people remained in the Napa Valley, working as labourers and servants. In the late 1800s, Chinese and Japanese immigrants worked Vacaville's orchards. In World War Two there was even a camp of German prisoners of war near Windsor, put to work.

The biggest change was the Bracero Program, a deal between the U.S. and Mexico that started in Stockton in August 1942 to fill wartime labour shortages. Over 22 years, it offered millions of contracts to Mexican workers. Quiz: what minimum hourly wage were they promised? [[pause 4]] Thirty cents an hour. The programme ended in 1964, and economists later found that ending it pushed farms toward machines.

Today, around a third of Napa County's people are Hispanic or Latino. And the tension between luxury and labour is very much alive: in 2026, Thomas Keller of the French Laundry opposed a plan for 120 apartments in Yountville for workers who'd been priced out of town.""",
'ag_preserve_story': """Have you noticed something about the Napa Valley floor? There are basically no housing developments or shopping malls between the towns. That's not luck. It's one of the most important land decisions in California history.

Neighbouring counties let big stretches of farmland turn into houses and shops. But in 1968, Napa's winemakers and civic leaders went the other way. Using a new state law that gave tax breaks for keeping land in farming, they created an agricultural preserve on the valley floor. Quiz: was Napa the first county in California to do this? [[pause 4]] Yes! It was the first one in the state. It started at 23,000 acres and grew to over 30,000. Then in 1990, voters went further and froze county zoning changes for thirty years, unless two-thirds of voters agreed.

The fights never stop. Locals battled the Wine Train in the eighties. County rules even stop Castello di Amorosa from hosting weddings. And now the big fight is about whether the people who work here can afford to live here. The preserve kept the valley green. Who gets to live in it is the next argument.""",
'cannabis_story': """Wine isn't the only crop around here with a complicated legal history.

California has been at the front of cannabis politics for half a century. In 1972, it held the first ballot vote in the nation to legalise cannabis. Quiz: did it pass? [[pause 4]] Nope! It failed. But in 1996, California became the first state to legalise medical cannabis, and in 2016, voters legalised recreational use, with 57 percent of the vote.

Legalisation turned out to be messy. Growers had to register and get permits, and more than half of the medical dispensaries closed. Legal businesses pay hefty taxes, while illegal growers keep going in remote rural areas. And it's all still illegal under federal law. So, a bit like the winemakers during Prohibition, today's cannabis farmers live in a weird legal twilight zone between what the state allows and what Washington forbids.""",
'russians_story': """We've met Russians again and again today: a river, a mountain, a farm near Graton. So here's the whole story.

Russian traders pushed east across Siberia and the North Pacific, and in 1799 they set up a colony in Alaska. Their business was fur, especially sea otters. From 1803, American ship captains took Alaska Native hunters down the California coast to hunt otters, and between 1805 and 1812 alone they gathered over 22,000 pelts.

In 1812 the Russians built their own base, Fort Ross, on the Sonoma coast, in the land of the Kashaya Pomo. It was super diverse: Native Californians, Native Alaskans, Russians, Finns and Swedes, all together. They explored the river and planted a farm and vineyard near Graton. And the Spanish and Mexicans got so nervous that they built the mission at Sonoma partly to block them.

Quiz: in 1841 the Russians decided to sell Fort Ross. They offered it to General Vallejo, but the Mexican officials dithered. Who ended up buying it? [[pause 5]] John Sutter! The same Sutter on whose land gold was discovered seven years later. Small world.""",
'grape_king_story': """Here's a wine story you won't hear in many tasting rooms.

California's first wine grape was the Mission grape, brought by the Spanish, and it ruled until about 1880. Then the Gold Rush created thirsty customers, and Agoston Haraszthy brought in cuttings from 165 of Europe's best vineyards. Charles Krug, a Prussian political dissident, learned winemaking from Haraszthy before starting his own winery in St. Helena.

And north of Santa Rosa, at the utopian colony of Fountain Grove, the vineyards were run by Nagasawa Kanaye. Quiz: what nickname do you think he earned? [[pause 4]] The Grape King of California! He was one of the biggest winemakers in the state, and he threw lavish dinners for guests like John Muir, Thomas Edison and Henry Ford. And according to the history books, Fountain Grove's cellars kept flowing right through Prohibition. Wink.

It's a reminder that wine country's history is a lot more diverse than the fancy châteaux suggest: Spanish missionaries, a Hungarian adventurer, German and Italian immigrants, a Finnish sea captain, and a Grape King, all on land that was Pomo, Wappo, Miwok and Patwin for thousands of years.""",
}

if __name__ == '__main__':
    apply('content/08_west_county.json', WC)
    apply('content/09_napa_hills.json', NH)
    apply('content/10_stories.json', ST)
