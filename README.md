# SuikaFruit

A puzzle game where you drop balls in a bag and merge them !

It's more addictive than it looks like.

***
## Vocabulary :

- Ball / Fruit : An object that can be throw in the bag and merge with another object with the same name.
- Merge : When 2 fruits collide to become a bigger fruit.
- Bag : The place where alll the fruits goes.
- Fruitopedia : Give the name, size, weight and given score of each fruit.
- Account / profile : Some data about player's previous games, current level, etc.
- Experience : Gained at the end of a game. Use to level up player's profile.
- Power : A capacity that allow player to usually modify a fruit. Can change the current of the game !
- Skin : A different appearance of a fruit. To give them funny aspect.
- Current fruit : The fruit that is about to be drop.
- Next fruit : Will become the new current fruit after the current one will be drop.

***
## Rules :

- You have to connect or create an account before playing (might change that in the futur).
- You can only drop one fruit at a time.
- Fruits can only merge with fruits with the same name (name depends of the current skin).
- The bigger a fruit get, the heavier it is.
- The skins doesn't change the fruit's attributes, hitbox or gameplay, just it appearance.
- A power will cost score and can be use once (Must be buy again to be reuse).
- Difficulty "Impossible" only allow to drop the 4th first smallest fruit (instead of 5).

***
## Prerequisites :

- Python 3.11.1 or below
- Python interpreter
- Librairies :
	- copy : 		Use to make copy of object without altering them.
	- math : 		Use to make mathematical operations (squareroot, degrees, exponential, power).
	- mutagen : 	Use to get a music file length.
	- os : 			Use to access and rename files and create directories and files.
	- PIL : 		Use to open, manipulates or apply filter on images.
	- pymunk : 		Use to add physics in the game (gravity and collisions). 
	- pygame : 		Use to manage the whole program interface.
	- random : 		Use to randomly create numbers or randomly choose an element in a list (like ball).
	- string : 		Use to get the alphabet.
	- sys : 		Use to safely close game.
	- time : 		Use to get current time or use and manipulate time formats.
	- webcolors : 	Use to transform and manipulate color names and rgb values.

***
## Installation guide

- Click on the green "<> Code" button
- On Local/SSH/, click on "Download as zip"
- Choose a location for the program in your machine
- Unzip the files
- With your python interpreter, launch the file "main.py"
- The game can start !

***
## User guide

#### Methods
- [RETURN] "Play" : Launch the game.
	- Connexion : Connect or create your profile
		- "Player" : Choose a pseudonyme. Just click on backspace once to erase 'Player'.
    	  Can be 'One Shot' (me), 'OneShot666' (my profile), 'Player' (default pseudo) or 'Bot'.
    	  Please don't use any bad words.
		- "Banners" : Personnalize your banner ! Choose 2 colors and the direction to create a nice gradient.
			- "Random" : If you don't want to choose, let chance choose for you !
			- (colors) : Select 2 colors.
			- (banners) : Change your banner.
			- "Vertical/Horizontal" : Change the direction of the banner you will create.
			- "Create" : Create a banner with the selected colors and direction.
		- "Skins" : Personnalize your avatar ! Choose one image among the skins.
			- "Random" : If you don't want to choose, let chance choose for you !
			- (skins) : Change your avatar.
  		- "Faces" : Personnalize your expression !
			- (faces) : Change your face.
	- Game : During the game.
		- [LEFT CLICK] "Drop fruit" : Let the current fruit fall in the bag.
		- [H] "Show/Hide help line" : Show or hide the help line.
  		  Help line : a vertical line under the current fruit position to help see where it should land.
		- [F] "Fruitopedia" : Open the fruitopedia screen to have information about the fruits.
		- [SPACE] "Pause game" : Pause the game and open the pause screen.
		- [P] "Parameters" (mouse on toothed wheel icon) : Open the parameters screen.
		- [RETURN] "Back to menu" : If the game have started (at least one fruit in the bag), open a warning screen.
  		  Else, directly go back to main menu.
			- "Back to menu ?" : Warning screen to warn player going back to the menu will delete current game.
		- [Q] "Quit game" : Close the game.
		- "Scoreboard" (mouse on score) : Show the scoreboard with the best score among players.
		- "Watermelon" (mouse on watermelon): Show the number of watermelon made during the game.
		- "Profile" (mouse on avatar) : Show the profile of the player.
		- "Skins" (mouse on clothes icon) : Show the skins screen.
		- "Shopping" (mouse on shop icon) : Show the shopping screen with the powers (cost score).
- [A] "Profile" : Open the profile screen.
	- [LEFT CLICK] "Set avatar" : To change player's skin. Open profile edition screen, skins tab.
	- [LEFT CLICK] "Set banner" : To change player's banner. Open profile edition screen, banners tab.
	- "Unlog" : Deconnect player's account. Will go back to main menu.
