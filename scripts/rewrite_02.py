"""Persona rewrite for content/02_napa.json (same facts, warmer delivery, quizzes)."""
import sys
sys.path.insert(0, 'scripts')
from rewrite_lib import apply

T = {
'jameson': """Okay, fun thought for this stretch: you're driving through old sea floor. This is Highway 12 through Jameson Canyon, the gap in the hills between Solano County and Napa, and back in 1928 it became part of the Lincoln Highway, the first road across America.

Check out the rocks. The geological maps show Markley Sandstone along here, white to light-grey, around 40 to 50 million years old. Further west come marine sandstones from the late Miocene, including one called the Cierbo Sandstone, which has beds of fossil shells in places. So these hills are basically old beaches and sea floor, folded up and lifted high.

And from here on, we start meeting the rock that runs the whole show today: the Sonoma Volcanics, lava flows that erupted between about eleven and three million years ago. Over that ridge? Wine country, baby.""",
'napa_intro': """Welcome to the Napa Valley, everybody! This is the big one. In 1981 it became only the second official wine region in the whole country, and now it's one of the most famous wine regions on the planet, with more than 450 wineries.

Quick lay of the land. The valley floor rises gently from sea level here near the bay up to Calistoga at the far end, at the foot of Mount Saint Helena. Mountains on both sides: the Mayacamas on your left as we head north, and the Vacas on your right. And two roads run up the valley: Highway 29 on the west, and the quieter Silverado Trail on the east.

Quiz! Where do you think the name Napa comes from? [[pause 5]] It's Native American, and the best guess is the Patwin word napo, which means house. And back in the 1850s, people even spelled it with two p's: Nappa.

The Napa wine story has three acts. Act one: a huge boom in the 1800s. Act two: a total crash, thanks to a bug, Prohibition and the Depression. Act three: an epic comeback, ending with Napa beating the French in Paris in 1976. I'll fill you in as we go.""",
'south_napa_quake': """Somewhere just west of here, under the vineyards and marshes between American Canyon and Napa, is the epicentre of the biggest Bay Area earthquake in a quarter of a century.

Picture it: 3:20 in the morning, the 24th of August 2014. A magnitude 6.0 quake hits, shaking for ten to twenty seconds. One person was killed, about 200 were hurt, and the damage came to somewhere between 362 million and a billion dollars. Downtown Napa took a beating, even buildings that had been earthquake-proofed: the old courthouse, the post office, churches and the library.

Quiz: the fault behind it, the West Napa Fault, is about 35 miles long. When do you think it was discovered? [[pause 5]] Only in 1976, and by a guy drilling for groundwater from Sebastopol! And in 2023 they found out it's nine miles longer than anyone thought. Cool footnote: an experimental earthquake warning system gave seismologists a few seconds' heads-up before the big shaking arrived.""",
'napa_town': """Picture Napa's Main Street in the 1850s: up to a hundred saddle horses tied up on any old afternoon. Yeehaw.

The city of Napa, off to the east, started life as a river town. The Napa River is tidal here, so this was as far as boats could get. The first recorded ship came up in 1842, and by 1850 a steamer called the Dolphin was carrying passengers. Nathan Coombs laid out the town in 1847 and 1848, and in 1859 John Patchett opened the county's first commercial winery, selling wine for two dollars a gallon. Two bucks!

There's a darker side to the story, though. When the first recorded expedition came into the valley in 1823, most people here were Native Americans. In 1850, fighting with American settlers turned into war, and soldiers massacred the people they found, driving the survivors north toward Clear Lake.

And a fun one to finish. In 1880 the Napa Valley Opera House opened downtown with Gilbert and Sullivan's HMS Pinafore. Jack London read there in 1905. It closed in 1914, sat empty for decades, then reopened in 2003. Quiz: what show do you think they picked for the reopening? [[pause 4]] HMS Pinafore, of course!""",
'napa_town.more': """For most of its history, Napa was the town wine tourists drove straight through. That changed after a 300-million-dollar flood project around the turn of this century widened the river and raised the bridges, and the developers moved in.

The big showpiece was Copia, a center for wine, food and the arts, mostly paid for by Robert and Margrit Mondavi and named after the Roman goddess of plenty. It opened in November 2001, with galleries, theatres, a giant kitchen garden and a restaurant called Julia's Kitchen, backed by Julia Child herself. But the crowds never came, and it closed in 2008. Julia Child's cookware went to the Smithsonian! Today the Culinary Institute of America has a campus on the site, right by the Oxbow Public Market.

And across the river is one of the oldest buildings in the valley: the adobe house Cayetano Juárez built in 1840. He was a soldier under General Vallejo, and the name of his ranch, Tulucay, comes from a Patwin village. The adobe's been used as a restaurant.""",
'wine_train': """Keep an eye out for the Napa Valley Wine Train, which runs from Napa to St. Helena right alongside Highway 29. And believe it or not, this train went all the way to the California Supreme Court.

The tracks are old. Sam Brannan, our Gold Rush millionaire, started the Napa Valley Railroad in 1864 to haul tourists from the Vallejo ferries up to his hot-springs resort in Calistoga. Passenger service ended in 1929. Then in the 1980s, when Southern Pacific wanted to abandon the line, local entrepreneurs bought it for 2.5 million dollars to run a fancy tourist train with lunch and wine.

A lot of locals were not into it. They said the valley already had way too many visitors, and they got the state to demand a full environmental review. Quiz: who won? [[pause 4]] The train! In 1990 the state Supreme Court ruled four to three that no review was needed, because the line was already in use. Then they spent about twenty million dollars fixing the tracks. And the fight over how many tourists this valley can handle? Still going.""",
'yountville': """Coming up is Yountville, named after George Calvert Yount, and this guy's life was basically a Western movie.

Born in North Carolina in 1794, he fought in the War of 1812, then left his family in Missouri to become a fur trapper. He reached California in 1831, hunted sea otters off the Channel Islands, then worked as a carpenter for General Vallejo in Sonoma. Through Vallejo he got a huge land grant in 1836 and became the first permanent Euro-American settler in the Napa Valley. And in 1838, he planted the valley's very first grapevines. So, Yount: the guy who started all of this.

Here's a spooky one. Yount said that in the spring of 1847 he kept having the same dream, of pioneers struggling in deep snow. And a famous writer later claimed that Yount's dream helped bring about part of the rescue of the Donner Party. Whoa.

Quiz: the town was originally laid out in 1855 with a totally different name, and had to change it because another town had it first. What was it? [[pause 5]] Sebastopol! We'll actually meet the real Sebastopol later. Today almost a third of Yountville's residents live at the Veterans Home of California, founded in 1884, the biggest of its kind in the country.""",
'yountville.more': """Okay, foodies, this one's for you. Yountville is home to The French Laundry, one of the most famous restaurants in America. And yes, it really was a laundry. The stone building went up as a saloon in 1896. Then in 1906 a law banned alcohol near the Veterans Home, and in 1920 it became a French steam laundry.

In 1978 Sally Schmitt and her husband Don, who was the mayor at the time, turned it into a restaurant and kept the old name because locals still called it that. Sally was a pioneer of California cuisine, cooking with local, seasonal ingredients. Thomas Keller took over in 1994 and won three Michelin stars. And in 2020, it was all over the national news when Governor Gavin Newsom went to a dinner there during COVID restrictions. Oops.

Also here: Domaine Chandon, opened in 1973 by the Champagne house Moët et Chandon, the first French-owned bubbly producer in the Napa Valley.""",
'napa_geology': """Let's talk dirt! Because in this valley, the dirt is literally the product.

Shape first. Napa is a long, skinny trough between two mountain ranges, with a whole family of faults, including the West Napa Fault, slicing through and slowly sliding the land past itself.

Then: volcanoes! Between about eleven and three million years ago, this whole area was erupting. The leftovers are called the Sonoma Volcanics, lava, ash and broken volcanic rock, and the hills on both sides are full of it. There's even a low hill east of Napa that geologists think was a volcano rising up inside an old collapsed crater. Up toward the Mayacamas there's white pumice from an eruption nearly five million years ago, and glassy lava with swirly flow bands, about 5.3 million years old.

Then the creeks took over. Over the last few hundred thousand years they washed gravel and sand down out of those volcanic hills and spread it in fans across the valley floor. In the middle of the valley, around Oakville and Rutherford, there's a gravelly rise called the Rutherford Bench, where the soil drains really well.

So here's the takeaway, Julia and Adam: next time you sip a Napa Cabernet, you're partly tasting a volcano. Cheers to that.""",
'oakville': """Okay, coming up is Oakville, population about fifty. Tiny! But it's got a juicy family drama.

First, quiz: Oakville has one of Napa's most famous vineyards, planted in 1868 and named To Kalon. That's Greek. What do you think it means? [[pause 5]] The beautiful! The guy who planted it, H. W. Crabb, tested over 400 grape varieties to figure out what grew best here.

Now the drama. In 1965, Robert Mondavi had a huge falling-out with his younger brother Peter over the family winery, Charles Krug. So Robert walked out and built his own winery right here, the first big new winery in Napa since Prohibition, with part of that old To Kalon vineyard. It's the mission-style building with the big arch and the bell tower. Robert pushed the idea of naming wines after the grape, like Cabernet or Chardonnay, instead of borrowing French place names, and that became the standard all over the New World. He even rebranded unpopular Sauvignon Blanc as Fumé Blanc. Marketing genius.

And the ending? Forty years after the feud, Robert and Peter finally made a barrel of wine together. One barrel. It sold for 400,000 dollars! Across the highway is Opus One, Mondavi's partnership with the famous Baron Philippe de Rothschild of Bordeaux, which made the whole world take Napa seriously.""",
'rutherford': """Here's Rutherford, and its most famous estate was bought with money from The Godfather. Seriously. But let's start at the beginning.

The town's named after Thomas Rutherford, who married George Yount's granddaughter. In 1864 Yount gave the couple about a thousand acres, and they planted vines.

The big estate here is Inglenook, started in 1879 by Gustave Niebaum, a Finnish sea captain who made a fortune in the Alaska fur trade. He actually wanted to build his winery in France, but his wife hated long ocean voyages, so: Napa! Decades later, the film director Francis Ford Coppola bought the estate bit by bit, starting in 1975, with his profits from The Godfather. In 2011 he even bought back the Inglenook name, and he said the name cost him more than the whole estate.

Next door is Beaulieu Vineyard. Quiz time. When Prohibition shut down almost every winery in America in 1920, Beaulieu didn't just survive, it grew. How? [[pause 6]] Church wine! They landed a contract to supply sacramental wine to churches across the country, and demand went through the roof. By 1933 they were making over a million gallons a year. Holy moly.""",
'wappo_story': """Long before vineyards, this valley was Wappo country. Their homelands covered the Napa Valley, the south shore of Clear Lake, the Alexander Valley and the Russian River valley.

They lived in small, independent groups, hunting and gathering, in homes made of branches, leaves and mud. And their baskets were woven so tightly they could hold water. Acorns from the oaks were a staple, and the hot springs up at Calistoga were a place of healing.

I love the old Wappo place names. Quiz: the Wappo called the area around St. Helena Anakotanoma. What do you think it means? [[pause 5]] Bull Snake Village! Calistoga was Nilektsonoma, Chicken Hawk Place. And Mount Saint Helena was Kanamota: Human Mountain.

The name Wappo itself probably comes from the Spanish word guapo, which can mean brave. And they earned it: they fought off military campaigns by General Vallejo until a peace treaty in 1836. Sadly, what came next was devastating. From maybe one or two thousand people around 1770, the population fell to just fifty by 1880. Their language is gone now, though someone did write down its grammar. So when you see the name Caymus on a wine label, that's the name of a Wappo group who lived here first.""",
'st_helena': """Welcome to St. Helena, the heart of old Napa wine country, and quiz time! One of the valley's first great vineyards here came out of a very modern-sounding legal document. What do you reckon? [[pause 5]] A prenup! Charles Krug started his winery here in 1861, often called the valley's first. He married Dr. Bale's daughter, and her mum insisted on a prenuptial agreement that protected twenty acres north of town. And that's exactly where Krug planted his vines. Smart lady. Much later, the Mondavi family bought the Krug winery for 75,000 dollars.

Then there's Beringer, founded in 1876. It calls itself the oldest continuously operating winery in the Napa Valley. In 1934, right after Prohibition, it became the first California winery to offer tours and tastings. And in 1939 it invited Hollywood stars like Clark Gable and Carole Lombard, and handed out maps saying All roads lead to Beringer. Historians call that the birth of Napa wine tourism. So, basically, every tasting room you see? Blame Beringer.

On Main Street, look out for a massive stone building: Greystone Cellars, built in 1889 so small growers could store and age their wine instead of selling it cheap to dealers in San Francisco. Today it's the Culinary Institute of America.""",
'st_helena.more': """Here's one of the great accidents in wine history. Right on Highway 29 in St. Helena is Sutter Home. In 1948 the Trinchero brothers bought it and scraped by making cheap jug wine.

In 1972, Bob Trinchero started making a pale wine from red Zinfandel grapes. Then, in 1975, about a thousand gallons of the juice stopped fermenting before all the sugar was gone. Oops! He set it aside, tasted it two weeks later, and it was sweet, pink and, in his words, pretty good. Quiz: what famous wine had he just accidentally invented? [[pause 5]] White Zinfandel! By 1987 it was the best-selling premium wine in America. Wine snobs might sniff at it, but loads of people had their very first glass of wine thanks to this happy accident.""",
'phylloxera_prohibition': """Okay, the Napa crash story. By 1880, this valley was booming: hundreds of vineyards, and by 1900 more than 140 wineries. Then came three punches in a row.

Punch one was tiny. A bug called phylloxera, a louse that eats grapevine roots, killed vines all over the valley. The fix was planting vines on roots that the bug couldn't hurt.

Punch two: Prohibition, in 1920. Lots of wineries just closed. A few survived making wine for churches, and growers sold grapes to people making wine at home.

Punch three: the Great Depression.

The comeback was slow, helped by a French winemaker at Beaulieu, Beringer's tourism, and a teacher-turned-winemaker called Brother Timothy, whose smiling face sold Christian Brothers wine all over the country. Then in 1965, Robert Mondavi opened his winery, and the boom was back on.

And the twist? Quiz: what do you think happened in 1983? [[pause 5]] The bug came back! A new outbreak hit vines planted on a rootstock called AxR1, and growers had to replant about three-quarters of the affected vineyards by the late nineties. Now they're fighting a different bug, the glassy-winged sharpshooter. In wine country, the war with bugs never ends.""",
'bale_mill': """Here's a cool spot coming up: the Bale Grist Mill, with its giant 36-foot waterwheel. It's one of only two water-powered mills left west of the Mississippi. And there's evidence that the rebels of the 1846 Bear Flag Revolt met here before they marched on Sonoma!

It was built in 1846 by Dr. Edward Turner Bale, an English ship's doctor who became surgeon-in-chief of the Mexican army and married General Vallejo's niece. His land stretched all the way from Rutherford to Calistoga. Settlers came from across the valley to grind their corn and wheat here, and the old-timers swore the slow-ground meal made bread that put city bread to shame. Sadly, Bale tried his luck in the Gold Rush, caught a fever, and died in 1849.

Right next door is Bothe-Napa Valley State Park, home to the furthest-inland coast redwoods of any state park in California. Our first redwoods of the day!""",
'calistoga_wineries': """Okay, the road into Calistoga has some seriously over-the-top wineries.

First: Castello di Amorosa, an actual medieval-style castle, opened in 2007. It has 107 rooms, a moat, a drawbridge, a great hall with frescoes, and wait for it, a torture chamber with an iron maiden that the owner says he bought in Italy for 13,000 dollars. In the 2020 fire, the farmhouse burned, but the castle was fine. Of course it was. It's a castle.

Next: Sterling Vineyards, perched on a volcanic hill 300 feet up. Quiz! How do you get up to the winery? [[pause 4]] An aerial tramway! Like a ski lift. And the building looks like it was beamed in from the Greek island of Mykonos.

And Schramsberg, started in 1862 by a German barber called Jacob Schram, with cellars dug into the hillside. Robert Louis Stevenson visited in 1880 and tasted eighteen wines. Eighteen! Now they make sparkling wine.""",
'calistoga': """Welcome to Calistoga, at the top of the Napa Valley! Julia, Adam, this town has my favourite origin story of the day. Quiz: how do you think it got its weird name? Have a think. [[pause 6]] It was a slip of the tongue! Sam Brannan, our Gold Rush millionaire, visited the hot springs here in 1852, fell in love, and bought more than 2,000 acres to build a spa to rival the fancy Saratoga Springs in New York. The story goes he meant to call it the Saratoga of California, but it came out as the Calistoga of Sarafornia. True or not, the name stuck!

His resort opened in 1862, and his railroad arrived in 1868, bringing San Francisco's rich and famous to soak in the waters. The little depot he built is still standing. Long before that, this was Nilektsonoma, the Chicken Hawk Place, home to several Wappo villages around the hot springs.

And the hot water is legit. In 1920, a soda fountain owner called Giuseppe Musante was drilling for cold water and hit a hot spring instead. By 1924 he was bottling it, and Calistoga sparkling water became a national brand.

Very 2020s note: Calistoga now has a hydrogen fuel-cell and battery power plant that can keep the whole town's lights on for up to 48 hours when the power gets cut during fire danger.""",
'calistoga.more': """Here's a romantic one. In 1880, a broke, sickly Scottish writer showed up here with his new American wife. Quiz: who was he? He wrote Treasure Island. [[pause 4]] Robert Louis Stevenson! He'd crossed an ocean and a continent to marry Fanny Vandegrift Osbourne, and friends told him the mountain air up here would help his lungs.

They tried the fancy Hot Springs Hotel, but couldn't afford ten dollars a week. So they spent their two-month honeymoon squatting, with Fanny's twelve-year-old son, in an abandoned bunkhouse at an old silver mine called Silverado, up on Mount Saint Helena. Cloth over the windows, water hauled by hand, rattlesnakes. Romantic, right?

He wrote it all up in a book called The Silverado Squatters, where he used his very first telephone and called Napa winemaking an experiment. And a lot of his notes about this scenery ended up in the descriptions in Treasure Island. There's a state park named after him at the top of Highway 29, with a trail past where the cabin stood. On a clear day up there, you can see Mount Shasta, 192 miles away.""",
'judgment_paris': """Okay, this is the big one. The story that put Napa on the world map.

In the early seventies, some California wines were amazing, but nobody cared, because everybody wanted French labels. A British wine merchant in Paris, Steven Spurrier, set up a blind tasting for America's 200th birthday. On the 24th of May 1976, eleven judges, mostly French wine experts, tasted the best Chardonnays and Cabernets, French versus Californian, without knowing which was which. Spurrier assumed France would win.

Quiz! What happened? [[pause 5]] California won both! Top white: a 1973 Chardonnay from Chateau Montelena, just north of Calistoga. Top red: a 1973 Cabernet from Stag's Leap Wine Cellars, on the Silverado Trail. Time magazine ran the story, and it became known as the Judgment of Paris. A bottle of that Montelena is now in the Smithsonian, and there's even a 2008 movie about it, Bottle Shock.

And the plot twist? People are still arguing about the maths. A 2026 analysis found mistakes in the published totals, suggesting the white wine result was actually a tie with a French wine, and that by some counting methods, a French red was the judges' favourite. But the headline was written, and Napa was famous forever.""",
'fires_story': """Driving through these hills, you might spot blackened tree trunks, and brand-new houses where old ones used to be. Here's the story of the fires.

On the night of the 8th of October 2017, hot, dry winds were gusting up to seventy miles an hour, and more than a dozen wildfires broke out across Northern California. One of them started at 9:43 at night near Tubbs Lane, just north of Calistoga. The Tubbs Fire raced more than twelve miles in its first three hours, through the Mark West Springs area and right into Santa Rosa. It destroyed more than 5,600 buildings, half of them homes in Santa Rosa. At the time, it was the most destructive wildfire in California history. And here's an eerie detail: it followed exactly the same path as another fire back in 1964.

Then 2020 was brutal too. A freak lightning storm sparked hundreds of fires, and the Glass Fire started above St. Helena, destroying wineries, a three-Michelin-star restaurant, and a historic resort. Calistoga had to evacuate for the second time since 2017. All told, about sixty percent of the Napa Valley has burned since 2017.

And now it's a money story. Since about 2020, seven of California’s twelve biggest home insurers stopped renewing policies in high-risk areas. People piled into the state's insurer of last resort, from 124,000 homes in 2019 to 663,000 by March 2026. So when you see a shiny new house on a burned hillside, someone probably fought really hard to insure it.""",
}

if __name__ == '__main__':
    apply('content/02_napa.json', T)
