from nltk.tokenize import word_tokenize
from typing import *
from system import System
from post import Post
from user import User

def admin_tools(system: System):
    print("Admin tools")
    print("  1. Add user\n  2. Remove user\n  3. Remove post\n  4. Search\n  5. Exit")
    option = input("> ")
    
    match option:
        case "1":
            name = input("Name: ")
            handle = input("Handle: ")
            user = system.add_user(User(name, handle))
            print(f"Added user {user.name()}!")
            
        case "2":
            handle = input("Handle: ")
            user = system.user_by_handle(handle)
            if user is None:
                print("User not found")
                return
            system.delete_user(user)
            print(f"Deleted user {user.name()}!")
            
        case "3":
            index = int(input("Index: "))
            system.delete_post(index)
            print(f"Deleted post {index}!")
            
        case "4":
            query = input("Query: ")
            results, indices = system.search(query, include_index=True)
            for result in results:
                print(result)
            for index in indices:
                print(f"  {index}: {system.__posts[index]}")
                
        case "5":
            return
        
        case _:
            print("Invalid option")

def logged_in_loop(system: System, current_user: User):
    while True:
        print("Please pick an option:")
        print("  1. Post\n  2. Follow\n  3. Search\n  4. Search for user\n  5. Edit profile\n  6. Administrative tools\n  7. Log out")
        option = input("> ")
        
        match option:
            case "1":
                current_user.post_to_system(system, input("Post: "))
            case "2":
                current_user.follow_by_handle(system, input("User's handle to follow: "))
            case "3":
                query = input("Search: ")
                results = system.search(query)
                print("\n", results)
            case "4":
                print(system.user_by_name(input("User: ")))
            case "5":
                print("Edit profile")
            case "6":
                admin_tools(system)
            case "7":
                return False

def login_menu(system: System) -> User:
    while True:
        print("Would you like to login or create an account?")
        print("  1. Login")
        print("  2. Create account")
        print("> ", end="")
        option = input()
        
        match option:
            case "1":
                handle = input("Handle: ")
                user = system.user_by_handle(handle)
                
                if user is None:
                    print("User not found")
                    continue
                
                print(f"Welcome back, {user.name()}!")
                return user
            
            case "2":
                name = input("Name: ")
                handle = input("Handle: ")
                user = system.add_user(User(name, handle))
                print(f"Welcome to Twitter, {user.name()}!")
                return user
            
            case _:
                print("Invalid option")


if __name__ == "__main__":
    twitter = System()
    
    print("Welcome to Twitter!")
    
    while True:
        current_user = login_menu(twitter)
        
        logged_in = logged_in_loop(twitter, current_user)
        
        if not logged_in:
            print("Logged out")