from system import System
from user import User
from post import Post
from typing import *

class Post:
    def __init__(self, user: "User", content: str):
        self.__user = user
        self.__content = content
    
    def __str__(self):
        return f"{self.__user.name}: {self.__content}"
    
    def __repr__(self):
        return f"Post(user={self.__user.name()}, content=\"{self.__content}\")"
    
    def __hash__(self):
        return hash(self.__content)
    
    def content(self):
        return self.__content
    
    def normalized_content(self):
        return self.__content.casefold()
    
    def user(self):
        return self.__user