from typing import *
from nltk.tokenize import word_tokenize
from collections import Counter
from user import User
from post import Post
from invertedindex import InvertedIndex

class System:
    def __init__(self):
        self.__users: dict[str, User] = {} # {handle: User instance, ...}
        self.__posts: dict[int, Post] = {} # {id: post, ...}
        self.__index: InvertedIndex = InvertedIndex() # {word: [post, ...], ...}
    
    def get_post(self, post_id: int) -> Post:
        return self.__posts.get(post_id, None)
    
    def __normalize(self, buffer: str) -> str:
        return buffer.casefold()
    
    def __tokenize(self, buffer: str) -> list[str]:
        return word_tokenize(self.__normalize(buffer))
    
    def __process_post(self, post: Post) -> None:
        """
        Processes a post by adding it to the system and inverse indexing it.
        """
        
        assert isinstance(post, Post), "Post must be a Post"
        assert post.id() not in self.__posts, "Post ID already exists"
        
        self.__posts[post.id()] = post
        self.__index.index_post(post)
        self.add_user(post.user_handle())
    
    def add_post(self, content: str, user: User) -> int:
        """
        Adds a post to the system. Returns the post's ID.
        """
        
        new_post = Post(len(self.__posts), user, content) # id, user, content
        self.__process_post(new_post)
        user.add_post(new_post.id())
        
        return new_post.id()
    
    def delete_post(self, post_id: int) -> None:
        """
        Deletes a post from the system.
        """
        
        post = self.__posts.get(post_id, None)
        assert post is not None, "Post not found"
        
        user = self.__users.get(post.user_handle(), None)
        assert user is not None, "User not found"
        
        del self.__posts[post_id]
        user.remove_post(post_id)
    
    def search(self, query: str, top_k: int = None) -> list[Post]:
        """
        Returns a list of posts that match the given query.
        """
        
        return self.__index.search(query, top_k)
    
    def __user_keyword_search(self, keyword: str) -> list[User]:
        """
        Internal helper method to search for users by keyword.
        
        Returns a list of User instances which contain the keyword in their name.
        """
        
        keyword = self.__normalize(keyword)
        return [user for user in self.__users.values() if self.__normalize(user.name()) == keyword]
    
    def search_users(self, query: str, top_k: int = None) -> list[User]:
        """
        Returns a list of users' names that match the given query.
        """
        
        assert isinstance(query, str), "Query must be a string"
        
        keywords = self.__tokenize(query)
        keyword_sets = [set(self.__user_keyword_search(keyword)) for keyword in keywords]
        all_users = list(set.union(*keyword_sets)) # all users that contain one or more of the keywords

        scored_users: Counter[User, int] = Counter()
        for user in all_users:
            user_keywords = self.__tokenize(user.name())
            
            for user_keyword in user_keywords:
                if user_keyword in keywords:
                    scored_users[user] += 1

        scored_users = scored_users.most_common(top_k)
        results = [user for (user, _) in scored_users]

        return results
    
    def add_user(self, handle: str, name: str = None) -> User:
        """
        Adds a user to the system and returns it. If the user already exists, it returns the existing user.
        """
        handle = self.__normalize(handle)
        
        if handle in self.__users:
            return self.__users[handle]
        
        if name is None:
            raise ValueError("User must have a name")
        
        new_user = User(handle, name)
        self.__users[handle] = new_user
        return new_user
    
    def __user_by_name(self, name: str, default = None) -> Optional[User]:
        """
        Returns a User instance if it finds a user with the given name in the system.
        Returns None if no user is found.
        """
        user: User
        for user in self.__users.values():
            if self.__normalize(user.name()) == name:
                return user
        return default
    
    def __user_by_handle(self, handle: str, default = None) -> Optional[User]:
        """
        Returns a User instance if it finds a user with the given handle in the system.
        Returns None if no user is found.
        """
        return self.__users.get(handle, default)
    
    def user(self, query: str) -> Optional[User]:
        """
        Attempts to return a User instance with the given handle.
        If no user is found, attempts to return a User instance with the given name.
        Returns None if no user is found.
        """
        
        query = self.__normalize(query)
        
        if query not in self.__users: # if handle not in system, search by name
            return self.__user_by_name(query)
        
        return self.__user_by_handle(query) # if handle in system, return user
        
    def posts_by_user(self, user: User) -> list[Post]:
        """
        Returns a list of posts from the given user.
        """
        
        assert isinstance(user, User), "User must be a User"

        return [self.__posts[id] for id in user.posts()] # list of Post instances
    
    def posts_by_following(self, user: User) -> list[Post]:
        """
        Returns a list of posts from users that the given user follows.
        """
        
        assert isinstance(user, User), "User must be a User"
        
        if len(user.following()) == 0:
            return []
        
        posts = []
        for following_handle in user.following():
            following = self.__user_by_handle(following_handle)
            assert isinstance(following, User), f"Couldn't find user that @{user.handle()} is following with handle: @{following_handle}"
            
            posts.extend(self.posts_by_user(following))
        
        return posts
    
    def follow(self, follower_handle: str, followee_handle: str) -> None:
        """
        First user follows second user by adding the second user's handle to the first user's following and 
        the first user's handle to the second user's followers.
        """
        
        follower = self.__user_by_handle(follower_handle)
        followee = self.__user_by_handle(followee_handle)

        assert follower is not None, "User that's following not found"
        assert followee is not None, "User to be followed not found"
        
        follower: User
        followee: User
        
        follower.add_following(followee.handle())
        followee.add_follower(follower.handle())
    
    def unfollow(self, follower_handle: str, followee_handle: str) -> None:
        """
        First user unfollows second user by removing the second user's handle from the first user's following and 
        the first user's handle from the second user's followers.
        """
        
        follower = self.__user_by_handle(follower_handle)
        followee = self.__user_by_handle(followee_handle)
        
        assert follower is not None, "User that's following not found"
        assert followee is not None, "User to be unfollowed not found"
        
        follower: User
        followee: User
        
        follower.remove_following(followee.handle())
        followee.remove_follower(follower.handle())
    
    def delete_user(self, user_handle: str) -> None:
        """
        Deletes a user and all their posts from the system.
        """
        
        user = self.user_by_handle(user_handle)
        assert user is not None, "User not found"
        
        for post_id in user.posts():
            del self.__posts[post_id]
        
        del self.__users[user.handle()]
    
    def delete_post(self, post_id: int) -> None:
        """
        Deletes a post from the system.
        """
        
        post = self.__posts.get(post_id, None)
        assert post is not None, "Post not found"
        
        user = self.__users.get(post.user_handle(), None)
        assert user is not None, "Post's user not found"
        
        user.remove_post(post_id)
        del self.__posts[post_id]
    
    @staticmethod
    def process_users(system: "System", users: list[(str, str)]) -> "System":
        """
        Processes a list of users by adding them to the system.
        Returns the system.
        """
        for handle, name in users:
            system.add_user(handle, name)
        
        return system
    
    @staticmethod
    def process_posts(system: "System", posts: list[tuple[str, User]]) -> "System":
        """
        Processes a list of posts by adding them to the system.
        Returns the system.
        """
        for post in posts:
            system.add_post(post[0], post[1])
        
        return system
    
    @staticmethod
    def process_follows(system: "System", follows: list[tuple[User, User]]) -> "System":
        """
        Processes a list of follows by adding them to the system. 
        
        The parameter 'follows' is a list of tuples [(User that's following, User that's being followed), ...].
        
        Returns the system.
        """
        for follow in follows:
            system.follow(follow[0].handle(), follow[1].handle())
        
        return system