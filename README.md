# Platform Game

This program is a platform game that is made using the pygame library.
The objective is simple: Move your character throughout the platforms and
window to reach the coin at the top. Be sure to avoid the moving enemies
otherwise you will lose.

With the exception of various constants, the game is highly customizable.
By modifying the spritedata.txt and surfacesdata.txt input files, the user
can change the location, sizes, and appearance of the platforms and ground.
Additionally, the player can modify the appearance, trajectories, speeds,
and spawn locations of the player sprite and enemies. The user can also add and 
remove enemies and platforms by adjusting these input files.

Be sure to pass in the input files as command line arguments when running the 
game. For example, on Windows the command line input would be as follows:

python main.py surfacesdata.txt spritedata.txt
(If the order of the input files is changed the program will not run properly)

The surfacesdata.txt file is formatted such that the data to represent the ground
is on the first line in the file. The following lines represent the data for the platforms. 
They are referred to as shelves in the program. The data is as follows:

x location | y location | width | height | landing point/ground threshold | image

(Note: In pygame, all objects are represented as rectangles and (0,0) is the top left corner)

The landing point is the vertical location of the platform that the player sprite's y 
coordinate should be set to in when landing on a platform. For the ground, if the player
sprite's y coordinate exceeds the ground threshold, the y coordinate is immediately set to
the ground's y coordinate. This is used for when the player sprite is falling towards the ground 

In the spritedata.txt file, the first line represents the data for the character controlled
by the user. The second line is for the coin. The remaining lines contain the data for the 
enemies. The data is formatted as follows:

Main Character and coin:
x spawn point | y spawn point | width | height | image

Enemies:
x spawn point | y spawn point | width | height | horizontal velocity | vertical velocity |
Leftmost position on predefined path | Rightmost position on predefined path | highest position
on predfined path | lowest position on predefined path | image

I created the artwork for the game using Google Drawing. (Admittedly, I am not an excellent artist)
However, I would be interested in seeing this game with some more professional artwork.

I am always looking to improve this game so feel free to let me know of any changes that could be made!
