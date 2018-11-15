# README
## 1.How to start
To start it is necessary install  **gym**, an open-source library that contains a lot of different environments.
To do this we have to open the terminal and digit  

```bash
git clone https://github.com/openai/gym.git
cd gym
pip install -e 
```
However with this method is possible to use only some environment categories:

1. algoritmich
2. toy-text
3. classic-control

To use the other environments we have to install other dependency.
We can find the instructions to install them at this link: https://github.com/openai/gym

## 2.Gym
The core of gym is the interface **Env** and to use it we need to know 3 methods:

1. **Reset(self)**: reset the state of the environment and return the observation;
2. **Step(self, action)**: the environment goes to the next step. Return observation, reward, done and info;
3. **Render(self, mode='human', close=False)**: it makes the rendering of an environment frame;

# CartPole-V0
To start we have to select the environment:  

```python
env = gym.make('CartPole-v0')
```
To interface with different environments we need to understand what are the **observation** returned in each step of the algorithm.

## 1.Observation
In this environment the observation is a tuple of 4 elements: 
 
1. **Position of cart**;
2. **Angle of the pole**;
3. **Angular speed of the pole**;
4. **Cart speed**;
 
All these caracteristics are measured in different ways and returned with different unit of measure.
It is very important normalize between 0 and 99 the data obtained to index the matrix of rewards.

```python
cart_pos = int(interp(cart_pos,[min_env[0], max_env[0]], [0,DIM_P - 1])) 
```
After dat normalization  it is possible to find the optimal state, that is the state where the position of the cart, the angle of the pole, the angular speed of the pole and the cart speed are equal to 50.
self.q[cart_pos][cart_speed][angle][angle_speed][action] = pv + learning_rate * (av + alpha * max(self.q[cart_pos, cart_speed, angle, angle_speed, :]) - pv)  # aggiornamento matrice q dei reward      

## 2.Reward
The method **step** return a reward that could be 0 or 1 depending if the the state is more or less near to teh optimal state.

## 3.Exploration
The method **exploration** return the next action taking in input the present state.
The choice of the next action can be made in a randomic way or taking the most useful action.

## 4.Alg_q
In the method **Alg_q** vwe can find the invocation of the method **step** that return **observation**. After data are normalized and the reward in the matrix q is update.

# MsPacman-v0
To start we have to select the environment:  

```python
env = gym.make('MsPacman-v0')
```

## 1.Observation
In this environment the observation is a RGB image, that is an array of dimensions (210,160,3).
Than every state of the environment is an image.  

## 2.Reward
Assign a reward to a specific state is very difficult because it require a specific interpretation of the image.
It is more useful to use standard rewards of the environment returned by the function **step**.

## 3.Exploration
The method **exploration** is the same in every environments, it takes in input a state and returns the next action.

## 4.Alg_q
In the method **Alg_q** there are the invocations of two other methods: **exploration** and **step**.
For the managment of observations a dictionary is generated, where the keys are the observations and the values are the rewards for each action.  
Each element of the dictionary has as a key an array and as associated values a set of rewards.

```python
state = int(sha1(observation.view(uint8)).hexdigest(), 16) 
```

  
