# Data for Non-strategic Econometrics (for Initial Play)

Datasets used in the paper [Non-strategic Econometrics (for Initial Play)](https://arxiv.org/abs/2208.06521) at AAMAS 2023. 

You can cite the paper with the following Bibtex entry:
```
@inproceedings{chui2023non,
  title={Non-strategic Econometrics (for Initial Play)},
  author={Chui, Daniel and Hartline, Jason and Wright, James R},
  booktitle={Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems},
  pages={634--642},
  year={2023}
}
```

Datasets consist of subjects playing 24 3x3 NFGs on Amazon Mechanical Turk, with subjects taking less than 120 seconds (2 minutes) to play all 24 games being excluded.

Subjects played across 2 conditions: 
## Filtered vs. Nonfiltered
	filtered games have no level-k strategy similar to a level (k-1) strategy, when any linear4 decision rule is used as a level-0 strategy. Nonfiltered games have no such condition.

## Ordered vs. Randomized
	Participants played all games in the same order in the ordered condition, whereas the games were presented in a random order to participants in the randomized condition
## Game indices
The `gameIndices.pkl` file gives the order the games were presented to each subject, with each row index corresponding to the subject in the file storing the player actions. For the ordered conditions, the gameIndices just contain an array containing the numbers 0-23 in order.
