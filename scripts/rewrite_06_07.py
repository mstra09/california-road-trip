"""Persona rewrite for content/06_santa_rosa.json and 07_north_sonoma.json."""
import sys
sys.path.insert(0, 'scripts')
from rewrite_lib import apply

SR = {
'santa_rosa': """Welcome to Santa Rosa, the biggest city in California's wine country! And it has a creek with a pretty grim name. Let me explain.

Before Europeans arrived, the Santa Rosa plain belonged to a powerful Pomo group called the Bitakomtara. They controlled it tightly: outsiders needed permission to pass through, and if they didn't ask, the penalties were harsh. They gathered for ceremonies on Santa Rosa Creek, near today's Spring Lake. Colonisation brought violence, enslavement and smallpox, and devastated them, though their descendants still live in the region.

The first European home here was built in the 1830s by María López de Carrillo, a widow from San Diego, whose daughter had married General Vallejo. Quiz: before she arrived, settlers from Sonoma used to slaughter cattle where two creeks meet, and one creek got named after it. Matanza means what in Spanish? [[pause 4]] Slaughter! So that's Matanzas Creek. Lovely. In the 1850s her son helped lay out the downtown grid around a central square, and the city still follows it.""",
'burbank': """Near downtown Santa Rosa is the house and garden of Luther Burbank, one of the most famous plant breeders who ever lived. And Julia, Adam, there's a really good chance you've eaten his work.

He was born in Massachusetts in 1849, the thirteenth of fifteen kids. As a young man he bred a new potato, sold the rights for 150 dollars, and used the money to move to Santa Rosa in 1875. Inspired by Charles Darwin, he crossed plants on an enormous scale and created more than 800 varieties: the Shasta daisy, the Santa Rosa plum, a white blackberry, a spineless cactus for cattle.

Quiz: a natural variant of his potato became the most widely grown potato in the United States. And a big share of one very famous fast-food chain's french fries are made from it. Which chain? [[pause 5]] McDonald's! The Russet Burbank is the classic french fry potato. So next time you have McDonald's fries, say thanks to Luther. He's buried in his garden here, under a cedar tree.""",
'schulz': """Okay, Peanuts fans! Santa Rosa was home to Charles Schulz, the creator of Charlie Brown and Snoopy. He grew up in Minnesota, the son of a barber, loved ice hockey, and moved out here in 1958. He kept drawing Peanuts right up until he died in 2000.

In 1969 he and his wife built an ice rink here, and everyone calls it Snoopy's Home Ice. Quiz: what do you think the café inside the rink is called? [[pause 5]] The Warm Puppy! Every summer it hosts Snoopy's Senior World Hockey Tournament for older players from around the world.

Down the street is the Charles M. Schulz Museum, with a 22-foot mural made of 3,588 Peanuts comic strips that together make a picture of Lucy holding the football for Charlie Brown.

And here's my favourite Santa Rosa coincidence. Schulz's very first published drawing, in 1937, was of his family dog Spike, who ate pins, tacks and razor blades. He sent it to Ripley's Believe It or Not, and they ran it! And Robert Ripley, who created Believe It or Not? Born right here in Santa Rosa.""",
'ripley': """Believe it or not, Robert Ripley was born right here in Santa Rosa, in 1890. He left high school after his dad died, started drawing sports cartoons for newspapers at sixteen, and moved to New York in 1913. In 1918 he drew his very first Believe It or Not cartoon, all about weird facts and feats, and readers loved it. They started mailing him their own oddities: funny-shaped vegetables, strangely marked pets, you name it.

He took his facts seriously enough to hire a full-time researcher. And by 1929 the panel was running in 360 newspapers in 17 languages, followed by radio and TV shows. Quiz: Ripley also held a sports title. Which sport? [[pause 5]] Handball! He was New York State handball champion in 1926. Believe it or not. A perfect Santa Rosan for a day full of oddities.""",
'rodgers_creek': """Okay, a little earthquake talk. Somewhere under this part of Santa Rosa runs one of the most dangerous faults in the Bay Area.

You've probably heard of the Hayward Fault, under Berkeley and Oakland. Well, this side of the bay has its partner: the Rodgers Creek Fault, running right through Santa Rosa. In 2016 scientists showed the two are actually connected under San Pablo Bay, making one fault about 120 miles long, from north of Healdsburg all the way to San Jose. It's the kind of fault where the ground on the other side slides sideways, to your right.

Quiz: on the evening of the 1st of October 1969, Santa Rosa got hit by not one, but how many earthquakes, about an hour and twenty minutes apart? [[pause 4]] Two! Magnitude 5.6 and 5.7. Chimneys fell, sidewalks buckled, pipes burst, and one person died. The damage was worse than expected, and modelling suggests the city sits where a basin full of sediment amplifies the shaking. Luckily it was evening, so few people were on the streets. Afterwards the city started earthquake-proofing its old brick buildings.""",
}
NS = {
'knights_valley': """Over the hill from Calistoga, Highway 128 drops into Knights Valley, a small, quiet valley with the warmest climate in Sonoma County.

In 1843 the Mexican governor rewarded a soldier from the Sonoma garrison, José de los Santos Berreyesa, with almost 18,000 acres, which included this valley and even the hot springs at Calistoga. Quiz: what do you think he used this beautiful valley for? [[pause 4]] His own private hunting preserve! And the adobe hunting lodge he built is still standing.

The English name comes from Thomas Knight, a guy from Maine who'd been one of the Bear Flag rebels in Sonoma in 1846. He bought a big chunk of the ranch, and his name stuck.""",
'chalk_hill': """Chalk Hill has a secret: there's no chalk. The hills to the south-west are the Chalk Hill wine area, named after one prominent hill. Quiz: so what's the white stuff in the soil really? [[pause 4]] Volcanic ash! White tuff, from the eruptions of the Mount Saint Helena area, the same volcanism that turned the Petrified Forest to stone. It's said to be great for white grapes, and there's a warm band of air here, so harvest often comes in September, weeks before the neighbours.

A bit further on, along Alexander Valley Road, the maps show a basalt lava flow and that obsidian-studded Glen Ellen gravel again. These are some of the last outposts of the big volcanic field, before the land turns to the old sea-floor rocks closer to the coast.""",
'alexander_valley': """You're entering the Alexander Valley, the big, vine-filled valley of the Russian River north of Healdsburg. It's the largest and most fully planted wine region in Sonoma County, with more than a hundred wineries.

The story starts with a ranch called Sotoyome, almost 49,000 acres, named after a Wappo group. It went to Henry Fitch, a San Diego sea captain who was General Vallejo's brother-in-law. Fitch never lived here. He hired a manager, Cyrus Alexander, with a deal that after four years, Alexander would get a chunk of land and some cattle. Alexander settled down, and the valley took his name, even though the American land commission later rejected his claim to it. Ouch.

Quiz: Alexander's replacement as ranch manager was the brother of a very famous Wild West frontiersman. Who? [[pause 5]] Kit Carson! His brother Mose Carson ran the ranch after 1845.

And a wine note: Jordan winery here, with its French-style château from 1976, had a long-time winemaker who was trained by André Tchelistcheff, the Beaulieu legend from Rutherford.""",
'healdsburg': """Healdsburg is named after a squatter, and it gave the world lemon pepper. Seriously.

It sits on the Russian River where three famous wine regions meet: the Alexander Valley, the Dry Creek Valley and the Russian River Valley. The Pomo built villages along the river here. The name comes from Harmon Heald, an Ohio businessman who squatted on the land from 1850, then bought a piece of it in 1857 when the owners auctioned off land to pay their taxes. The railroad arrived in 1872. And when Prohibition shut the wineries of Dry Creek Valley, which had been one of California's top Zinfandel regions, a lot of the land was switched to plums and prunes.

Quiz: what famous seasoning was first developed commercially here in 1967? It's in the title. [[pause 3]] Lemon pepper! Thanks, Healdsburg.

If you cross the old steel bridge into town, that's the Healdsburg Memorial Bridge from 1921, one of only thirteen bridges of its design in the whole country. People have been crossing the river at this exact spot since the 1850s, and the beach next to it is still a favourite swimming spot.""",
'healdsburg.more': """Here's a strong woman for you: Isabelle Simi. Simi Winery was started in San Francisco in 1876 by two Italian brothers who'd come for the Gold Rush, and they moved it here in 1881, paying 2,250 dollars in gold coins. From 1904, Giuseppe Simi's daughter Isabelle ran it, and she kept making wine right through Prohibition, storing it in the stone cellars. So when Prohibition ended in 1933, Simi was one of the only wineries with wine ready to sell. Clever. And in 1973 Simi hired Maryann Graf, the first woman to graduate from an American university with a degree in winemaking.

Just north of town, Lytton has had a wild run: a luxury resort in 1872, then a boys' military school, a sanitarium, and for decades an orphanage. In 2017, the Lytton Band of Pomo Indians bought it back for around 30 million dollars, after years of trying to recover land they'd lost.""",
'windsor': """Quiz: the town of Windsor, coming up, got its name from a Pony Express rider. Why do you think he chose Windsor? [[pause 4]] He thought the countryside looked like the grounds of Windsor Castle, back in his home country of England! He was Hiram Lewis, the first postmaster, in 1855. Long before that, it was a Southern Pomo village called Tsoliikawai, which means blackbird field.

Windsor had a rough start to the 1900s: a fire wiped out the town centre in 1905, then the 1906 earthquake damaged buildings that were still being repaired. In World War Two, the army built an air base on the south side of town, now the Charles M. Schulz airport. And in 1943 there was even a camp here for German prisoners of war.""",
'westside_blueschist': """Westside Road is one of the prettiest drives in wine country, winding along the river through some of the most celebrated Pinot Noir country in California. Cool, foggy, gorgeous.

But check out the rocks too. The geology maps show this road crossing old sea-floor sandstone that got dragged down into the Earth in a subduction zone, squeezed at huge pressure, and turned blue with a mineral called glaucophane, then somehow made it back to the surface. It's called blueschist, and it's rare all over the world. Quiz: why do you think it's so rare? [[pause 5]] Because it can only form deep in a subduction zone, and then it has to find its way all the way back up to the surface. Further along you'll pass mélange, that fruitcake rock, and old river gravels on flat benches cut into the bedrock.

So on this lovely, winding road, you're driving over bits of an ancient ocean floor that went down into the Earth and came back up.""",
}

if __name__ == '__main__':
    apply('content/06_santa_rosa.json', SR)
    apply('content/07_north_sonoma.json', NS)
