from nltk.tokenize import word_tokenize
from typing import *
from system import System
from post import Post
from user import User
import os

def search(system: System, current_user: User):
    print("Search menu")
    print("  1. Search for post")
    print("  2. Search for user")
    print("  3. Back")
    option = input("> ")
    os.system("clear")
    
    match option:
        case "1": # Search for post
            print("Search for post")
            query = input("> ")
            results = system.search(query)
            
            print()
            post: Post
            for post in results:
                print(f"https://rdSocial.com/post/{post.id()}/\n@{post.user_handle()}: {post.content()}")
                print()
        
        case "2": # Search for user
            print("Search for user")
            query = input("> ")
            results: list[User] = system.search_users(query, top_k=5)
            for i, user in enumerate(results):
                print(f"{i}: {user}")
            
            print(f"{len(results) + 1}: Back")
            print()
            print("Follow or unfollow the user above by entering their number.")
            option = int(input("> "))

            if option == len(results) + 1:
                return
            
            if option > len(results) or option < 1:
                print("Invalid option")
                return
            
            user = results[option]
            
            if user.handle() in current_user.following():
                current_user.unfollow(system, user.handle())
                print(f"No longer following {user.name()}!")
            else:
                current_user.follow(system, user.handle())
                print(f"Now following {user.name()}!")
            
        case "3": # Back
            return
        case _:
            print("Invalid option")

def app_loop(system: System, current_user: User) -> bool:
    while True:
        print("Please pick an option:")
        print("  1. Home")
        print("  2. Search")
        print("  3. Post")
        print("  4. Profile")
        print("  5. Edit profile")
        print("  6. Logout")
        option = input("> ")
        os.system("clear")
        
        match option:
            case "1": # Home
                print("-------- Home --------")
                for post in system.posts_by_following(current_user):
                    print(post)
                print("----------------------")
                print()
            case "2": # Search
                search(system, current_user)
            case "3": # Post
                content = input("Post: ")
                current_user.post(system, content)
            case "4": # Profile
                print(system.posts_by_user(current_user))
            case "5": # Edit profile
                print("Edit profile")
            case "6": # Log out
                return False

def login_menu(system: System) -> User:
    while True:
        print("Would you like to login or create an account?")
        print("  1. Login")
        print("  2. Create account")
        option = input("> ")
        os.system("clear")
        
        match option:
            case "1": # Login
                handle = input("Please enter your handle:\n> ")
                
                user = system.user(handle)
                if user is None:
                    print(f"User {handle} not found")
                    continue
                
                os.system("clear")
                print(f"Welcome back, {user.name()}!")
                print()
                return user
            
            case "2": # Create account
                print("Create an account")
                name = input("Pick a name:\n> ")
                handle = input("Pick a handle:\n> ")
                user = system.add_user(handle, name)
                
                os.system("clear")
                print(f"Welcome to rdSocial, {user.name()}!")
                print()
                return user
            
            case _:
                print("Invalid option")

if __name__ == "__main__":
    print("Initializing system...")
    
    system: System = System()
    
    users = [
        ("garda", "Gard Aanstad"),
        ("elwynbm", "Elwyn Bjerkan"),
        ("charlie", "Charlie"),
        ("dan", "Dan the man"),
        ("eve", "Eve"),
    ]
    
    system = System.process_users(system, users)
    
    posts = [
        ("Hello, world! I'm Gard and I live in Oslo. I <3 Oslo!", system.user("garda")),
        ("Hey, everyone! I'm Elwyn and I'm from Larvik. I live in Oslo.", system.user("elwynbm")),
        ("I'm Charlie! I live in Oslo.", system.user("charlie")),
        ("Hi, I'm Dan the man! I'm born and raised in Larvik.", system.user("dan")),
        ("Test", system.user("eve")),
    ]
    
    system = System.process_posts(system, posts)
    
    follows = [
        (system.user("garda"), system.user("elwynbm")),
        (system.user("garda"), system.user("charlie")),
        (system.user("garda"), system.user("dan")),
        (system.user("garda"), system.user("eve")),
        (system.user("elwynbm"), system.user("garda")),
        (system.user("elwynbm"), system.user("dan")),
        (system.user("charlie"), system.user("garda")),
        (system.user("charlie"), system.user("dan")),
        (system.user("dan"), system.user("garda")),
        (system.user("dan"), system.user("elwynbm")),
        (system.user("dan"), system.user("charlie")),
        (system.user("dan"), system.user("eve")),
    ]
    
    system = System.process_follows(system, follows)
    
    os.system("clear")
    print("Welcome to rdSocial!\n")
    
    while True:
        current_user = login_menu(system)
        
        logged_in = app_loop(system, current_user)
        
        if not logged_in:
            print("Logged out.\n")