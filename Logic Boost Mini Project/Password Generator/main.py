import random
import string

# Now create Func to characterise the password
def generate_password(length=9,use_letters=True,use_numbers=True,use_symbols=True):
    character=""

    if use_letters:
        character += string.ascii_letters

    if use_numbers:
        character += string.digits

    if use_symbols:
        character += string.punctuation

    if not character:
        return "Error:at least on character to be included"
    
    password = ''.join(random.choice(character) for i in range(length))
    return password

def main():
    print("This is Password Generator...")

    # Get Password length
    while True:
        try:
            length=int(input("Enter the Length of your Password (9+):"))
            if length<7:
                print("Password should be greater than 7:")
                continue
            break

        except ValueError:
            print("Invalid input,Retryyy..")

    # Get character preferences
    def get_yes_no(prompt):
        while(True):
            response=input(prompt).strip().lower()
            if response in['y','yes']:
                return True
            
            elif response in ['n','no']:
                return False
            
            else:
                print("Invalid input..Please Enter(y/n)")


    use_letters=get_yes_no("Include Letter(A-Z)and(a-z)?(y/n)")
    use_numbers=get_yes_no("Include Numbers(0-9)?(y/n)")
    use_symbols=get_yes_no("Include Symbols(?@#$!)?(y/n)")

    print("\n ....Generating Password....")

    password = generate_password(length,use_letters,use_numbers,use_symbols)

    if password.startswith("Error"):
        print(password)
    
    else:
        print(f"\n Password is:{password}")
        print("\nProcess Closing..")
    
if __name__=="__main__":
    main()



