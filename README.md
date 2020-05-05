# Don't use this yet

No seriously, nothing in here is ready or tested yet.
I'll do a release and have things documented by the time it is.

### Why?

Because there are many situations in which a small app may need to store data and not want to commit to a full DB design from the outset.
Many solutions for this incur tradeoffs, this one is one I would consider "not terrible"

### What this isn't

A replacement for a proper database and queries, or an ORM handling all of that for you

### What this is

An abstraction around storing "some number of identifiers" mapping to "some easily serialized types" without a concrete schema.

This is great for not thinking about certain things specific to DBs, but it makes a few concessions and is less performant than using the right tool for the job. This is a tool for rapid development scaffolding.

### Quickstart

(TODO)
