"""
board: 5x5, A0 to E5
ships: 2 unit cruiser, 2 unit destroyer, 1 unit submarine
status of locations: hit(1)/miss(-1)/water(w)/ship(s)
status of ship: sunk(1)/afloat(0)
"""
from libdw.sm import SM
import random
from time import sleep

directions=[(0,1), (0,-1), (1,0), (-1,0)]

class Ship:    
    def __init__(self, name, length):
        self.name=name
        self.length=length
        self.loc={}
        self.sunk=False
    
    def checkstatus(self):
        if 0 not in self.loc.values():
            self.sunk=True
        
    def attacked(self, hitloc):
        self.loc[hitloc]=1
        
            
class Board:
    def __init__(self):
        self.coord={}
        for row in ('A', 'B', 'C', 'D', 'E'):
            for col in (1, 2, 3, 4, 5):
                self.coord[(row, col)]='w'   
        
    def update(self, loc):
        if self.coord[loc]=='s':
            self.coord[loc]=1
            return "hit"
        else:
            self.coord[loc]=-1
            return "miss"
        
    def display(self, view=None):
        print(" ", end='')

        for i in range(1,6):
            print("{:2d}".format(i), end='')
        print('')
        
        for row in ('A', 'B', 'C', 'D', 'E'):
            print("{}".format(row), end='')
            for col in range(1,6):
                if self.coord[(row, col)]=='w': sym='*'
                elif self.coord[(row, col)]=='s':
                    if view==None: sym='s'
                    else: sym='*'
                elif self.coord[(row, col)]==1: sym='x'
                elif self.coord[(row, col)]== -1: sym='w'
                
                print(" {}".format(sym), end='')
            print()
        
    
class Player:
    def __init__(self):
        self.board=Board()
        self.shiplog=[Ship('cruiser', 2), Ship('destroyer', 2), Ship('sub', 1)]
        self.lost=False
    
    def clearsurr(loc, loclist):
        for d in directions:
            surrloc=(chr(ord(loc[0])+d[0]), loc[1]+d[1])
            if surrloc in loclist:
                loclist.remove(surrloc)
        return loclist

    def gameover(self):
        if self.shiplog==[]:
            self.lost=True
            
    def placeships(self):
        pass
    
    def playturn(self, opp):
        pass

            
class Human(Player):
    def getcoord(text):
        try:
            x,y = text.split()
        except ValueError:
            text = list(text)
            x,y = text[0], text[1]        
        return x,y
    
    def placeships(self):
        emptyloc=list(self.board.coord.keys())
        
        for ship in self.shiplog:
            potloc=[]
            print("\nPlace your {}-unit {}.".format(ship.length, ship.name))
            while True:
                text = input("Enter coordinates of a location for the hull: ")
                x,y=Human.getcoord(text)
                try:
                    headloc=(x, int(y))
                except ValueError:
                    print("Coordinates must be alpahabet-integer combination. Example: A1.")
                    continue
                
                if headloc in emptyloc:
                    ship.loc[headloc]=0
                    self.board.coord[headloc]='s'
                    emptyloc.remove(headloc)
                    break
                else:
                    print("This is not an allowed location.")
            
            if ship.length!=1:
                for d in directions:
                    checkloc=(chr(ord(headloc[0])+d[0]), headloc[1]+d[1])
                    if checkloc in emptyloc:
                        potloc.append(checkloc)
                
                while True:
                    text = input("Enter coordinates of a location for the stern: ")
                    x,y = Human.getcoord(text)
                    try:
                        nextloc=(x, int(y))
                    except ValueError:
                        print("Coordinates must be alpahabet-integer combination. Example: A1.")
                        continue
                    if nextloc in potloc:
                        ship.loc[nextloc]=0
                        self.board.coord[nextloc]='s'
                        break
                    else:
                        print("This is not an allowed location.")
                
                emptyloc.remove(nextloc)
                emptyloc=Human.clearsurr(nextloc, emptyloc)
        
            emptyloc=Human.clearsurr(headloc, emptyloc)
            
    
    def playturn(self, opp):
        while True:
            text = input("\nEnter coordinates of a location to attack: ")
            x,y = Human.getcoord(text)
            try:
                tryloc=(x, int(y))
            except ValueError:
                print("Coordinates must be alpahabet-integer combination. Example: A1.")
                continue
            
            if tryloc not in opp.board.coord:
                print("No location corresponds to these coordinates.")
            
            elif type(opp.board.coord[tryloc])==int:
                print("This location has already been attacked.")
                
            else:
                result=opp.board.update(tryloc)
                print("Your attack was a {}!".format(result))
                if result=="hit":
                    for ship in opp.shiplog:
                        if tryloc in ship.loc:
                            ship.attacked(tryloc)
                            ship.checkstatus()
                            if ship.sunk==True:
                                print("Opponent's {} has been sunk.".format(ship.name))
                                opp.shiplog.remove(ship)
                            break
                break
                
