# Gravity Rig add-on
Thank you for downloading the Gravity Rig addon. 

## About 
This add-on is intended to take over the tedious process of making rigs react to gravity. 

## How it works
You define a guide for the mesh you want to deform, just like you would place an armature. Instead, you place vertex and edges (faces are ignored and loops will be interpreted in a seemingly random fashion). You can start with a cube or plane and merge its vertices into one. Then extrude them so as to follow the inside of the mesh you want to rig.
The shape of the guide can be made of disointed edges. Single vertices will be ignored. 
In order to know which vertices to consider the "pins" in our rig, we use a reference object. Vertices closest to the origin point of that object will be considered as "roots". There will be one root per ensemble of vertices joined by edges. The reference object can be whatever. An empty, a lamp... 
The guide will be added a cloth simulator, and an empty will be created and parented to each of its vertices. A rig will follow those empties.
When the cloth deforms, the empties follow and the rig follows the empties. Parenting your mesh to that rig will have it deformed according to gravity.
Of course you can adjust the cloth simulation to your liking. However, the pin group is automatic. All root vertices have a weight of 1. "Leaf" vertices will have a value as set in the add-on's interface. Vertices in between will be set to an intermediate weight. Weights can be later edited in the relevant vertex group.

The cleanup work in the following manner:
* select the mesh you want to remove the rig of and click on cleanup
* if you have removed the mesh and are stuck with assets you'd rather remove, click on cleanup. The add-on will detect orphan rigs and remove them

## Known issues
Need to better undertsand workflows so as to make it more useable
Some Python warnings to take care of
Weight attribution could be other than linear
Bone number capabilty is probably limited
We may need to parent the first bone of a chain to the first empty of that chain. Otherwise the empty is useless.
When something is parented to rig, it tends to break the logic

## Special thanks
Leander on blenderstackexchange for a snippet of code that helped.
Alimayo Arango and Tommy Oliver 3D who taught the method on which the add-on is based.
Everyone posting questions and answers on Blender and Python.

## The author
I'm a Blender hobbyist by night and a developer by day. 
You can follow Kiskit 3D on Youtube. 