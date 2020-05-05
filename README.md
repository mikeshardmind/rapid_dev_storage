# Don't use this yet

No seriously, it's not documented, and it shouldnt be used without more consideration.

I'll do a release and have things documented by the time it is ready for use.

### Why?

Because there are many situations in which a small app may need to store data and not want to commit to a full DB design from the outset.
Many solutions for this incur tradeoffs, this one is one I would consider "not terrible"

Everything in it is designed to be replacable, from how things get stored on disk, to what gets used for serialization, with defaults which should work reasonably well for the intended use.

### What this isn't

A replacement for a proper database and queries, or an ORM handling all of that for you

### What this is

An abstraction around storing "some number of identifiers" mapping to "some easily serialized types" without a concrete schema.

This is great for not thinking about certain things specific to DBs, but it makes a few concessions and is less performant than using the right tool for the job. This is a tool for rapid development scaffolding.

### Quickstart

(TODO)


### I want to use it now!!

If you want to mess with this before it is ready for use...


```py
# python3.8 -m asyncio
>>> from rapid_dev_storage import SQLiteBackend, Storage
>>> backend = await SQLiteBackend.create_backend_instance(":memory:", "test", 1)
>>> store = Storage(backend)
>>> await store.get_group("Test")["some_id", "some_other_id"].set_value(42)
>>> await store.get_group("Test")["some_id", "some_other_id"].get_value()
42
```

There's more work and documentation to be done here, but if you use it exactly as it's intended currently, it will probably work for you. I still can't recommend using it yet.
