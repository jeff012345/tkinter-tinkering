# -*- coding: utf-8 -*-
from dot import Dot
from scene import Scene

try:
    scene = Scene()
    
    dot1 = Dot(scene, 100, 100)
    dot1.draw();
    
    scene.run();
except Exception as err:
    print(err)

