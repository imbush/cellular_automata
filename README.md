# cellular_autonomata
Skeleton code and examples for continuous range cellular autonomata. <b>Work In Progress</b>

## Progress
So far, I have created a simple pygame display and binary one dimensional cellular automata function. The function binary_one_dimension takes a row and a decimal rule as input. And outputs the next iteration of the row. Running [definitions.py](/definitions.py) allows the user to input their rule of choice in the terminal and presents the iterations of the row as descending rows with pygame. The initial row used is a row filled with "off" states with one "on" states tile in the center. The width and height of the array can be changed in definitions. The display settings can be found in [pygame_settings.py](/pygame_settings.py).

Here is an example of elementary cellular automata: Wolfram rule 30.</br>
![wolfram rule 30 binary one dimensional automata](/readme_images/wolfram_rule30.png)

Here is an example of totallistic cellular automata with 5 colors. Code 727846227.</br>
![5-color code 727846227 totallistic one dimensional automata](/readme_images/k5_code727846227.png)

## To do:
- [X] Skeleton pygame display code
- [X] Function display in run mode
- [X] Sample binary automota rules
- [X] Multiple state cellular automata
- [ ] Javascript version

## Research Sources:
https://mathworld.wolfram.com/CellularAutomaton.html

