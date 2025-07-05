# 🚗 Car Simulation with Genetic Algorithm Evolution

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![Jupyter](https://img.shields.io/badge/jupyter-%23F37626.svg?style=flat&logo=jupyter&logoColor=white)](https://jupyter.org/)

A fascinating exploration of **evolutionary computation** and **genetic algorithms** applied to car design optimization! This project simulates the evolution of car designs through natural selection principles, demonstrating how computational biology techniques can solve complex engineering problems.

## 🧬 Project Overview

This simulation creates a population of virtual cars with varying characteristics (frame length, body shapes, wheel configurations) and evolves them through generations to optimize their racing performance. Just like in nature, the fittest individuals survive and reproduce, passing their beneficial traits to offspring while introducing beneficial mutations.

### 🔬 Biological Inspiration

The genetic algorithm implemented here mirrors fundamental principles of biological evolution:
- **Natural Selection**: Only the fastest cars survive to reproduce
- **Genetic Diversity**: Each car has a unique "genome" encoding its physical characteristics
- **Crossover**: Parent cars mate to produce offspring with combined traits
- **Mutation**: Random variations introduce novel characteristics
- **Population Dynamics**: Generations evolve toward better-adapted individuals

## 🏗️ Car Anatomy & Technical Details

Each virtual car is defined by **15 genetic parameters** organized into 5 key components:

### 1. Frame Length 📏
- **Range**: 2.0 - 6.0 meters
- **Impact**: Affects stability and aerodynamics

### 2. Upper Profile Shape 📈
- **Parameters**: 5 floating-point values
- **Description**: Height at equi-spaced points from rear to front
- **Example**: `[0.8, 1.0, 1.0, 0.5, 0.3]`

### 3. Lower Profile Shape 📉
- **Parameters**: 5 floating-point values  
- **Description**: Ground clearance at equi-spaced points
- **Example**: `[0.3, 0.3, 0.3, 0.3, 0.3]`

### 4. Left Wheel 🛞
- **Position**: 0.0 (rear) to 1.0 (front)
- **Radius**: 0.0 - 2.0 meters
- **Example**: `[0.1, 0.5]` (near rear, medium size)

### 5. Right Wheel 🛞
- **Position**: 0.0 (rear) to 1.0 (front)  
- **Radius**: 0.0 - 2.0 meters
- **Example**: `[0.9, 0.5]` (near front, medium size)

![Car Anatomy](https://sales.bio.unipd.it/assets/carsim/car_model.png)

### 🚧 Manufacturing Constraints

Cars must satisfy realistic engineering constraints:
- **Total Height**: 0.5 - 5.0 meters (upper + lower at each point)
- **Frame Length**: 2.0 - 6.0 meters
- **Wheel Radius**: 0.0 - 2.0 meters
- **Wheel Position**: 0.0 - 1.0 (relative to frame)

## 🧬 Genetic Algorithm Implementation

### Genome Representation
Each car's design is encoded as a 15-element genome:
```python
genome = [frame_length, upper[0:5], lower[0:5], left_wheel[0:2], right_wheel[0:2]]
# Example: [4.0, 0.8, 1.0, 1.0, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.1, 0.5, 0.9, 0.5]
```

### 🏆 Fitness Evaluation
Cars are evaluated on two criteria:
1. **Track Completion**: How far along the track they travel (0.0 - 1.0)
2. **Race Time**: How quickly they complete the track (if they finish)

**Scoring Formula**:
```python
if completion < 1.0:
    fitness = completion  # Didn't finish: only distance matters
else:
    fitness = 1.0 + (100.0 - time)  # Finished: bonus for speed
```

### 🔄 Evolutionary Operations

#### Selection
- **Method**: Tournament selection of top 30% performers
- **Principle**: Survival of the fittest drives evolution

#### Crossover (Mating)
- **Method**: Single-point crossover
- **Process**: Random split point combines parent genomes
```python
child_genome = parent1_genome[:crossover_point] + parent2_genome[crossover_point:]
```

#### Mutation
- **Method**: Gaussian noise addition
- **Strength**: Configurable (default 0.05)
- **Constraint Handling**: Values clipped to valid ranges

#### Population Dynamics
- **Elite Preservation**: Best 30% survive each generation
- **Offspring Production**: 40% created through mating
- **Random Immigration**: 30% new random individuals prevent local optima

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.x**
- **NumPy** for numerical computations
- **Jupyter Notebook** for interactive exploration
- **Car Simulator Binary** (platform-specific)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/ateferos77/Car_Simulation.git
cd Car_Simulation

# Install dependencies
pip install numpy jupyter

# Launch the interactive notebook
jupyter notebook carsimulatoin.ipynb
```

### Platform-Specific Setup

#### Windows
- Use the included `carsim.exe` executable
- Alternatively, extract `carsim_windows.zip`

#### Linux/Mac
- You may need to compile the simulator from source
- Or use Wine to run the Windows executable

## 📖 Usage Instructions

### Basic Car Simulation
```python
import carsim
import numpy as np

# Define a car blueprint
car = [
    4.0,                              # Frame length
    np.array([0.8, 1.0, 1.0, 0.5, 0.3]),  # Upper profile
    np.array([0.3, 0.3, 0.3, 0.3, 0.3]),  # Lower profile  
    np.array([0.1, 0.5]),             # Left wheel [position, radius]
    np.array([0.9, 0.5])              # Right wheel [position, radius]
]

# Simulate the car's race
trajectory = carsim.simulate(*car)
```

### Running Genetic Algorithm
```python
# Create initial population
population = initial_population(100)

# Evolve for multiple generations
for generation in range(30):
    scores = carsim.race(population)
    population = generation_evolution(population, scores)
    
    # Track best performer
    best_car = select_best(population, scores, 0.1)[0]
    print(f"Generation {generation}: Best score = {max(combined_scores(scores))}")
```

### Interactive Exploration
Open `carsimulatoin.ipynb` to:
- 🔬 Explore car anatomy step-by-step
- 🧬 Learn genetic algorithm concepts  
- 🏎️ Watch cars race in real-time
- 📊 Analyze evolutionary progress
- 🎛️ Experiment with parameters

## ✨ Key Features

### 🎮 Interactive Simulation
- **Real-time Racing**: Watch cars navigate tracks in web browser
- **Visual Evolution**: Observe design improvements across generations
- **Parameter Tuning**: Experiment with mutation rates, population sizes

### 🔬 Educational Value
- **Biological Concepts**: Learn natural selection, genetics, evolution
- **Computational Methods**: Understand optimization algorithms
- **Engineering Applications**: See how biology inspires technology

### 🛠️ Extensible Framework
- **Modular Design**: Easy to modify fitness functions
- **Constraint System**: Realistic manufacturing limitations
- **Population Management**: Sophisticated breeding strategies

## 🌱 Applications in Biology & Beyond

### 🧬 Computational Biology
- **Protein Folding**: Optimize 3D protein structures
- **Drug Discovery**: Evolve molecular compounds
- **Phylogenetic Analysis**: Reconstruct evolutionary trees
- **Sequence Alignment**: Find optimal DNA/protein alignments

### 🌍 Real-World Applications
- **Bioinformatics**: Genetic sequence analysis
- **Synthetic Biology**: Design artificial biological systems
- **Ecosystem Modeling**: Simulate population dynamics
- **Medical Research**: Optimize treatment protocols

### 🤖 Engineering & AI
- **Neural Architecture Search**: Evolve AI model structures
- **Robotics**: Optimize robot behaviors and morphologies
- **Engineering Design**: Evolve mechanical systems
- **Scheduling Problems**: Optimize resource allocation

## 📚 Examples & Expected Outputs

### Initial Random Population
```
Generation 0: Average fitness = 0.23, Best fitness = 0.67
```

### After Evolution
```
Generation 10: Average fitness = 0.78, Best fitness = 0.94
Generation 20: Average fitness = 0.89, Best fitness = 1.23
Generation 30: Average fitness = 0.95, Best fitness = 1.41
```

### Typical Evolutionary Trajectory
1. **Early Generations**: Most cars crash, few complete track
2. **Middle Generations**: More cars finish, times improve
3. **Late Generations**: Fine-tuning for optimal speed

## 🤝 Contributing

We welcome contributions from both biology and computer science communities!

### Areas for Contribution
- **New Fitness Functions**: Alternative performance metrics
- **Advanced Operators**: Sophisticated crossover/mutation methods
- **Visualization Tools**: Better progress tracking and analysis
- **Documentation**: Biological explanations and tutorials
- **Platform Support**: Cross-platform simulator binaries

### Contribution Guidelines
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Implement** your changes with tests
4. **Document** biological relevance where applicable
5. **Submit** a pull request with detailed description

### Research Opportunities
- Compare with other evolutionary algorithms
- Investigate different selection pressures
- Analyze genetic diversity maintenance
- Study convergence properties

## 🔮 Future Enhancements

### 🚗 Advanced Car Physics
- [ ] **3D Dynamics**: Full three-dimensional simulation
- [ ] **Aerodynamics**: Wind resistance and downforce
- [ ] **Tire Models**: Realistic friction and wear
- [ ] **Suspension Systems**: Springs and dampers

### 🧬 Enhanced Genetics
- [ ] **Multi-objective Optimization**: Speed vs. fuel efficiency
- [ ] **Diploid Genetics**: Dominant/recessive traits
- [ ] **Sexual Selection**: Mate choice algorithms
- [ ] **Population Structure**: Geographic isolation effects

### 🎯 Specialized Applications
- [ ] **Autonomous Vehicles**: Evolve driving behaviors
- [ ] **Formula 1 Design**: Optimize for specific tracks
- [ ] **Off-road Vehicles**: Terrain-specific adaptations
- [ ] **Electric Vehicles**: Battery and efficiency optimization

### 🔬 Research Extensions
- [ ] **Comparative Evolution**: Multiple species competition
- [ ] **Environmental Changes**: Dynamic track conditions
- [ ] **Coevolution**: Predator-prey dynamics
- [ ] **Cultural Evolution**: Learning and teaching behaviors

## 📄 License

This project is licensed under the **Mozilla Public License 2.0** - see the [LICENSE](LICENSE) file for details.

## 🎓 Educational Resources

### Recommended Reading
- **"Introduction to Genetic Algorithms"** by Melanie Mitchell
- **"Adaptation in Natural and Artificial Systems"** by John Holland
- **"The Selfish Gene"** by Richard Dawkins
- **"Evolutionary Computation"** by Kenneth De Jong

### Online Courses
- MIT OpenCourseWare: Evolutionary Biology
- Coursera: Computational Biology Specialization
- edX: Introduction to Artificial Intelligence

---

*"In the end, we are all just cars trying to navigate the track of life, evolving one generation at a time."* 🏁

**Happy Evolving!** 🧬✨