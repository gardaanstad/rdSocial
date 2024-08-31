from typing import *


class Post:
    from user import User
    def __init__(self, id: int, user: "User", content: str):
        self.__id = id
        self.__user_handle = user.handle()
        self.__content = content
    
    def __str__(self):
        return f"@{self.__user_handle}: {self.__content}"
    
    def __repr__(self):
        return f"Post(id={self.__id}, user={self.__user_handle}, content=\"{self.__content}\")"
    
    def __hash__(self):
        return hash(self.__content)
    
    def id(self) -> int:
        return self.__id
    
    def content(self) -> str:
        return self.__content
    
    def user_handle(self) -> str:
        return self.__user_handle