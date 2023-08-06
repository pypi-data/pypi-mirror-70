# MouseTools

A Python wrapper for the Disney API. Data is pulled directly from Disney. This package supports Walt Disney World and Disneyland.


### Installation
You can install using pip:
```bash
pip install MouseTools==2.0.0b5
```
or because version 2.0.0 is in beta right now and might be updated frequently:
```bash
pip install git+https://github.com/scaratozzolo/MouseTools
```


### Example usage:
The first time you load MouseTools in any project, it will take a while to load as the initial database is set up and created. There is a lot of data to load and parse so just be patient. After this it shouldn't take as long as syncing takes less time.
```python
import MouseTools

wdw_dest = MouseTools.Destination(80007798)
print(wdw_dest.get_park_ids())

# sync_on_init means sync the database with Disney on object instantiation. Default is True.
# This parameter is helpful when creating many objects back to back as syncing only once is necessary.
dlr_dest = MouseTools.Destination(80008297, sync_on_init=True)
print(dlr_dest.get_attraction_ids())

mk = MouseTools.Park(80007944)
print(mk.get_wait_times())

pirates = MouseTools.Attraction(80010177)
print(pirates.get_wait_time())
# Returns a list of other possible attraction ids
print(pirates.get_possible_ids())

```

For more documentation go to the [wiki](https://github.com/scaratozzolo/MouseTools/wiki) or run the following command from a termainal:
```Bash
python -m pydoc MouseTools
```


I created this project to help with another project found [here](https://github.com/scaratozzolo/WDWWaits). Some parts of the wrapper were created with that in mind.

As I said above, this is currently a beta and not everything has been tested. If you notice any issues please open a new issue with a "bug" label. Furthermore, if you have any feature requests, open a new issue with a "feature request" label.

This update would not have been possible without the work being done on the [themeparks package](https://github.com/cubehouse/themeparks). A lot of this update has inspiration taken from this.
