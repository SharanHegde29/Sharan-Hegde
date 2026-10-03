todo_list = []

def display_menu():
    print("\n--- To-Do List Menu ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Task")
    print("4. Exit")
    print("-----------------------")

def add_task():
    task = input("Enter the task you want to add: ").strip()
    if task:
        todo_list.append(task)
        print(f" Task '{task}' added.")
    else:
        print(" Task cannot be empty.")

def view_tasks():
    if not todo_list:
        print("\n Your to-do list is empty! Time to add some tasks.")
        return

    print("\n--- Your Tasks ---")
    for i, task in enumerate(todo_list):
        print(f"{i + 1}. {task}")
    print("------------------")

def delete_task():
    if not todo_list:
        print("\nNothing to delete. The list is already empty.")
        return

    view_tasks() 
    
    try:
        task_num = int(input("Enter the number of the task to delete: "))
        
        index_to_delete = task_num - 1 
        
        if 0 <= index_to_delete < len(todo_list):
            deleted_task = todo_list.pop(index_to_delete)
            print(f" Task '{deleted_task}' deleted successfully.")
        else:
            print(" Invalid task number. Please try again.")
            
    except ValueError:
        print(" Invalid input. Please enter a valid number.")


def main():
    print(" Welcome to the Minimal To-Do List CLI!")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            print("\n Goodbye! Your current list will not be saved.")
            break 
        else:
            print("Invalid choice. Please select a number between 1 and 4.")

if __name__ == "__main__":
    main()
