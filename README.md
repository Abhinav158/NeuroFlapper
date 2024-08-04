
# Neuroflyer 🐦

Neuroflyer is an educational project aimed at demonstrating the NEAT (NeuroEvolution of Augmenting Topologies) algorithm using the `neat-python` library. The project showcases how to train an AI agent to navigate the classic "Flappy Bird" game, avoiding obstacles (pipes) during its flight. 

Neuroflyer leverages the NEAT algorithm to evolve neural networks capable of controlling the bird's movements in the Flappy Bird game.

## Demo

https://github.com/user-attachments/assets/ea0b936b-7c2e-4d16-80ea-97e8779844e3


## Features

 - NEAT Algorithm: Implementing the NEAT algorithm using `neat-python`
   to evolve neural networks. 
  - Pygame Integration: Simulation of the Flappy Bird game environment using `pygame`. 
   - Dynamic Learning: The AI Bird learns to play the game better over successive generations.
  - Visualization: Real-time visualization of the bird's movements and
   the evolving gameplay.

## Game Elements 

The game simulation environment is setup in `pygame` 

The project consists of three main classes representing the key components of the game, each with its own properties and behaviors:

<ul>
    <li>Bird - Represents the agent </li>
    <li>Pipe - Represents the obstacles the bird must avoid</li>
    <li>Ground or Base - Represents the lower limit or base obstacle</li>
</ul>

## Running the Project 

1. Clone the repository 

```bash
git clone https://github.com/abhinav158/neuroflyer.git

cd neuroflyer
```

2. Ensure you add the game assets from the `images` directory and the font file 

3. Run the game 

```bash
python main.py
```

## References 

https://www.pygame.org/docs/ref/font.html
https://neat-python.readthedocs.io/en/latest/
