"""Persona rewrite for content/04_berryessa.json (same facts, warmer delivery, quizzes)."""
import sys
sys.path.insert(0, 'scripts')
from rewrite_lib import apply

T = {
'i505': """Fun fact: the road you've just turned onto used to have a letter in its number! This is Interstate 505, a quiet four-lane road running about thirty miles up the edge of the valley to Interstate 5. Basically, it lets people skip Sacramento entirely.

It was originally planned as part of a loop called I-5W, W for west. Then the feds scrapped almost all the lettered interstates and chopped I-5W into pieces. One piece became the stretch of I-80 you just drove, and this piece became 505. The northern end only opened in 1977.

That ridge to your left is the Vaca Mountains. The flat ground you're on is gravel and sand washed down out of them, plus a few patches of a layer called the Tehama Formation, old river mud and volcanic ash from a few million years ago.""",
'winters': """Coming up is Winters, a cute little town on Putah Creek, right where it comes out of the hills. And it's one of the places where farming in the whole Sacramento Valley got started.

In 1842, a Kentucky guy named William Wolfskill was granted a ranch along this creek, and his brother John started planting orchards and vineyards here. He's credited with kicking off farming in the entire Sacramento Valley.

Quiz: the town is named Winters. Was that because of the weather? [[pause 4]] Nope! It's named after Theodore Winters, whose ranch provided half the land for the town. Not very wintry at all. And in 1935, the Wolfskill family gave a hundred acres of the old ranch to UC Davis for an experimental orchard. Now we leave the freeway and follow Highway 128 west, up the creek, into the hills.""",
'putah_creek': """See that creek next to the road? That's Putah Creek, and its name has caused some drama.

Quiz: the early spelling of this creek's name got rejected by the federal government. Why do you think? [[pause 5]] It looked like a rude word in Spanish! Old maps spelled it Puta Creek, and the naming board said, no thank you. The experts say the resemblance is totally accidental, and the name actually comes from the Lake Miwok words for grassy creek. The Patwin call it Liwaito.

And it's a feel-good environmental story too. After a drought in the late 1980s, most of the creek below the dams dried up completely. That led to a big lawsuit, and in 2000 everybody signed the Putah Creek Accord, which guarantees water releases that copy the natural seasons. And it worked: the number of streamside bird species doubled, and native steelhead trout and Chinook salmon came back to spawn. While the farmers kept their water too. Everybody wins!""",
'berryessa_fires': """These dry, grassy canyons burn a lot. Highway 128 has been closed by fire again and again.

Quiz: in July 2015, the Wragg Fire started right next to this highway. What do you think started it? [[pause 5]] The hot exhaust of an idling car touching dry grass. That's all it took. It forced 136 homes to evacuate and closed this road and the freeway. Then there was the Winters Fire in 2017, and the Quail Fire in 2020.

And in August 2020 came the big one. A super-unusual series of thunderstorms, fed by moisture from a dying tropical storm, sparked fires all over Northern California. Around here alone there was one near Monticello Dam, one near the Putah Creek bridge, one at Spanish Flat and one north of the lake. With firefighters stretched across the whole state, they all grew and merged into the LNU Lightning Complex, which burned over 363,000 acres across five counties.""",
'monticello_dam': """Okay, look up the canyon! That's Monticello Dam, a 304-foot concrete arch jammed into a narrow gorge called Devil's Gate. It's a hundred feet thick at the bottom and only twelve at the top. And when they poured the last bucket of concrete in February 1957, the crew tossed in a few coins for luck.

But the coolest thing about it is hidden. Quiz: when the lake gets too full, how does the extra water get out? [[pause 5]] Through the Glory Hole! It's a giant concrete funnel in the lake, 72 feet across, dropping 200 feet straight down through the hillside. When the lake's full, water pours into it like the world's biggest bathtub drain. It doesn't happen often: in 2017 it overflowed for the first time since 2006, then again in 2019. And it's genuinely dangerous: in 1997 a woman was pulled in and killed.

Behind the dam is Lake Berryessa, the biggest lake in Napa County, about sixteen miles long with 165 miles of shoreline. Fun detail: the dam and lake are completely in Napa County, but the dam is less than 500 feet from two other counties.""",
'monticello_town': """Here's something kind of haunting. Under Lake Berryessa there's a whole town.

This valley used to be a ranch belonging to the Berryessa family, which is where the lake gets its name. They lost it fast. Quiz: by 1853 they owed a guy 1,645 dollars and couldn't pay. So the county auctioned off 26,000 acres. What do you think it sold for? [[pause 5]] 2,000 dollars! And the buyer flipped it for 100,000. Brutal.

In 1866, developers laid out a town called Monticello. Farmers poured in, growing wheat and barley on what was considered some of the best soil in the country. It had hotels, blacksmiths, a general store, and in 1896 a beautiful three-arched stone bridge, the biggest stone bridge west of the Rockies.

Then in 1947 the government decided to build a dam. The residents protested, but the governor backed it, and the town was doomed. The famous photographer Dorothea Lange documented its death for Life magazine, although Life never ran the story. Buildings were knocked down, the cemetery was moved up to a bluff called Spanish Flat, and the post office closed in 1956. But that old stone bridge? It was built so well they couldn't easily demolish it. So they just left it. It's still down there, under the water.""",
'great_valley_rocks': """Okay, geology moment! Every road cut along here is a page from the bottom of a dinosaur-age sea.

The layered sandstone and shale you're passing is the Great Valley Sequence, the same old sea floor that's buried miles deep under the flat valley behind us. Here it comes up to the surface. The geological maps show formations with names like the Sites, the Venado and the Yolo. Near the dam, the Venado even has a layer of giant jumbled blocks at the bottom.

Quiz: how do geologists know how old the Yolo Formation is? [[pause 5]] Microscopic fossils! Tiny sea creatures in the mudstone date it to the late Cretaceous, roughly 88 million years ago. Back then, sand and mud were pouring down underwater canyons off ancient volcanoes and settling on the deep ocean floor. So every time we pass a road cut, you're looking at the bottom of a sea from the age of the dinosaurs.""",
'ophiolite': """Keep your eyes on the road cuts! Look for a colour change: greenish, shiny, slippery-looking rock, and thin, scrubby plants. That's something pretty rare.

The geological maps say this stretch of Highway 128 crosses the Coast Range Ophiolite. Quiz: an ophiolite is a slab of something you're normally never supposed to see on land. Any idea what? [[pause 5]] The ocean floor! An ophiolite is a chunk of ocean crust, plus a piece of the Earth's mantle underneath it, shoved up onto a continent. The rock here started as peridotite, which comes from the mantle, and seawater forced deep into it turned it into serpentinite. This slab is Jurassic, and it's called arguably the biggest ophiolite in the United States.

And the soil from it is tough on plants: low in calcium, high in heavy metals like chromium and nickel. That's why the slopes look so bare, and why the area is home to rare plants that grow nowhere else.""",
'berryessa_monument': """Here's a national monument that deliberately left out its own lake. Because of jet skis!

The wild hills around Lake Berryessa are part of the Berryessa Snow Mountain National Monument, created by President Obama in July 2015. It stretches about a hundred miles north into Mendocino County, with bald and golden eagles, black bears, mountain lions and tule elk. And people have lived in these hills for around 11,000 years: Patwin, Pomo, Wappo, Lake Miwok, Yuki and more.

A whole coalition of counties, cities, a Pomo tribe and conservation groups campaigned for it. But boaters worried that a national monument might one day ban their motorboats and jet skis, so the lake was left out. Then in May 2024, President Biden added nearly 14,000 acres, including an eleven-mile ridge called Molok Luyuk.""",
'franciscan_sage': """Okay, here's California's geological junk drawer: the Franciscan Complex, and much of the Coast Ranges from here to the ocean is made of it.

For tens of millions of years, an ocean plate was diving under North America, and as it went down, it scraped off a crazy mix of stuff: deep-sea sandstone, chert full of tiny fossils, ocean-floor basalt, and chunks of rock that got dragged deep underground, squeezed under enormous pressure, then popped back up. Geologists call it an accretionary wedge, and the Franciscan is the textbook example.

Quiz: there's a rock in here called mélange. That's French for mixture. What do you think it looks like? [[pause 5]] A fruitcake! Blocks of chert, greenstone, serpentinite and blueschist floating in a squished, muddy matrix. And blueschist is a rare blue rock that only forms deep in a subduction zone, at high pressure but low temperature. So if you spot a blue-grey shiny rock in a road cut later today, you might be looking at old ocean floor that went down into the Earth and somehow came back. And look closely at the geology maps: these hills are dotted with mapped landslides.""",
'hennessey': """This little lake lent its name to the fire at the heart of California's seventh-largest wildfire complex. Here's the story.

This is Lake Hennessey, the City of Napa's main water supply. Congress approved a dam here in 1944 but never paid for it, so in 1946 the city just built it themselves, for 550,000 dollars. It's named after Edwin Hennessey, a local leader who helped get it done.

Early on the morning of the 17th of August 2020, a lightning strike started a small fire on Hennessey Ridge Road near the lake. The Hennessey Fire grew to 192,000 acres all by itself, the heart of the LNU Lightning Complex.

Now a fun one. Hidden in the hills to the north is Pope Valley. Quiz: a scene from a James Bond movie was filmed in the sky above it in 1978. Which movie? [[pause 5]] Moonraker! The opening skydiving sequence. Not bad for a sleepy little valley. Nearby is Chiles Valley too, where Joseph Chiles planted vines back in 1850.""",
'solano_water_story': """California's history is basically a history of moving water around, and Lake Berryessa is a textbook case.

The farms of Solano and Yolo counties had been worked since the 1840s, but the summers were bone-dry. As early as 1907, Bay Area cities hired a group of engineers to look at damming Putah Creek, but they moved on to bigger projects. Then in 1947, the county and the federal Bureau of Reclamation launched the Solano Project, with Governor Earl Warren pushing hard, to water 96,000 acres of prime farmland.

Quiz: Lake Berryessa can hold 1.6 million acre-feet of water. How much do you think flows in each year? [[pause 5]] About 375,000 acre-feet. So refilling it from empty would take more than four years' worth of inflow. Downstream, a smaller dam sends water through a canal to farms and to the taps of Vallejo and Benicia.

The cost fell on the people of the valley, who lost their whole town, and on the creek itself, which ran dry below the dams in the late eighties until the lawyers sorted it out in 2000. It's a small version of the deal behind every big California water project: the cities and farms win, somebody's valley gets flooded, and the fish wait for the lawyers.""",
}

if __name__ == '__main__':
    apply('content/04_berryessa.json', T)
