# FakeDB
Just a quick and dirty way to persist dictionaries for Python 3.2 or higher.  Can persist data as either json, bson, or hjson.  Conflict resolution is performed with a revision key, blocking a write if an existing document and a modified version do not have matching revision keys.

```python
from fakedb import FakeDB

db = FakeDB()
data = {"content":"hello world!"}
db.write(data, "test")

data = db.read("test")
data["content"] = "foo bar"
db.write(data, "test")
```
