## SMTK (Social Media Tool Kit)

#### **DISCLAIMER:**
This is a work in progress experiment. Contributions, ideas, thoughts, opinions are welcome. If you are looking for a fully fleshed out, well documented codebase you may be uncomfortable working on this project (for now). The upside is there is a lot of work to be done and this is a great opportunity to make substantial contributions.

## Purpose:
Collecting social media data can be a nuisance. This project aims to make the collection process as simple as possible for researchers. We make common-sense assumptions about what most researchers need, and how they like to work with their data. SMTK sits on top of other python libraries such as facepy (facebook) and python-twitter (twitter) to provide researchers with a clear and easy way to interact with various social media API's. Our purpose is to take care of low level details and provide a clean API for working across multiple platforms.


## Philosophy:
Our goal is to make it as **easy as possible** for researchers to get up and running with new collections. Our focus is on ease of use over features. At every decision point we carefully consider how a new feature will impact simplicity. A user should be able to use our toolkit without prior knowledge of underlying libraries and APIs. Based on our experience of underlying API we will attempt to make the best decision that should work in average case but if you are looking for maximum control over your collection process, consider using underlying libraries/API endpoints directly.

This project aims to use the most current version of python 3.6. Back porting to previous versions is a secondary concern and not guaranteed.

## Background:
SMTK grew out online community research we are doing at [Data for Democracy](https://github.com/Data4Democracy). Some early inspiration came from [collect-social](https://github.com/Data4Democracy/collect-social), [discursive](https://github.com/Data4Democracy/discursive) and [twitter-framework](https://github.com/bstarling/twitter-framework). Thanks to all the early contributors to these projects, much of the code and functionality found here was directly inspired these early projects.

## Roadmap:
* Twitter
* Facebook
* Disqus
* Youtube
* Create ready to go setup/configuration

Interesting in contributing? Please join us in #assemble and checkout our [contributors guide](./CONTRIBUTING.md) and join us in our slack channel [#assemble](https://datafordemocracy.slack.com/messages/assemble/)

#### Using 4chan API

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
    print("Thread is no longer active")
```
