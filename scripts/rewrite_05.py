"""Persona rewrite for content/05_sonoma.json (same facts, warmer delivery, quizzes)."""
import sys
sys.path.insert(0, 'scripts')
from rewrite_lib import apply

T = {
'carneros_intro': """You're crossing Los Carneros, the rolling hills between the Napa and Sonoma valleys, right along the top of San Pablo Bay. Quiz: carneros is a Spanish word. Any idea what it means? [[pause 4]] Rams! As in sheep. Lots of sheep used to graze these hills, and the name goes back to a ranch from 1836.

Carneros has a cool claim to fame: it was the first wine region in California defined by its climate instead of by county lines. Being right by the bay, it gets fog and cool breezes, so it's cooler than the valleys further north. Perfect for Pinot Noir and Chardonnay, and for bubbly. Which explains the fancy French château on the hill: Domaine Carneros, started in 1987 by the Champagne house Taittinger, and modelled on their own château in France.

And keep an eye on these green hills. One of them might look very familiar. More on that shortly!""",
'di_rosa': """Hidden off this road is the di Rosa art centre, and the land has had quite a life.

In 1855 someone planted grapes and olives here. In 1886 two Frenchmen built a stone winery. Then the phylloxera bug killed the vines, and the old winery got used for growing mushrooms, making moonshine, storing grain, and finally as a hay barn.

In 1960, Rene di Rosa bought it, replanted vines and turned an old Depression-era pond into a 35-acre lake. When he sold the vineyards in 1986, he used the money to turn the whole place into an art park. Now it has about 1,600 works by Northern California artists, in galleries and a sculpture meadow, and the land is protected forever.""",
'bliss': """Okay, this is one of my all-time favourite stories. Julia, Adam: did you ever use a computer with Windows XP? Picture the default desktop picture. [[pause 4]] The green hill and the blue sky! It's called Bliss, and it might be the most viewed photograph in history. And it was taken right around here, near the Napa-Sonoma county line, on this very highway.

In January 1996, a former National Geographic photographer, Charles O'Rear, who lived in St. Helena, was driving to see his girlfriend. A storm had just passed, the winter rain had turned the grass bright green, and he spotted a hill that had been cleared of vines because of the phylloxera bug. He pulled over, set up his tripod, and took four shots. And he says he didn't edit it at all.

Microsoft bought the full rights in 2000. People have tried to recreate the shot ever since, but they can't. Quiz: why not? [[pause 4]] The hill went back to being a vineyard! So look out for green hills with vines on them. One of them is the most famous hill in the world, wearing a disguise.""",
'schellville': """This crossroads is Schellville, and it's got two railroads: a real one that floods, and a quarter-size one that one guy built by himself.

The real one first. Schellville has been a rail junction since 1888, with a two-mile railyard. Being low by Sonoma Creek, it floods every five to ten years. And in March 2023, after months of rain, the soggy ground gave way and a train full of corn seed derailed right here. Nobody was hurt.

Now the fun one. On the way into Sonoma is Sonoma TrainTown. Stanley Frank from Oakland started building it in 1958, and he made everything himself: the tiny houses, the landscaping, even the steam engines. Everything is exactly one quarter of real size. It opened in 1968, and his family still runs it: a twenty-minute ride past waterfalls and tiny houses, over a trestle and through tunnels, on four miles of track.""",
'sonoma_intro': """Welcome to Sonoma, where modern California kind of began!

Quiz: Spain built a famous chain of twenty-one missions along California. This town has the very last one, and the northernmost. And it's the only one not built by the Spanish. Who built it? [[pause 5]] Mexico! Mission San Francisco Solano was founded in 1823, just after Mexico won independence. And part of the reason was to keep an eye on the Russians at Fort Ross. Russians again!

When Mexico shut down the missions in the 1830s, a young officer called Mariano Guadalupe Vallejo was sent to turn this one into a town. In 1835 he laid out the plaza you'll see in the middle, the biggest town plaza in California. And the City Hall in the middle of it, dedicated in 1908, was built with four identical sides, so none of the shopkeepers around the square would feel snubbed. How diplomatic is that?""",
'sonoma_intro.more': """Across from the mission is the Blue Wing Inn, one of the first hotels north of San Francisco. It started with the very first property deal in the new town: Vallejo gave the lot to his manager, Antonio Ortega. The local priest soon complained about how Ortega treated the Native people, and after more scandals and some dodgy accounts, Vallejo fired him in 1837. Ortega stayed on anyway and ran a tavern there.

Then in 1849, in the middle of the Gold Rush, two guys bought it and turned it into a hotel, with a gambling hall and a saloon, serving miners heading to and from the gold fields and the American soldiers stationed here. Wild West vibes.""",
'bear_flag': """Okay, here's California's strangest little rebellion, and it happened right on Sonoma's plaza.

By 1846, Mexico had pretty much ignored California for years, and Mexican officials were nervous about all the Americans showing up uninvited. Those Americans, in turn, complained they couldn't buy land and were being threatened with getting kicked out.

So, early on the morning of the 14th of June 1846, about thirty-three American settlers rode into Sonoma and took General Vallejo prisoner. Here's the funny part: Vallejo actually liked the idea of American rule! He sat down to negotiate his own surrender, while, according to accounts, the rebels proceeded to get drunk. They raised a homemade flag with a grizzly bear and the words California Republic, and declared independence.

Quiz: how long do you think the California Republic lasted? [[pause 5]] About three and a half weeks! The Mexican-American War had already broken out, and on the 9th of July a U.S. Navy lieutenant raised the American flag in front of the Sonoma barracks, and that was that. But the bear flag survived: it became the basis of California's state flag. There's a monument on the plaza where it was first raised.""",
'vallejo_story': """Okay, one man pops up in almost every story on this side of the hills: Mariano Guadalupe Vallejo. Let's meet him properly.

He was born in Monterey in 1807, the eighth of thirteen kids of a Spanish soldier. As a boy he got private lessons from the governor, with access to his library, and an English merchant taught him English, French and Latin. In his twenties he was sent north to close the Sonoma mission and command the whole northern frontier. He became super powerful and super rich, with a ranch of 44,000 acres.

He was a man stuck between two worlds. In 1846, the Bear Flaggers took him prisoner, even though he was in favour of America taking over. Then he helped at California's first constitutional convention and served in the first State Senate.

Quiz: two Bay Area cities are named after Vallejo's family. One is Vallejo, obviously. What's the other? [[pause 5]] Benicia, after his wife, Francisca Benicia Carrillo! And just outside Sonoma, he built a wooden Gothic house that was made on the East Coast and shipped around Cape Horn in pieces. He called it Lachryma Montis, mountain tear, after a spring on the land. He lived there until he died in 1890, and you can still visit it.""",
'haraszthy': """Sonoma Valley calls itself the birthplace of the California wine industry, and here's the colourful guy who helps make that case: Agoston Haraszthy.

A Hungarian nobleman and adventurer, he'd already founded a village in Wisconsin, where the German settlers called him the Count, and been the first sheriff of San Diego. Then in 1857, just east of Sonoma, he founded Buena Vista, one of California's first successful commercial wineries. He's often called the father of California wine, and he brought in more than 300 kinds of European grapes. His money skills were less impressive, though. The bankers had to take over, and he was pushed out in 1866.

Next door, a Bavarian, Jacob Gundlach, planted a vineyard in 1858 called Rhinefarm. Gundlach Bundschu is now the oldest winery in California owned by the same family the whole time, six generations!

Quiz: when that nasty phylloxera bug was destroying vineyards all over California in the late 1800s, someone here in the Sonoma Valley figured out the fix. What was it? [[pause 6]] Grafting European vines onto tough, disease-resistant American roots. A grower called Julius Dresel did it first, commercially, and it saved the entire California wine industry.""",
'springs': """In 1943, ninety veterans of Guadalcanal were sent to a fancy resort here to recover with golf, cherry pie and dances. Here's the story.

North of Sonoma, the highway runs through a string of little towns known as the Springs: Boyes Hot Springs, Fetters Hot Springs, Agua Caliente and El Verano. Agua Caliente means hot water, and Native people used and considered these springs sacred long before anyone else showed up.

Quiz: in 1895, a Captain Boyes drilled down just 70 feet. What did he hit? [[pause 4]] 112-degree hot water! He built a resort hotel, which burned down in a wildfire in 1923. Its replacement became the Sonoma Mission Inn. And in World War Two, the Navy borrowed it as a rest centre for sailors and Marines back from the Pacific, including those Guadalcanal veterans. From one of the worst battles in history, straight to soft beds and cherry pie.""",
'sdc': """This one's a darker story, but an important one. Off to the west, near the village of Eldridge, are the grounds of the Sonoma Developmental Center, which for over a century was a big state institution for people with developmental disabilities. It opened here in 1891.

California passed a forced sterilisation law in 1909, only the third state to do so. From 1918, the superintendent here, F. O. Butler, was a big believer in it, and personally performed at least a thousand operations. The centre even admitted people just to sterilise them and send them home. It was said to have sterilised more people than any other institution in the world, and risky medical experiments on residents went on into the 1960s.

It finally closed at the end of 2018. Not every story on a road trip is a happy one, but this one's worth knowing.""",
'jack_london': """Up on the slopes of Sonoma Mountain, above the village of Glen Ellen, is the ranch of Jack London, and his life was as wild as his books.

Born in San Francisco in 1876, he was an oyster pirate in the bay as a teenager, sailed off to the Klondike gold rush at 21, and came back a committed socialist. Quiz: in 1903 he sold The Call of the Wild, one of the most famous books ever, to a magazine. How much do you think he got for it? [[pause 5]] 750 dollars!

In 1905 he bought an abandoned winery here and called it Beauty Ranch. Then he started building his dream house, Wolf House: 26 rooms, nine fireplaces, built of massive stone to survive earthquakes, with fancy new stuff like electric lights, refrigeration and even a built-in vacuum cleaner. He and his wife Charmian spent over 80,000 dollars on it. And then, on the 22nd of August 1913, just before they were due to move in, it burned down.

He was devastated, deep in debt, and he died at the ranch in 1916, aged just forty. His ashes are under a rock from the ruins of Wolf House. He also wrote a novel called The Valley of the Moon, a translation of the Native name for the Sonoma Valley. You can still walk to the stone ruins today.""",
'obsidian': """Here's something you could find in the gravel around here: natural volcanic glass!

The geology maps around Glen Ellen and Kenwood show a layer called the Glen Ellen Formation: river gravel made mostly of eroded volcanic rock, famous for its pebbles of obsidian. Up in the hills there's a lava called the Rhyolite of Adobe Canyon, glassy and grey-white with swirly folded bands, about 5.3 million years old.

Nearby Annadel State Park's whole history is written in this rock: Native Americans used its obsidian, and then, quiz, in the early 1900s people quarried its volcanic rock for something you've definitely walked on. What? [[pause 5]] Cobblestones! And some biologists say Annadel has the best untouched oak woodland anywhere.""",
'kenwood': """This next town tried on more names than a teenager tries on outfits.

Kenwood sits on an old Mexican ranch called Los Guilicos, granted in 1837 to a Scottish sea captain who never even lived on it. In 1850 he sold it to another Scot, William Hood, a cabinet-maker who'd climbed the mountain above the valley, fallen in love with the view, and made his fortune building houses in Gold Rush San Francisco to afford it. The mountain's now called Hood Mountain.

When the railroad arrived in 1887, the town tried Rohrerville, then Los Guilicos, then South Los Guilicos. Quiz: why do you think people wanted to change it again? [[pause 4]] Nobody could pronounce Guilicos! So around 1895 they voted for Kenwood. Either because settlers came from Kenwood in Illinois, or because English families knew Kenwood House in London. Maybe both!

Up to the north-east is Sugarloaf Ridge State Park. When the state planned to close it in 2011 to save money, a group of volunteers called Team Sugarloaf took it over and reopened it. They even run an observatory up there.""",
}

if __name__ == '__main__':
    apply('content/05_sonoma.json', T)
