"""Persona rewrite for content/03_russian_river.json (same facts, warmer delivery, quizzes)."""
import sys
sys.path.insert(0, 'scripts')
from rewrite_lib import apply

T = {
'mt_st_helena': """Look north, everyone. That big mountain closing off the top of the valley? That's Mount Saint Helena. It has five peaks in a rough letter M, the Napa River starts on its slopes, and it's one of the few mountains around the Bay Area that actually gets snow.

Okay, quiz, and this one's a curveball. The Wappo called it Human Mountain, and the Spanish called it Mount Mayacamas. But the name it has today came from a completely unexpected country. Which one? [[pause 6]] Russia! In 1841 a Russian survey party from Fort Ross, out on the Sonoma coast, climbed to the top and left a copper plate with the name of Princess Helena de Gagarin, the wife of the fort's commander. So this mountain, and very likely the town of St. Helena, are named after a Russian princess. How cool is that?

And it's volcanic, with an explosive past. Its eruptions sent avalanches of hot ash rolling across this landscape, and one of them, as you're about to hear, turned an entire forest to stone.""",
'petrified_forest': """Coming up on, wait for it, Petrified Forest Road, is the Petrified Forest. About 3.4 million years ago, an eruption from the direction of Mount Saint Helena buried a forest of giant redwoods in volcanic ash. And over thousands of years, those trees turned to stone. Stone trees!

Quiz! The biggest one, nicknamed The Queen, is eight feet wide and 65 feet long. How old do you think she was when the volcano got her? [[pause 5]] About 2,000 years old! And here's the twist: these redwoods prove that redwoods used to grow way further inland than they do now.

Fun history too. Robert Louis Stevenson visited on his 1880 honeymoon and wrote that it was owned by an old Swedish ex-sailor who stumbled on it while clearing land. There's even a stone tree named after Stevenson. A woman named Ollie Orre Bockee bought the place around 1912 for 14,000 dollars, charged tourists fifty cents a head, and her family's run it ever since. In 2023 it went up for sale. Want to guess the price? [[pause 4]] Twelve million dollars. Anyone have that on them?""",
'volcanoes_story': """Here's a fun fact to blow your minds: you're crossing the Mayacamas Mountains, and almost everything around you was once molten.

The rock is called the Sonoma Volcanics: obsidian, pumice, ash, and lava, several thousand feet thick. It makes up most of the mountains around the Napa and Sonoma valleys, and it erupted from several vents, on and off, mostly between three and five million years ago. It's also what a lot of the wine-country soil is made of. So: lava wine. Kind of.

And the volcano story isn't over! To the north, around Clear Lake, is a volcanic field that last erupted only about 11,000 years ago, and the U.S. Geological Survey rates its threat as high. Its heat powers a place called The Geysers, up in these mountains: the largest geothermal field in the world, with eighteen power plants running on underground steam. In 2019 it made about a fifth of California's renewable energy.

Native people built steam baths there for something like 12,000 years. In the 1850s it became a fancy resort that drew Ulysses Grant, Teddy Roosevelt and Mark Twain. Quiz: there's one big problem with the name The Geysers. What is it? [[pause 5]] There are no geysers! The steam vents are actually fumaroles. The guy who named it in 1847 got it wrong, and nobody ever bothered to fix it.""",
'mark_west': """Okay, here's a hero story. On the night of the 8th of October 2017, the Tubbs Fire came racing down this exact valley from Calistoga, heading for Santa Rosa. And nearby is Safari West, a 400-acre wildlife preserve with giraffes, rhinos, cheetahs, around 800 animals in all.

Quiz: the owner, Peter Lang, was 76 years old. When the fire came, what do you think he did? [[pause 5]] He stayed. All night. He fought the flames by himself for more than ten hours, with nothing but garden hoses. And not a single animal died. What a legend.

This is the Mark West Springs area, named after a Scottish-American pioneer called William Marcus West, and the creek you're following runs nearly thirty miles from the mountains to the Russian River. Down the hill, the community of Larkfield-Wikiup lost about 500 homes in that fire, and just two years later, in 2019, another fire pushed right up to its edge again. A lot of what you're seeing has been rebuilt since.""",
'utopias': """The hills north of Santa Rosa have attracted some real dreamers. Let me tell you about two of them.

In 1875, a religious leader called Thomas Lake Harris brought his followers, the Brotherhood of the New Life, here from New York to found a colony called Fountain Grove. He named his mansion Aestivossa, which he said meant high country of divine joy, in a language only he understood. And he insisted his real palace was in interspace. As you do. Meanwhile, his practical right-hand man, Nagasawa Kanaye, ran 2,000 acres of vineyards. Today Fountaingrove is a fancy neighbourhood.

Then in 1894, about thirty Christian socialists founded a commune in these hills called Altruria, inspired by a utopian novel. They grew orchards and sold their produce in San Francisco. Then they built a hotel. Quiz: how long do you think utopia lasted after that? [[pause 4]] Not long! The hotel sank them, and by 1896, every Altrurian settlement was abandoned. Turns out paradise is expensive.""",
'fulton_laguna': """Coming up: a giant natural sponge! This is the Laguna de Santa Rosa, a 22-mile wetland that drains most of the Santa Rosa plain. In heavy winter rain it spreads into a shallow lake that can soak up more than 80,000 acre-feet of floodwater.

It's the wildest place in Sonoma County, the most biologically diverse, with over 200 kinds of birds, bald and golden eagles, otters, mink and bobcats, plus three endangered plants that grow nowhere else. Sadly it's also been hammered by more than a century of farming and building, but people have been restoring it since the 1990s.

And a nerdy little twist. Mark West Creek, which we followed down the hills, has been diverted in three places, so now it looks like the creek feeds the Laguna, when naturally it's the other way round. Sneaky.

Oh, and the tiny place you're passing is Fulton, founded by the brothers Thomas and James Fulton, with a post office since 1871.""",
'russian_river_intro': """Woohoo! Welcome to the Russian River, everybody, the last leg of our journey. It's the second-biggest river in the Bay Area, 115 miles long, flowing south out of Mendocino County and then west to the Pacific.

Quiz! Why do you think a river in California is called the Russian River? [[pause 5]] Because of actual Russians! In the early 1800s, the Russian-American Company ran a fur-trading colony at Fort Ross on the coast, and one of their explorers, Ivan Kuskov, travelled up this river. An 1817 Russian map calls it the Slavyanka. But long before that, the Southern Pomo called it Ashokawna, the east water place, and Bidapte, big river.

This is also the Russian River Valley wine region: cool, foggy country thanks to the nearby ocean, which is perfect for Pinot Noir and Chardonnay. By 1900 there were nearly 200 wineries around here. And before the vines? Redwoods, lining the banks. You'll see them close in as we head downstream. Get ready for the trees!""",
'el_molino': """Here's a quick one. Right around here, near Forestville, was California's first commercial water-powered sawmill. It was built in 1834 by John Bautista Rogers Cooper, a sea captain who'd married General Vallejo's sister. The Mexican government gave him this land partly as a strategy: get settlers out here to keep an eye on the Russians at Fort Ross.

The mill ran on Mark West Creek and cut redwood. Quiz: how long do you think it survived? [[pause 4]] About seven years! Floods destroyed it in the winter of 1840. The river always wins around here.

Forestville itself was settled in the late 1860s, originally spelled with two r's after one of its founders. And by 1900 it had a reputation as a hangout for bohemian writers and artists.""",
'river_floods': """This lovely, lazy river has a wild side. Flood stage here at Guerneville is 32 feet. Quiz: the record flood, in February 1986, went way past that. How high do you think it got? [[pause 5]] 49 and a half feet! Seventeen feet over flood stage. And in the second half of the twentieth century the river flooded about five times a decade. Two big dams upstream now hold back a lot of that water, but in February 2019 it got almost as high as in 1986.

And here's a water fight brewing. Some of this river's summer water doesn't even belong to it! Since 1908, a tunnel up in Mendocino County has been borrowing water from a totally different river, the Eel River, and sending it into the Russian. That borrowed water helps supply drinking water to more than 600,000 people in Sonoma and Marin. But in 2019 PG&E decided the old hydro plant wasn't worth keeping. The Eel River dams are going to be removed, and everyone downstream is trying to figure out how to keep some of that water coming.""",
'korbel': """Okay, wine lovers, up ahead is a winery that legally prints the word champagne on its labels, and France can't do anything about it.

It's Korbel, making sparkling wine here since 1882. It was started by Francis Korbel and his brothers, who came from Bohemia, and who also, randomly, started a satirical San Francisco magazine called The Wasp. They use the proper Champagne method, where the wine gets its second fermentation right in the bottle you buy.

So how do they get away with saying champagne? [[pause 4]] Old American rules from the 1930s treat some place names as semi-generic, as long as the label also says where the grapes were really grown. And a 2006 deal with Europe protected older American brands that were already using it. Somewhere, a Frenchman is wincing. Korbel makes about 1.6 million cases a year now.""",
'rio_nido': """Here's one of my favourite little places: Rio Nido, the river nest, a tiny resort village tucked into a redwood canyon. It was started in 1908 by a San Francisco lodge called the Eagles, so its first name was Eaglenest. In World War Two, its dance hall was packed with sailors on leave and big bands played there.

Okay, Julia, Adam, here's a weird one. The streets here are named Canyon One, Canyon Two, Canyon Three, Canyon Four, then Canyon Six and Canyon Seven. What's missing? [[pause 4]] There's no Canyon Five! The story goes it's because of an accident on the road that became Canyon Six. Spooky.

And the town's unofficial slogan? The Moon Is Always Out In Rio Nido. Love that.""",
'guerneville': """Ladies and gentlemen, Julia, Adam and our amazing driver: welcome to Guerneville! You made it! Woohoo!

Okay, pronunciation check. It's Gurn-vill. Locals even sell T-shirts that say Don't call it Guerneyville. So now you know.

Final quiz of the trip. The town's very first English name was a bit less pretty. Given that loggers cut down most of the giant redwoods here in the late 1800s, what do you think they called it? [[pause 5]] Stumptown! And the parade every year is still called Stumptown Days. The redwoods grew so thick here that local legend says the valley had the densest amount of living stuff on the planet. Then the loggers came, especially after the 1906 earthquake, when San Francisco needed rebuilding. Today's forests on the hills are mostly less than 200 years old, regrown after all that logging.

Before all of that, the local Pomo used this spot as a summer camp and called it Ceola, the shady place. The name Guerneville comes from George Guerne, a Swiss guy who owned the sawmill. In 1877 the railroad arrived and the town became San Francisco's summer playground. Then in the late seventies, gay entrepreneurs from San Francisco discovered it and brought it back to life, and it's been a famously welcoming town ever since.

Thanks for riding with me today, gang. You've been a great audience. Go enjoy those redwoods!""",
'guerneville.more': """If you've got an hour, go see the trees that the loggers missed: Armstrong Redwoods, just north of town. In the 1870s, Colonel James Armstrong saved the grove as a natural park. After he died, his daughter and another local family ran a whole campaign, with rallies and car caravans, to save this last bit of the old forest, and in 1917 the county bought it for 80,000 dollars.

Quiz: the tallest tree in there, the Parson Jones Tree, is a hundred yards from the entrance. How tall do you think it is? [[pause 5]] More than 310 feet! That's taller than a thirty-storey building. And the oldest, the Colonel Armstrong Tree, is over 1,400 years old. There's an easy trail through the grove, wheelchair-accessible too. Totally worth it.""",
'bohemian_grove': """Okay, conspiracy fans, this one's for you. Just downstream at Monte Rio, hidden in the redwoods, is the Bohemian Grove: a 2,700-acre private campground owned by San Francisco's very exclusive Bohemian Club. Every July, powerful people from politics, business and the arts spend more than two weeks camping here.

It started innocently. In 1878, a bunch of journalists from the club had an overnight going-away party in the redwoods for an actor moving to New York. They had so much fun they did it again the next year, without him! Then the rich businessmen joined, and the money and the power followed.

Quiz: in 1942, something top-secret was planned at the Grove. What do you think it was? [[pause 6]] An early planning meeting for the Manhattan Project, the atomic bomb! And in 1950, Dwight Eisenhower and Richard Nixon met for the first time here, at a lunch hosted by Herbert Hoover.

No woman has ever been a full member. And the secrecy creates legends. In 2000, the broadcaster Alex Jones sneaked in, filmed the club's Cremation of Care ceremony, and called it a ritual sacrifice. Other reporting doesn't support that, and another filmmaker who saw the same footage said it looked more like an overgrown frat party. Fun fact: one of the camps inside is called Silverado Squatters, after Stevenson's book!""",
'pomo_story': """This river is Pomo country. The Pomo lands once stretched from the Pacific coast all the way inland to Clear Lake. But here's the thing: the Pomo were never one single nation. They lived in small, independent bands linked by family, and they spoke seven related languages so different that speakers of one couldn't understand another.

Quiz: the name Pomo was originally the name of just one village. What do you think it meant? [[pause 5]] Those who live at red earth hole! Probably after the red magnesite they mined to make beads, or the reddish soil. By 1877, English speakers were using it for everyone.

The Southern Pomo, who lived along this lower river, were the first to be hit by Spanish colonisation, and were even used as labour to build the last of the California missions, in Sonoma. By 2012, there was just one fluent speaker of Southern Pomo left. But since 2011 the Dry Creek Rancheria has been bringing it back, with classes, a phone app, and signs on their ancestral land. And their old Coyote stories even mention the beavers that used to dam this river.""",
}

if __name__ == '__main__':
    apply('content/03_russian_river.json', T)
