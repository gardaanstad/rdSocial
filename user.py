from post import Post
from system import System
from typing import *

class User:
    def __init__(self, name: str, handle: str, admin: bool = False):
        self.__name: str = name
        self.__handle: str = handle # unique identifier
        
        self.__admin: bool = admin
        
        self.__followers: list[int] = [] # list of follower indices in system.__users
        self.__following: list[int] = [] # list of following indices in system.__users
        
        self.__posts: list[int] = [] # list of post indices in system.__posts
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"User(name={self.__name}, handle={self.__handle})"
    
    def name(self):
        return self.__name
    
    def normalized_name(self):
        return self.__name.casefold()
    
    def handle(self):
        return self.__handle
    
    def followers(self) -> list[int]:
        return self.__followers
    
    def following(self) -> list[int]:
        return self.__following
    
    def follower_amount(self) -> int:
        return len(self.__followers)
    
    def add_follower(self, follower: int):
        """
        Adds a follower to the user's followers in the form of an index into the system's self.__users list.
        """
        assert isinstance(follower, int), "Follower index must be an integer"
        assert follower >= 0, "Follower index must be non-negative"
        
        self.__followers.append(follower)
    
    def add_following(self, following: int):
        """
        Adds a following to the user's following in the form of an index into the system's self.__users list.
        """
        assert isinstance(following, int), "Following index must be an integer"
        assert following >= 0, "Following index must be non-negative"
        
        self.__following.append(following)
    
    def posts(self) -> list[int]:
        """
        Returns the user's posts in the form of indices into the system's self.__posts list.
        """
        return self.__posts
    
    def add_post(self, post_index: int) -> None:
        """
        Adds a post to the user's posts in the form of an index into the system's self.__posts list.
        """
        assert isinstance(post_index, int), "Post index must be an integer"
        assert post_index >= 0, "Post index must be non-negative"
        
        self.__posts.append(post_index)
    
    def post_to_system(self, system: "System", content: str) -> int:
        return system.add_post(Post(self, content))
    
    def follow_by_handle(self, system: "System", handle: str) -> None:
        system.follow_by_handle(self.handle(), handle)