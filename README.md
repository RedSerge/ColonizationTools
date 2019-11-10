# Red Serge’s Colonization DOS Toolbox.
**(Tools for “Colonization for DOS”, v. 3.0, 7 feb 1995 – available at Steam).**

### Introduction

*(These tools are provided “AS IS”, use at your own risk, don’t forget to backup, be sure that you understand the information provided below and know how to use DOSBox).*

This little project happened overnight when I had no Internet connection to play my favorite games - just USB Flash with random stuff, and DOSBox (along with Colonization and Turbo Pascal) was among it, somehow.

It’s always fun to play Sid Meier’s strategy games, but it’s usually even more fun to update them with some ideas or scenarios of my own, extending the playtime. So, I made my personal toolbox for this purpose. Hastily written code is not an example of the most clean and effective programming, yet it achieved its purpose of bringing me some fun – and be useful for its purpose, that’s why I decided to share this spontaneous stuff.

Anyway… Let me list it and describe how to use it (first of all, extract all the binary files from BIN.ZIP to the folder with your Colonization game).

### 1)	Randomize leaders and improve native villages:

**`LEADER.EXE`**

Randomizes the leaders of each country (their corresponding characteristics).
Reads NAMES.OLD, expands it with randomly generated (different) lines describing rival characters, stores the result into NAMES.TXT. 

NAMES.OLD provided along with this toolbox improves the power of the natives; to use original settings, just copy NAMES.TXT over NAMES.OLD before launching LEADER.EXE.

As a result, each new game can have different set of leaders. Just launch LEADER.EXE before starting the new game.

### 2)	Grant the independence:

**`GRANT.EXE [n]`**

*n = 0..9, number of save file [COLONY0n.sav], default value = 0*

Reads COLONY0n.sav and check the conditions to grant independence. If those conditions are achieved, Parliament disbands the Expeditionary Forces, allowing to win without bloodshed.

The Civilization game is popular for its ability to win by different matters, militant and civilized. The Colonization, however, enforces the great big battle at the end upon the player. Meanwhile, the computer-controlled European rivals are always got their independence granted by their Motherland for development. Why not to bring those rules into consideration for the player, too?

Of course, the rules are stricter than for the NPCs, you know :) . 80 colonists (citizens living in the colonies, no army or roaming units) must strictly (no percent rounding, no Simon Bolivar effect, no nonsense) support the idea of the Independence. The rebels per colony are counted this way: Size of colony * real rebel percent (w/o effects provided by Simon Bolivar).

### 3)	“Repaint” and “Reality” fix tools.

**`REALITY.EXE [n]`**

**`REPAINT.EXE [nefsd]`**

*n = 0..9, number of save file [COLONY0n.sav], default value = 0.*

*e, f, s, d  = 0..3, new master of current English, French, Spanish and Dutch colonies, correspondingly. Default values: 1,2,3 and 0.*

REPAINT.EXE reads the selected save file and provides its colonies another master along with parameters. For example, “REPAINT.EXE 21201” changes COLONY02.SAV (2) in such a way, that English and Dutch colonies are now belonging to French (1), French – to Spanish (2), Spanish – to English (0). No units are updated, though – that’s where REALITY.EXE comes to the rescue.

REALITY.EXE reads the selected save file and checks whether the units in each colony match its allegiance. I made this tool as a separate one, as I had a bug once when the Tory colony produces colonist which somehow is Rebel. I fortified the unit and … never was able to get that colony back! I attacked it and went right through it. This fix helped me to correct the bug and still win :) .

### 4)	*“This is taxation without representation! Unfair!”*

**`TAXPATCH.EXE [t]`**

*t = -128..127, maximum tax rate, default value = 0.*

Changes VICEROY.EXE procedure that controls the tax rate when the King visits viceroy. Original value is 75 (%). If current tax value is higher than this bound, it becomes equal to it. The relative offset of the procedure is stored at file TAXATION.POS.

### 5)	The Time Warp.

**`TIMEWARP.EXE [xyz]`**

*x, y, z = 0..9, number of save file [COLONY0n.sav], default value = 0, 1 and 2, correspondingly.*

