# coding=utf-8
from gym import Env
import random
from Tkinter import *
import numpy as np
import time


class WumpusEnv(Env):
    """
    The wumpus world was introduced by Genesereth, and is discussed in Russell-Norvig.
    The wumpus world is a cave consisting of rooms connected by passageways. Lurking somewhere in the cave is the
    terrible wumpus, a beast that eats anyone who enters its room. The wumpus can be shot by an agent, but the agent has
    only one arrow. Some rooms contain bottomless pits that will trap anyone who wanders into these rooms (except for
    the wumpus, which is too big to fall in). The only mitigating feature of this bleak environment is the
    of finding a heap of gold. The game ends either when the agent dies (falling into a pit or being eaten by the
    wumpus) or when the agent climbs out of the cave.

    Performance mesure:
    -   +1000 for climbing out of the cave with the gol
    -   -1000 for falling into a pit or being eaten by the wumpus
    -   -1 for each action taken
    -   -10 for using up the arrow

    Actions:
        - 'Forward' (F): moves the agent forward of one cell (walls are blocking)
        - 'TurnLeft' by 90 (L)
        - 'TurnRight' by 90 (R)
        - 'GrabGold' (G): pick up the gold if it is in the same cell as the agent
        - 'ShootArrow' (S): fires an arrow in a straight line in the direction of the agent is facing. The arrow
          continues until it either hits (and hece kills) the wumpus or hits a wall. The agent has only 1 arrow.
        - 'ClimbOut' (C): climbs out of the cave

    Perceptions:
        - In the square containing the wumpus (W) and in the directly (not diagonally) adjacent squares, the agent will
          perceive a 'Stench' (S)
        - In the squares directly (not diagonally) adjacent to a pit (P), the agent will perceive a 'Breeze' (B)
        - In the square where the gold (G) is, the agent wil perceive a 'Glitter'
        - When an agent walks into a wall, it will perceive a 'Bump'
        - When the wumpus is killed, it emits a woeful 'Scream' that can be perceived anywhere in the cave
    Perceptions are givent to the agent in the form of a tuple of booleans for
    ('Stench','Breeze','Glitter','Bump','Scream'). For example if there is a stench and a breeze, but no glitter,
    bump, or scream, the perception tuple will be: (True, True, False, False, False).

    Environment:
    A fixed 4x4 grid of rooms. The agent always starts in the square labeled [0,0], facing to the right.

    S     N     B   P
    W   B/S/G   P   B
    S     N     B   N
    A     B     P   B
    """
    #metadata = {'render.modes': ['human']}

    def __init__(self):
        
        self.env = np.zeros((4,4))
        self.actions = ['F', 'L', 'R', 'G', 'S', 'C']
        self.orientation = 1    # orientation tra 0 e 3 
        self.i_agent = 3       # riga
        self.j_agent = 0        # colonna
        self.shoot = 1
        self.init_state = self.env[self.i_agent][self.j_agent]
        self.state = self.init_state
        self.env =  [[0 for x in range(4)] for x in range(4)] 
        self.env[0][0] = [0,[1,0,0,0,0],1]                           # 0.reward  1.perception 2.orientation
        self.env[0][1] = [0,[0,0,0,0,0],1]
        self.env[0][2] = [0,[0,1,0,0,0],1]
        self.env[0][3] = [0,[0,0,0,0,0],1]
        self.env[1][0] = [-1000,[0,0,0,0,0],1]
        self.env[1][1] = [0,[1,1,1,0,0],1]
        self.env[1][2] = [-50,[0,0,0,0,0],1]
        self.env[1][3] = [0,[0,1,0,0,0],1]
        self.env[2][0] = [0,[1,0,0,0,0],1]
        self.env[2][1] = [0,[0,0,0,0,0],1]
        self.env[2][2] = [0,[0,1,0,0,0],1]
        self.env[2][3] = [0,[0,0,0,0,0],1]
        self.env[3][0] = [0,[0,0,0,0,0],1]
        self.env[3][1] = [0,[0,1,0,0,0],1]
        self.env[3][2] = [-50,[0,0,0,0,0],1]
        self.env[3][3] = [0,[0,1,0,0,0],1]

        self.root = Tk()    
         

    def _step(self, action):   #ritorna una lista con lo stato , l'orientazione e righe e colonne corrispondenti
  
        if action == 'F':
            if self.orientation == 0:
                if self.i_agent == 0:
                    print("Invalid action")
                    return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent
                else:
                    self.i_agent = self.i_agent-1 
                    return self.env[self.i_agent-1][self.j_agent], self.orientation, self.i_agent, self.j_agent

            if self.orientation == 1:
                if self.j_agent == 3:
                    print("Invalid action")
                    return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent
                else:
                    self.j_agent = self.j_agent+1
                    return self.env[self.i_agent][self.j_agent+1], self.orientation, self.i_agent, self.j_agent

            if self.orientation == 2:
                if self.i_agent == 3:
                    print("Invalid action")
                    return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent
                else:
                    self.i_agent = self.i_agent+1
                    return self.env[self.i_agent+1][self.j_agent], self.orientation, self.i_agent, self.j_agent

            if self.orientation == 3:
                if self.j_agent == 0:
                    print("Invalid action")
                    return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent
                else:
                    self.j_agent = self.j_agent-1
                    return self.env[self.i_agent][self.j_agent-1], self.orientation, self.i_agent, self.j_agent

        elif action == 'L':             #turn left cambia la variabile orientation
            if self.orientation == 0:
                self.orientation = 3
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent
            else:
                self.orientation -= 1
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent

        elif action == 'R':             #turn right cambia la variabile orientation
            if self.orientation == 3:
                self.orientation = 0
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent
            else:
                self.orientation += 1
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent

        elif action == 'G':     #raccogliere l'oro nell'apposita casella 

            if self.env[self.i_agent][self.j_agent][0:2] != [0,[1,1,1,0,0]]:
                print("Invalid Action")
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent

            else:                
                self.env[self.i_agent][self.j_agent] = [0,[1,1,0,0,0],0];
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent

        elif action == 'C':

            if self.env[self.i_agent][self.j_agent][0:2] != [0,[1,0,0,0,0]]:
                print('Escape')
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent
            else:
                print('Invalid Action')
                return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent


        elif action == 'S':   #shoot           

            
            temp1 = self.i_agent
            temp2 = self.j_agent

            if self.shoot == 1:
                self.shoot = self.shoot-1                
                            
                if self.orientation == 0:
                    while temp1 != 0:
                        if self.env[temp1][temp2] ==[-1000,[0,0,0,0,0],1]:                           
                            self.env[temp1][temp2] = [0,[0,0,0,0,0],1]
                            for i in range(4):
                                for j in range(4):
                                    self.env[i][j][1][4] = 1
                        temp1 -= 1

                if self.orientation == 2: 
                    while temp1 != 4:
                        if self.env[temp1][temp2] == [-1000,[0,0,0,0,0],1]:
                            self.env[temp1][temp2] = [0,[0,0,0,0,0],1] 
                            for i in range(4):
                                for j in range(4):
                                    self.env[i][j][1][4] = 1                          
                        temp1 += 1
                

                if self.orientation == 1:
                    while temp2 != 4:
                        if self.env[temp1][temp2] ==[-1000,[0,0,0,0,0],1]:
                            self.env[temp1][temp2] = [0,[0,0,0,0,0],1]
                            for i in range(4):
                                for j in range(4):
                                    self.env[i][j][1][4] = 1
                        temp2 += 1

                if self.orientation == 3:
                    while temp2 != 0:
                       if self.env[temp1][temp2] ==[-1000,[0,0,0,0,0],1]:
                            self.env[temp1][temp2] = [0,[0,0,0,0,0],1]
                            for i in range(4):
                                for j in range(4):
                                    self.env[i][j][1][4] = 1
                       temp2 -= 1
            else:
                print('Invalid Action')

            return self.env[self.i_agent][self.j_agent], self.orientation, self.i_agent, self.j_agent

        
    def _reset(self):
        self.orientation = 1
        self.state = self.init_state
        self.j_agent = 3
        self.i_agent = 0
        self.shoot = 1
        self.env[1][0] = [-1000,[0,0,0,0,0],1]
        for i in range(4):
            for j in range(4):
                self.env[i][j][1][4] = 0    
        return 
      

    def renderx(self, n, m, root):
      
        frame = Frame(root)
        root.title("Wumpus")
        frame.grid(row=0,column=0) 
        btn =  [[0 for x in range(4)] for x in range(4)] 
        for x in range(4):
            for y in range(4):
                btn[x][y] = Button(frame, bg = 'grey', height = 10, width = 15)
                btn[x][y].grid(column=x, row=y)
        
        btn[0][1] = Button(frame, bg = 'red', text = 'W', height = 10, width = 15)
        btn[0][1].grid(column=0, row=1)
        btn[1][1] = Button(frame, bg = 'yellow', text = 'Gold', height = 10, width = 15)
        btn[1][1].grid(column=1, row=1)        
        btn[n][m] = Button(frame,  command = self.color_change(n,m,btn), bg = 'grey', height = 10, width = 15)
      
        if self.env[1][0] == [0,[0,0,0,0,1],1]:
            btn[0][1] = Button(frame, bg = 'Grey', height = 10, width = 15)
            btn[0][1].grid(column=0, row=1)


        root.update_idletasks()
        root.update()
        time.sleep(0.5)


    def color_change(self,x,y, btn):
        btn[x][y].config(bg="green")    
