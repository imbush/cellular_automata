# cellular_autonomata
Skeleton code and examples for continuous range cellular autonomata. <b>Work In Progress</b>

## Progress
So far, I have created a simple pygame display and binary one dimensional cellular automata function. The function binary_one_dimension takes a row and a decimal rule as input. And outputs the next iteration of the row. Running [definitions.py](/definitions.py) allows the user to input their rule of choice in the terminal and presents the iterations of the row as descending rows with pygame. The initial row used is a row filled with "off" states with one "on" states tile in the center. The width and height of the array can be changed in definitions. The display settings can be found in [pygame_settings.py](/pygame_settings.py).

Here is an example of cellular automata: Wolfram rule 30.</br>
![wolfram rule 30 binary one dimensional automata](/readme_images/wolfram_rule30.jpeg)

## To do:
- [X] Skeleton pygame display code
- [ ] Interactable tiling in draw mode
- [X] Function display in run mode
- [X] Sample binary automota rules
- [ ] Multiple state cellular automata

## Research Sources:
https://mathworld.wolfram.com/CellularAutomaton.html

