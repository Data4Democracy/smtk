## SMTK (Social Media Tool Kit)

create a 4chan Monitors:

```python
board = 'pol'
chan = ChanMonitor(board)
chan.follow() # loops continuously looking for thread updates
```

ChanMonitor provides three methods you can override to code specific logic for each event.
* `on_status` : called each time an api update is received
* `on_archive` : called each time a thread is archived (replies no longer allowed)
* `on_loop_complete` : called each time poll of all active threads is complete
* `on_start`: called once at startup

In order to actually do something with the thread updates inherit from `ChanMonitor`
and override above methods

```python
class DemoChan(ChanMonitor):
  def on_start(self):
    print("Hey I am starting now!")
  def on_loop_complete(self):
    print("The loop just finished processed 200 active threads!")
  def on_status(self, thread):
    print("Print {}".format(thread.id))
  def on_archive(self, thread):
    fake_function_to_json_dump_and_save_file(thread)
```
