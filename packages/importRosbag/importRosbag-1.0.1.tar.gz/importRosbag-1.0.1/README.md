# importRosbag
Import rosbag data - pure python - standalone - no ROS installation required.

The importRosbag function imports a .rosbag file. Use the 'filePathOrName' 
parameter to supply the path. e.g. 

```
import os
from importRosbag.importRosbag import importRosbag

prefix = 'C:/' if os.name == 'nt' else '/home/sbamford/'    
filePathOrName = os.path.join(prefix, 'data/rpg/shapes_rotation.bag')

topics = importRosbag(filePathOrName=filePathOrName)
```

A rosbag consists of a set of topics, each of which has a set of messages.
A topic has a name, which was defined by the creator, and a message type, which
is standard and defines the content of each message. 
This function uses the topic types to interpret the messages from each topic, 
yielding one dict for each topic. Each of these dicts contains an iterable for 
each data field.

By default this function unpacks all topics for which it has a message type 
definition, but you can use one of the following keyword params to limit which 
topics are intepretted:

* 'listTopics' = True - no unpacking - just returns a list of the topics contained in the file and their associated types - use this to quickly inspect the contents of a bag;
* 'importTopics' = <list of strings> - only imports the listed topics;
* 'importTypes' = <list of strings> - only imports the listed types.

Example usage:

```
# Import everything
topics = importRosbag(filePathOrName=filePathOrName)

# Or just list the topics in the bag
topics = importRosbag(filePathOrName=filePathOrName, listTopics=True)

# Or just import one particular topic
importTopics = ['/dvs/camera_info']
topics = importRosbag(filePathOrName=filePathOrName, importTopics=importTopics)

# Or just import two particular types - Note that slash and underscore are interchangable
importTypes = ['esim_msgs_OpticFlow', 'geometry_msgs/PoseStamped']
topics = importRosbag(filePathOrName=filePathOrName, importTypes=importTypes)
```

Message types supported are a selection of standard message types, plus a couple 
related to event-based sensors:

Standard:

* geometry_msgs/PoseStamped
* geometry_msgs/Transform
* geometry_msgs/TransformStamped
* geometry_msgs/TwistStamped
* sensor_msgs/CameraInfo
* sensor_msgs/Image
* sensor_msgs/Imu
* sensor_msgs/PointCloud2
* tf/tfMessage

Specialised:

* dvs_msgs/EventArray
* esim_msgs/OpticFlow

The method of importation is honed to the particular needs of the author, 
sometimes ignoring certain fields, grouping data in particular ways etc. 
For example, from the CameraInfo message type we import only a single message 
because we're not currently interested in autocalibration or its results.
However this code should serve as a model for anyone who wishes to import rosbags.
Although it's possible to import messages programmatically given only the message 
definition files, we have chosen not to do this, because if we did it we would 
anyway want to take the resulting data and pick out the bits we wanted. 

Timestamps: We convert timestamps to 64-bit floats. This won't work for you if you 
care about sub-microsecond precision, for any timestamps encoded as unix time. 

Quaternions: Attention! If you import any of the types which encode rotations as
quaternions, e.g. PoseStamped/Transform/TransformStamped/tfMessage: we import 
quaternions in the form w,x,y,z, which is the convention in certain software, 
like blender; however, in the rosbag, the native form is x,y,z,w. 


Dependencies:

* numpy
* tqdm

