import random
n=random.randint(1,100)   #randomly choose a number 
a=-1
guesses=0 
while(a!=n):
    guesses+=1
    a=int(input("Guess the number: "))
    if(a>n):
        print("Guess a Lower number please")
    else:
        print("Guesses a higher number pleases")

print(f"You have guessed the number correctly in{guesses} attenpts and the number is {n}")        