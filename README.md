**3d Loved Ones

This is a Python app that controls a batch of Raspberry Pi's. Each RPi is running Linux that auto logs onto the local wifi. There is a client Python app running upon startup listening for events over a socket connection. When it receives the "snappic" command, it takes a picture and then sends it back to the server which saves them into a common folder. 

All cameras fire simultaneously to capture an object from all angles. These are then fed into photogrammetry software like MeshRoom or better yet, RealityCapture. This does the work to convert it into a 3d model.

---


