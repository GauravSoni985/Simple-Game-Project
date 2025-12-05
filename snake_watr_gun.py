import random
'''
snake water gun game ( stone paper sciesor) 
stone=1
paper=0
scissor=-1'''
computer=random.choice([-1,0,1])   #randomly choose a number
youstr=input("Enter your choice: ")
youdict={"s": 1, "p": 0, "si": -1}
you=youdict[youstr]
if(computer==you):
    print("Match Draw")
else:   
     if(computer==-1 and you==1):
         print("You win")
     elif(computer==-1 and you==0):
       print("computer win and You lose")
     if(computer==1 and you==-1):
      print("computer win and you lose") 
     elif(computer==1 and you==0):
       print("you win! ")       
     if(computer==0 and you==-1):
      print("you win! ")
     elif(computer ==0 and you ==1):
      print("computer win and you lose" )