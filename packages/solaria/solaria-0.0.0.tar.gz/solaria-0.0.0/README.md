[![Solaria Logo](resources/solaria_logo.png)](https://github.com/cqpancoast/solaria)

Solaria is an API for creating [interactive storytelling](https://en.wikipedia.org/wiki/Interactive_storytelling) modules, with a focus on managing non-linear narratives.
These modules can either sit inside larger storytelling programs and manage a non-linear narrative, such as with an MMORPG like World of Warcraft, or tell a story pretty much on their own, as with a text-based game like Zork.

There are two kinds of modules that Solaria can create:
- a *reading*, which tells a story by interacting with one (or more!) reader(s). It takes as input reader actions within a story world that could potentially affect the path of a narrative, and outputs, roughly, events that occur due to this and all previous actions.
- a *writing*, which lets a writer write a story by creating and configuring a reading. It takes as input configurations to a reading and outputs some representation of the current state of the reading-precursor.
