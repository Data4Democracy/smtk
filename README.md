## SMTK (Social Media Tool Kit)

#### **DISCLAIMER:**
This is a very early stage work in progress experiment. Contributions, ideas, thoughts, opinions are welcome. If you are looking for a fully fleshed out, well documented codebase you may be uncomfortable working on this project (for now). The upside is there is a lot of work to be done and this is a great opportunity to make substantial contributions.

## Purpose:
Collecting social media data can be a nuisance. This project aims to make the collection process as simple as possible for researchers. We make common-sense assumptions about what most researchers need, and how they like to work with their data. SMTK sits on top of other python libraries such as facepy (facebook) and python-twitter (twitter) to provide researchers with a clear and easy way to interact with various social media API's. Our purpose is to take care of low level details and provide a clean API for working across multiple platforms. As we build out our core functionality we hope to do even more work to abstract out annoying tasks like scheduling tasks, handling API limit breaches/timeouts so your collections keep running in a robust fashion.

## Philosophy:
Our goal is to make it as **easy as possible** for researchers to get up and running with new collections. Our focus is on ease of use over features. At every decision point we carefully consider how a new feature will impact simplicity. A user should be able to use our toolkit without prior knowledge of underlying libraries and APIs. Based on our experience of underlying API we will attempt to make the best decision that should work in average case but if you are looking for maximum control over your collection process, consider using underlying libraries/API endpoints directly.

This project aims to use the most current version of python 3.6. Back porting to previous versions is a secondary concern and not guaranteed.

## What we are not:
We do not offer every available endpoint on every platform. We have distilled this down to the ones we've found to be most useful in our previous research. If you need more functionality consider using the underlying libraries/API endpoints directly. At the moment our core library is considering platforms which offer an API. We may consider adding support for scraping platforms which do not offer an API in the future.

## Background:  
SMTK grew out online community research we are doing at [Data for Democracy](https://github.com/Data4Democracy). Some early inspiration came from [collect-social](https://github.com/Data4Democracy/collect-social), [discursive](https://github.com/Data4Democracy/discursive) and [twitter-framework](https://github.com/bstarling/twitter-framework). Thanks to all the early contributors to these projects, much of the code and functionality found here was directly inspired these early projects.

## Structure:  
SMTK core provides classes which interact with the social media API endpoints / python API wrappers to create the appearance that data is being streamed to the user.

Every platform will have a base Collector (Ex:`CollectTwitter`) which offer a variety of commonly performed tasks. These start with basic functions like get a users friends list but will also include more advanced functions like `map_network` which starts with a list of seed accounts and begin crawling through a seed user(s) network returning connection, friends and posts as it goes.

All collection classes should implement several `on_<event>` methods (`on_start`, `on_post`, `on_profile` are common ones). This is how data is "returned" (streamed) to the user of smtk. By inheriting from our base class users of the library are able to build their own logic on top of our functionality. This is done to separate the code which obtains the data from logic to route, parse and/or store the data.

This project is still in an experimental phase. If you have experience with similar projects/domains we welcome suggestions.

## Vision/Roadmap  
Our goal is to implement core functionality for the common social media platforms then once we have a good baseline we will move to building pre-packaged implementations. Our extensions/implementations of core functionality will make it easy to start up a collection. SMTK will take care of creating a database to store results and offer pre-set configuration options which will require little more than a user's API credentials. We also hope to offer multi-platform functions such as combining youtube links embedded in tweets with metadata returned by the YouTube API. Finally we plan to build a command line interface and eventually a web UI.

Platforms:
* Twitter
* Facebook
* Reddit
* Disqus
* Youtube

Interesting in contributing? Please join us in #assemble and checkout our [contributors guide](./CONTRIBUTING.md) and join us in our slack channel [#assemble](https://datafordemocracy.slack.com/messages/assemble/)

#### Code Examples  
```python
from smtk.fourchan import ChanMonitor

board = 'pol'
chan = ChanMonitor(board)
chan.follow() # loops continuously looking for thread updates
```

ChanMonitor provides four methods you can override to code to your specific needs.  
* `on_status` : called each time an api update is received  
* `on_archive` : called each time a thread is archived (replies no longer allowed)  
* `on_loop_complete` : called each time poll of all active threads is complete  
* `on_start`: called once at startup  

In order to actually do something with the updates inherit from `ChanMonitor`
and override above methods. Eventually we will provide these superclasses so users do not have to hand code them.  
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

[Here](https://github.com/bstarling/fourchan_monitor) is an example of the chan monitor feeding our [Eventador](https://github.com/bstarling/assemble/tree/master/eventador) hosted kafka cluster.
