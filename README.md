## mtg

Console-based access to the [Gatherer Magic Card Database](http://gatherer.wizards.com).

### Motivation

I'm not going to lie: I look up a lot of Magic cards.  Sometimes I
want to see the art, but usually I just want to know what the card
does.  There are plenty of web-based search engines, but even modest
queries can involve manipulating many form elements when, really, all
you want to do is type it out.  Thus: mtg.

### Documentation

Mtg is a command-line tool.  It accepts a number of arguments that
specify what cards you are looking for.  There are a number of
conventions it relies on to make complex queries remain compact.  The
best way to learn these is to read some examples.

#### Simple Queries

Search for cards by name.  Any positional arguments passed to mtg are
assumed to be part of the card's name.  This lets you look up any card
with:

```
$ mtg ancestral recall

------------------------------
Ancestral Recall U
Instant
Text: Target player draws three cards.
Limited Edition Alpha (Rare), Limited Edition Beta (Rare), Unlimited
Edition (Rare)
```

All other search filters are achieved with options.  For example, to find all white cards with "gideon" in the name, you use:

```
$ mtg gideon --color=w
```

To specify colors, use the one-letter abbrevations: w, u, b, r, g.
You may also specify "c" for colorless:

Filter by card text.  A string of comma separated terms searches cards
containing all terms, not the exact phrase.  For example, to find all
green cards that mention flying, use:

```
$ mtg --text=flying --color=g
```

Note that a text search _includes reminder text_.  If you are confused
about why your search for "flying" is returning creatures with Reach,
this is why.

To search for an exact phrase, make sure to put the text in quotes:

```
$ mtg --text='destroy all creatures'
```

Filter by type.  Mtg does not distinguish between subtypes,
supertypes, and plain old types.  Mix and match, any order you want,
whatever.  Put them all on `--type` argument and you'll get what you
want.

```
$ mtg --text='destroy all creatures' --type=instant
```

#### Combining terms

Sometimes, you want to search for more than one thing.  Give mtg a comma separated list and it will return only cards that match both words (logical _and_).

For example, find all artifact goblins:

```
$ mtg --type=goblin,artifact
```

All cards that mention flying and islandwalk:

```
$ mtg --text=flying,islandwalk
```

If you want results to match either term (logical _or_), use the
pipe character to separate words:

```
$ mtg --type='nautilus|oyster'
```

Note: many terminals require you to enclose a pipe character in quotes
or escape it with a backslash for mtg to properly interpret it.

You can combine the _and_ and _or_ opreators by combining commas and
pipes.  The following query will return all snow cards that are either
mtg --type='snow,zombie|goblin|aurochs'

#### Multicolored Cards

Searching for multicolored cards is sometimes tricky, so there are a
few more options to help you out.

First, you don't need to comma-separate the color letters.  The search

```
$ mtg --color=w,g
```

is equivalent to

```
$ mtg --color=wg
```

Both will find cards that are white and green.

Similarly, to find cards that are white plus either blue _or_ green,
the comma is optional, and you use the pipe operator as normal:

```
$ mtg --color='w,u|g'
```

is equivalent to

```
$ mtg --color='wu|g'
```

Lastly, to exclude unselected colors, there is a `-xc` flag.  To find
cards that are white-green and no other colors, use:

```
$ mtg --color=wg -xc
```

#### Numbers

Sometimes you want to find a card based on a numeric field.  Right now
you can do that for these three: power, toughness, and converted mana
cost.

To find a card where the number matches exactly, just search as you
would normally.  For example, to find all 4/4 goblins, use:

```
$ mtg --type=goblin --power=4 --tough=4
```

You can also use the inequality operators greater-than (>) and
less-than (<).  Also allowed are greater-than-or-equal-to (>=) and
less-than-or-equal-to (<=).  Note again most shells require you to
escape pointy bracket characters.  To find goblins even bigger than
4/4, use:

```
$ mtg --type=goblin --power='>4' --tough='>4'
```

Searching by converted mana cost is the same, though we use the
helpful abbreviation "cmc."  To find all angels that cost two or less,
use:

```
$ mtg --type=angel --cmc='<=2'
```

You can also combine these with the _or_ operator.  To find angels
that cost either two or less or nine or greater, use:

```
$ mtg --type=angel --cmc='<=2|=>9'
```

#### Negation

If you want to specifically exclude something from the results, you
can use the _not_ operator: `!`.  This is helpful for weeding out junk
you don't want.  For example, to find all angels that are not white:

```
$ mtg --type=angel --color='!w'
```

You can also combine this in the usual way.  To find angels that are
not white but are either blue or colorless, use:

```
$ mtg --type=angel --color='!w,u|c'
```

#### Other search fields

Rarity uses the following abbreviations:

 * `c`: common
 * `u`: uncommon
 * `r`: rare
 * `m`: mythic rare
 * `s`: special (Timeshifted cards)
 * `l`: land

E.g., all mythic rare goblins:

```
$ mtg --type=goblin --rarity=m
```

Searched can be limited to sets or blocks using the full name of the
set or an abbreviation, e.g. all alternate win conditions not from
unhinged or unglued:

```
$ mtg --text='win the game' --set='!unhinged,!unglued'
```

Or, all white commons from Innistrad:

```
$ mtg --color=w --rarity=c --set=inn
```

#### Display options

The output of "mtg" is customizable to a certain degree.  Add the
flags below to format the results to your liking.

`-r`: Show reminder text.  Normally reminder text is hidden, because most people using this program are super-geniuses who know all the rules.  But sometimes it's helpful!  For example, what did "banding" do again?

```
$ mtg timber wolves -r
```

`--hidesets`:  Hide the list of what sets the card has been printed in.  Sometimes, you just don't care about this.  Especially for basic land!  Breathe a breath of fresh air with this:

```
$ mtg --type='basic,!snow' --hidesets
```

`--rulings`: Show the card rulings.  Note: this only works if there is exactly 1 search result.  I'm (slowly) working on fixing this.