- [H] "Help" : Open/close help note screen.
- [M] "Mute" : Mute/unmute music.
- [ARROW UP] : Increase music volume.
- [ARROW DOWN] : Reduce music volume.
- [P] "Parameters" : Open/close parameters screen.
	- [TAB] "Next parameter" : Select next parameter for modification.
	- [MAJ + TAB] "Previous parameter" : Select previous parameter for modification.
	- [RETURN] "Modify checkbox" : Check/uncheck a checkbox parameter.
	- [ARROW LEFT/RIGHT] "Modify gradient" : Modify the value of a gradient parameter.
	- [N] "Next music" : Stop current music and play a random one.
	- "Fullscreen" : Change the size of the screen to fullscreen or half the size.
	- "Luminosity" : Change the luminosity of the screen.
	- "Gamma" : Change the gamma of the screen.
	- "Save score" : Automatically save score after each game.
	- "Restart game" : Automatically start a new game after player lose the current one.
	- "Collect cookies" : Doesn't do anything (maybe ?). Can't be uncheck.
	- "Show scoreboard" : When check, show the scoreboard on the game screen when the mouse is over it.
	- "Show next fruit" : When check, show the next fruit on the game screen.
	- "Show help line" : When check, allow to display the help line on the game screen.
	- "Difficulty" : Can modify the difficulty of the game.
		- "Easy" : Fruits are smaller. When sort the bag, will give score.
		- "Medium" : Regular difficulty, all default parameters.
		- "Hard" : Fruits are bigger.
		- "Impossible" : Fruits are huge. Only the 4th first smallest fruit are available instead of 5.
	- "Draw bg behind skin" : Display a circle behind each fruit to see its hitbox.
	  Unlock at level 2 (with first skin).
	- "Repeat music" : Play the current music endlessly.
	- "Music" : Modify the music volume.
	- "Sounds" : Modify the sounds volume.
- [Q] "Quit" : Close the game.

-Images-
![Create your profile](images/screenshots/create_profile.png)
![Fruitopedia](images/screenshots/fruitopedia.png)
![Icon](images/screenshots/icon.png)
![Main menu](images/screenshots/main_menu.png)
![Music screen](images/screenshots/music.png)
![Parameters screen](images/screenshots/parameters.png)
![Pause screen](images/screenshots/pause.png)
![Powers screen](images/screenshots/powers.png)
![Player's profile](images/screenshots/profile.png)
![Scoreboard](images/screenshots/scoreboard.png)
![Skins screen](images/screenshots/skins.png)

***
## Roadmap

- v0.0.1 :
	- Create window
	- Add caption
	- Add icon
- v0.0.2 :
	- Create fruits
	- Display random fruit on screen
- v0.0.3 :
	- Prevent fruit from going out window
	- Add gravity
- v0.0.4 :
	- Add collision between fruit
	- Add repulsion force
- v0.0.5 :
	- Make same fruit merge and create next fruit
- v0.0.6 :
	- Add a box (borders) and add collisions with it
	- Add background
- v0.0.7 :
	- Add score
	- Add next fruit screen
	- Add current fruit to know which one is current and which one is next
- v0.0.8 :
	- Allow player to choose where to put the fruit (can slide with mouse)
	- Make next fruit coherent (fix bug)
- v0.0.9 :
	- Upgrade fruit physics and collisions
	- Add timers for dropping next fruit and merging fruit (too fast otherwise)
- v0.1.0 :
	- Add main menu
	- Add buttons to slide between menus and more (start game, restart, go to menu, options, exit)
- v0.1.1 : [small update]
	- Make buttons work
	- Launch project on GitHub
- v0.1.3 :
	- Add scoreboard screen
	- Add save scores function for scoreboard
	- Add Fruitopedia screen
- v0.1.4 : [design update]
	- Add borders and reflect on fruit and buttons
- v0.1.5 :
	- Add condition for losing game
	- Add lose screen
- v0.1.6 :
	- Add more dynamic functions (display_default_box function, fruit's size)
- v0.1.7 :
	- Add musics
	- Add music lector
	- Add volume setting
	- Add mute feature
- v0.1.8 :
	- Add parameters screen
	- Add balanced difficulties
- v0.1.9 :
	- Add skin for fruit (not used yet)
	- Add a background for all screens
- v0.2.0 :
	- Add documentations
	- Clean code
	- Add comments
- v0.2.1 :
	- Make all parameters work
	- Allow to change between skins
	- Add gradient bar fluid
- v0.2.2 :
	- Allow to click on buttons
	- Minors changes
- v0.2.3 :
	- Add powers (make them cost score) :
		- pop a fruit
		- sort basket
		- make fruit smaller and lighter
		- make fruit bigger and heavier
		- choose current fruit
- v0.2.4 :
	- Upgrade physics (using pymunk)
	- Make score more balanced
	- Merging fruits will now increase score (instead of dropping fruits)
- v0.2.5 :
	- Update lost screen when high score is beaten
	- Add sounds
- v0.2.6 :
	- Add rolling fruit on menu (use a timer)
	- Add skin screen
	- Add skins background (transparent circle to make hitbox clearer)
	- Add skins overlay (display data when mouse on it) : only work on skins screen
- v0.2.7 :
	- Add level with xp (based on score)
	- Add accounts
	- Add icon for account
	- Add saves for player's data
- v0.2.8 :
	- Add bonus
 	- Add banners
	- Add palettes
	- Add notifications on screen
	- Add loading screen
- v0.2.9 : [In production]
	- Modify automatically color palette and music based on day in calendar (valentine, halloween, christmas, ...)
- v0.3.0 : [Later]
	- Add credits
	- Allow to execute the game (use executionner)
	- Add update screen for new version
- v0.3.1 : [Later]
	- Add 'last_player.txt' file to auto-log last player
	- Add level screen to set difficulty related parameters in the game
- v0.3.2 : [Later]
	- Add bots with different level
	- Allow to play against bot
- v0.3.3 : [Later]
	- Add success which give profile experience
	- Animations when player gain experience or for buttons background)

***
## User license : GNU GPL v3

- Copyleft strict
- You can use it, modify it and share it but you have to keep the same license
- Must stay open source

***
**Contact : mir.nathan666@gmail.com**

Feel free to share your exprerience and your suggestions !
