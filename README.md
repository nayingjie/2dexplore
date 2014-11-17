2dexplore
=========

A pygame 2d exploring game.

Installation
============

For Linux, download the game, unpack it anywhere you like, and run 'run.sh' script.
For Windows, also, download it and run 'run.bat' script

The game requires Python 2.7.x and compatible pygame 1.9.0 corresponding to python version.
Recommended Python version is 2.7.8 and it can be found [here](https://www.python.org/downloads/release/python-278/)
Also, you can download pygame [here](http://www.pygame.org/download.shtml) (be sure to choose the proper version for your platform.)

How-To
======

Keys:
-----

[W] [A] [S] [D] - move  
[SHIFT] + [W] [A] [S] [D] - break block in direction of moving  
[X] - break block standing on.  
[Z] - place block (if in inventory or god mode).  
[E] - explode (god mode only)  
[1] - scroll inventory  
[ESC] - reset map  

Debug:
------

[F1] - God Mode (infinite inventory, flying)  
[M] - spawn Entity  
[N] - despawn Entity  

Game is autosaved, the file name is 'explore_save.gz' in working dir.  
For saving format, see world.py.  
