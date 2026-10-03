'''
rock>scissor
paper>rock
scissor>paper
'''

import random

def game():
    output=["rock" , "paper", "scissor"]
    print("This is a Rock,Paper,Scissor Game..")
    print("Enter end to finish the game:")

    while True:
        user_choice=input("Enter Rock,Paper or Scissors.").lower()

        if user_choice=="end":
            print("Thanks for Playing:")
            break

        if user_choice not in output:
            print("Invalid Terms:")
            continue

        computer_choice=random.choice(output)
        print(f"Computers Choice:{computer_choice}")

        if user_choice==computer_choice:
            print(f"Its a Tiee,Both choose:{user_choice}")

        elif user_choice=="rock":
            if computer_choice=="scissor":
                print("Rock Smashed Scissor,You Win")
            else:
                print("Paper Wrapped the Rock,You Lose")

        elif user_choice=="paper":
            if computer_choice=="rock":
                print("Paper Wrapped the Rock,You Win")
            else:
                print("Scissor Sliced the Paper,You Lose")

        elif user_choice=="scissor":
            if computer_choice=="paper":
                print("Scissor Sliced the Paper,You Win")
            else:
                print("Rock Smashed Scissor,You Lose")
        
        print("-"*30)

if __name__=="__main__":
    game()



            