class AI(Player, SM):
    start_state="hunt"
    
    def __init__(self, opp): 
        Player.__init__(self)
        self.availableloc=list(coord for coord in opp.board.coord.keys() if (ord(coord[0])+coord[1])%2==0)
        self.possibleloc=[]
        
    def placeships(self):
        emptyloc=list(self.board.coord.keys())
        potloc=[]
        
        for ship in self.shiplog:
            while len(ship.loc)!=ship.length:
                headloc=random.choice(emptyloc)
    
                if ship.length==1:
                    ship.loc[headloc]=0
                    self.board.coord[headloc]='s'
                    emptyloc.remove(headloc)
                    emptyloc=AI.clearsurr(headloc, emptyloc)

                else:
                    for d in directions:
                        checkloc=(chr(ord(headloc[0])+d[0]), headloc[1]+d[1])
                        if checkloc in emptyloc:
                            potloc.append(checkloc)
                   
                   
                    if len(potloc)!=0: 
                        nextloc=random.choice(potloc)
                        for fixloc in (headloc, nextloc):
                            ship.loc[fixloc]=0
                            self.board.coord[fixloc]='s'
                            emptyloc.remove(fixloc)
                        emptyloc=[loc for loc in emptyloc if loc not in potloc]
                        potloc=[]
         
        
    def playturn(self, opp):
        #if all even locations have been checked then availableloc will be empty, then check all odd locations
        opp.gameover()
        if opp.lost==False and self.availableloc==[]:
            self.availableloc=list(coord for coord in opp.board.coord.keys() if (ord(coord[0])+coord[1])%2!=0)
            
        if self.state=="hunt":
            tryloc=random.choice(self.availableloc)
        else:
            tryloc=random.choice(self.possibleloc)
       
        result=opp.board.update(tryloc)
        print("Opponent's attack was a {}!".format(result))            
        
        for ship in opp.shiplog:
            if tryloc in ship.loc:
                ship.attacked(tryloc)
        
        if tryloc in self.availableloc:
                self.availableloc.remove(tryloc)
                
        if result=="hit":
            #check if any ship has been sunk
            #if yes then delete all locations in possibleloc from availableloc, empty possibleloc and change state
            #if not then add surrounding locations to possibleloc and change state only at first hit
            for d in directions:
                checkloc=(chr(ord(tryloc[0])+d[0]), tryloc[1]+d[1])
                if checkloc in opp.board.coord and opp.board.coord[checkloc] in ('w', 's'):
                        self.possibleloc.append(checkloc)
               
            for ship in opp.shiplog:
                ship.checkstatus()
                if tryloc in ship.loc and ship.sunk==True:
                    self.availableloc=[loc for loc in self.availableloc if loc not in self.possibleloc]
                    self.possibleloc=[]
                    result="sunk"
                    print("Your {} has been sunk.".format(ship.name))
                    opp.shiplog.remove(ship)
                    break
            
        elif self.state=="target": 
            self.possibleloc.remove(tryloc)
       
        self.step(result)      
        
    def get_next_values(self, state, inp):
        if state=="hunt" and inp=="miss":
            next_state=state
            
        elif state=="hunt" and inp=="hit":
            next_state="target"
    
        elif state=="target" and inp!="sunk":
            next_state=state
            
        elif inp=="sunk":
            next_state="hunt"
          
        output=inp
        return next_state, output
        
def main():
    realPlayer=Human()
    aiPlayer=AI(realPlayer)

    print("PLACEMENT RULES:\n1.Ships must be placed either horizontally or vertically.\n2.Ships cannot be overlapped.\n3.Ships cannot share any edges; touching corners are accepted.")
    print("\nPosition your ships according to the rules.")
    realPlayer.board.display()
    realPlayer.placeships()
    sleep(1)
    print("\nThis is your final board configuration.")
    realPlayer.board.display()
    sleep(3)
    print("\nYour opponent will now position their ships.")
    aiPlayer.placeships()  
    aiPlayer.start()
    sleep(3)
    print("\nYou and your opponent will take turns to attack. You are the first player.")
    sleep(3)
    
    moves=0
    while True:
        print("\nYOUR TURN\n")
        aiPlayer.board.display("hidden")
        realPlayer.playturn(aiPlayer)
        aiPlayer.gameover()
        if aiPlayer.lost:
            sleep(5)
            print("\nYou've won in {} moves".format(moves))
            break
        sleep(3)
        print("\nOPPONENT's TURN")
        aiPlayer.playturn(realPlayer)
        realPlayer.gameover()
        if realPlayer.lost:
            sleep(5)
            print("\nOpponent has won in {} moves".format(moves))
            break

        moves+=1
        sleep(3)

if __name__ == '__main__':
    main()

