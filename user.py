from typing import *

class User:
    def __init__(self, handle: str, name: str):
        self.__handle: str = handle # unique identifier
        self.__name: str = name
        
        self.__followers: list[str] = [] # list of follower user handles in system.__users
        self.__following: list[str] = [] # list of following user handles in system.__users
        
        self.__posts: set[int] = set() # list of post ids in system.__posts
    
    def __str__(self):
        return f"{self.__name} (@{self.__handle})"
    
    def __repr__(self):
        return f"User(name={self.__name}, handle={self.__handle})"
    
    def name(self) -> str:
        """
        Returns the user's name.
        """
        return self.__name
    
    def normalized_name(self):
        return self.__name.casefold()
    
    def handle(self):
        return self.__handle
    
    def delete_user(self, system) -> None:
        system.delete_user(self.handle())
    
    # Followers and following ==========================================================================================
    
    def followers(self) -> list[int]:
        """Returns the user's followers in the form of handles."""
        return self.__followers
    
    def following(self) -> list[int]:
        """Returns the user's following in the form of handles."""
        return self.__following
    
    def follower_amount(self) -> int:
        """Returns the number of followers the user has."""
        return len(self.__followers)
    
    def add_follower(self, follower: str):
        """
        Adds a follower to the user's followers in the form of a handle into the system's self.__users dictionary.
        """
        assert isinstance(follower, str), "Follower handle must be a string"
        
        self.__followers.append(follower)
    
    def add_following(self, following: str):
        """
        Adds a following to the user's following in the form of a handle into the system's self.__users dictionary.
        """
        assert isinstance(following, str), "Following handle must be a string"
        
        self.__following.append(following)
    
    def remove_follower(self, follower: str):
        """
        Removes a follower from the user's followers in the form of a handle into the system's self.__users dictionary.
        """
        assert isinstance(follower, str), "Follower handle must be a string"
        
        self.__followers.remove(follower)
    
    def remove_following(self, following: str):
        """
        Removes a following from the user's following in the form of a handle into the system's self.__users dictionary.
        """
        assert isinstance(following, str), "Following handle must be a string"
        
        self.__following.remove(following)
    
    def follow(self, system, user: "User") -> None:
        """
        Follows a user by calling the system's follow method with the current user's handle and the user to be followed's handle.
        """
        assert isinstance(user, User), "User must be a User object"
        system.follow(self.handle(), user.handle())
        
    def unfollow(self, system, user: "User") -> None:
        """
        Unfollows a user by calling the system's unfollow method with the current user's handle and the user to be unfollowed's handle.
        """
        assert isinstance(user, User), "User must be a User object"
        system.unfollow(self.handle(), user.handle())
    
    # Posts ============================================================================================================
    
    def posts(self) -> list[int]:
        """
        Returns the user's posts in the form of ids into the system's self.__posts dictionary.
        """
        return list(self.__posts)
    
    def add_post(self, post_id: int) -> None:
        """
        Adds a post to the user's posts in the form of an id into the system's self.__posts dictionary.
        """
        assert isinstance(post_id, int), "Post id must be an integer"
        assert post_id >= 0, "Post id must be non-negative"
        
        self.__posts.add(post_id)
    
    def post(self, system, content: str) -> int:
        """
        Posts a new post to the system and returns the id of the post.
        """
        return system.add_post(content, self)
    
    def delete_post(self, system, post_id: int) -> None:
        if post_id in self.__posts:
            self.__posts.discard(post_id)
            system.delete_post(post_id)