Copies [COLONY0x.sav] to [COLONY0z.sav], checking along the way the colonies stored in [COLONY0y.sav]. For each colony that locates at the same position on the map as the corresponding colony in [COLONY0x.sav] and belongs to the same European Power, the colony internal information (except its name) is stored in [COLONY0z.sav]. All “tory uprising” flags are dropped, allowing Tory to start colonial rebellion once again (just because I love to give second chances :) ).

Well, this is ultimate cheating tool to abuse the game :) . I actually made it for two reasons: to eliminate atrocities against the natives made by another European powers – to be able to come back in time without losing the progress that was made along the way yet keep the natives and their ecosystem alive. I hate eliminating natives, as you already could have guessed :) …
…Another usage example: as some kind of a sci-fi Time Warp :) , where I can “teleport” my colonies between games, on another “planet”. Just for fun :) .

### 6)	Colonies can’t be built during the War of Independence – but what about “after the War”?

**`SWITCH.EXE [n]`**

*n = 0..9, number of save file [COLONY0n.sav], default value = 0.*

Toggles the rebel/tory mode of the selected save file if the War of Independence is already won. Usage: switch to the “tory” mode, create the colony or talk to the European power or whatever, switch back again w/o consequences (For example, “Test Routine” item from the “Cheat” menu changes some internal flags and states, while this tool doesn’t have any side effects).

### 7)	Introducing new terms of the game.

**`TERMS.EXE [n]`**

*n = 0..9, number of save file [COLONY0n.sav], default value = 0.*

This tool modifies the selected save file in one of different ways:

1)	Before the War of Succession event: «suspends» the War of Succession, preventing the elimination of the weakest European power as well as ability to declare the Independence properly.
2)	After the War of Succession “suspension”, if the current in-game date is not before 1600 AD, and at least one European power has no colonies: restores the original state of the War of Succession.
3)	After the War of Succession finish, if it’s possible to declare the independence: provides the alternative scenario to declare the independence. There’s no hall of fame [don’t expect your score to be recorded alongside ones achieved under traditional rules]; no Intervention from other European power, all treaties between you and your rivals are kept untouched, moreover, you can’t talk to them or seize their colonies yet they can attack you.
4)	After the War of Independence victory: provides the way to recover back to the state 2, with “suspended” War of Succession.

Why should my rivals be eliminated when my colonial empire is ready to declare an independence? Why should I be the only one that got eliminated after 1600 AD w/o colonies? Why should my rivals got “frozen” once I declare the independence? Well, this cornerstone tool solves those questions once and for all, as it provides new terms and new set of rules to change the game flow. The usual scenario of usage for my toolset is as in the example below:

1)	Run LEADER.EXE to randomize the rivals. Run “TAXPATCH.EXE 75” to restore the taxation mechanics.
2)	Start the game, save it at slot #0, before the very first step (1492 AD), run TERMS.EXE to suspend the War of Succession.
3)	Play till 1600 AD, forcing one of the European nations to be withdrawn from the New World, got the rebel rate above (or equal to) 50%. Store some old version of your game at slot #1, keep saving your actual one at slot #0.
4)	Run TERMS.EXE to eliminate “the weakest link” (the one w/o colonies).
5)	[Additional step] Run GRANT.EXE, if in peaceful mode and don’t want to actually fight with these pesky Tories :) . Just be sure to reach the conditions. 
6)	In any case, sign peace with all the European powers and run TERMS.EXE to declare an independence.
7)	Win the War. 
8)	[Additional step] Run TERMS.EXE twice to recover your “colonial” status and continue playing. Run TAXPATCH.EXE to block the taxation (you’re independent, after all! :) ). Play till the War of Succession on the next step. Use SWITCH.EXE to select the appropriate mode (keep that fancy rebel USA flag :) – or do some business, like signing peace treaty with rivals or building new colony, for example).
9)	[Unnecessary step] Manipulate the allegiance of the colonies via REPAINT.EXE and REALITY.EXE, if needed. Run “TIMEWRAP.EXE 102”, load the save game from slot #2 and watch your colonists travel through time :) .
10)	[Necessary step] Have fun! :)
