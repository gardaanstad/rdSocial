from typing import *
from nltk.tokenize import word_tokenize
from user import User
from post import Post

class System:
    def __init__(self):
        self.__users: list[User] = []
        self.__user_handles: set[str] = set()
        
        self.__posts: list[Post] = []
        
        self.__index: dict[str, list[Post]] = {}
    
    def __index_post(self, post: Post):
        content = word_tokenize(post.normalized_content(), language="norwegian")
        
        for word in content:
            if word not in self.__index:
                self.__index[word] = [post]
                continue
            self.__index[word].append(post)
    
    def __add_user(self, user: User) -> User:
        """
        Internal method for adding a user to the system. 
        Returns user if user was added or already exists.
        Raises ValueError if user handle already exists in system, but user instance is different.
        """
        
        if user in self.__users:
            return user
        
        if user.handle() in self.__user_handles:
            raise ValueError("User handle already exists in system")
        
        self.__user_handles.add(user.handle())
        self.__users.append(user)
        return user
    
    def __add_post(self, post: Post) -> int:
        """
        Adds a post to the system, inverse indexes it, and returns the index of the post in the system's self.__posts list.
        """
        
        self.__posts.append(post)
        self.__add_user(post.user())
        self.__index_post(post)
        
        return len(self.__posts) - 1
    
    def add_post(self, post: Post) -> int:
        """
        Adds a post to the system, inverse indexes it, and returns the index of the post in the system's self.__posts list.
        """
        
        return self.__add_post(post)
    
    def process_posts(self, posts: Iterable[Post]) -> None:
        """
        Processes a list of posts, adding them to the system and inverse indexing them.
        """
        
        posts = iter(posts)
        post = next(posts, None)
        
        while post:            
            post_index = self.__add_post(post)
            
            post.user().add_post(post_index)
            
            post = next(posts, None)
    
    def process_post(self, post: Post) -> None:
        """
        Processes a post, adding it to the system and inverse indexing it.
        """
        
        post_index = self.__add_post(post)
        post.user().add_post(post_index)
    
    def delete_post(self, post_index: int) -> None:
        """
        Deletes a post from the system.
        """
        
        self.__posts.pop(post_index)
    
    def add_user(self, user: User) -> User:
        """
        Adds a user to the system.
        """
        
        return self.__add_user(user)
    
    def __keyword_search(self, keyword: str) -> list[Post]:
        keyword = self.__normalize(keyword)
        return self.__index.get(keyword, [])
    
    def __normalize(self, buffer: str) -> str:
        return buffer.casefold()
    
    def __tokenize(self, buffer: str) -> list[str]:
        return word_tokenize(self.__normalize(buffer), language="norwegian")
    
    def search(self, query: str, top_k: int = None, include_index: bool = False) -> list[Post]:
        assert isinstance(query, str), "Sentence must be a string"
        
        keywords = self.__tokenize(query)
        keyword_sets = [set(self.__keyword_search(keyword)) for keyword in keywords]
        all_posts = set.union(*keyword_sets)
        
        from collections import Counter

        scored_posts: Counter[Post, int] = Counter()
        for post in all_posts:
            for keyword in keywords:
                if keyword in post.normalized_content():
                    scored_posts[post] += 1
        
        results = [post for post, _ in scored_posts.most_common(top_k)]
        return (results, [self.__posts.index(post) for post in results]) if include_index else results
    
    def __user_by_name(self, name: str, default = None, include_index = False) -> Optional[Union[User, Tuple[User, int]]]:
        name = self.__normalize(name)
        
        i: int
        user: User
        
        for i, user in enumerate(self.__users):
            if self.__normalize(user.name()) == name:
                return (user, i) if include_index else user
        return default
    
    def __user_by_handle(self, handle: str, default = None, include_index = False) -> Optional[Union[User, Tuple[User, int]]]:
        handle = self.__normalize(handle)
        
        i: int
        user: User
        
        for i, user in enumerate(self.__users):
            if self.__normalize(user.handle()) == handle:
                return (user, i) if include_index else user
        return default
    
    def user_by_name(self, name: str) -> Optional[User]:
        return self.__user_by_name(name, default=None, include_index=False)
    
    def user_by_handle(self, handle: str) -> Optional[User]:
        return self.__user_by_handle(handle, default=None, include_index=False)
        
    def posts_by_user(self, query_user: str) -> list[Post]:
        user = self.__user_by_name(query_user)
        if user is None:
            return []

        return [self.__posts[i] for i in user.posts()]
    
    def posts_by_following(self, query_user: str) -> list[Post]:
        user = self.__user_by_name(query_user)
        if user is None:
            return []
        
        posts = []
        for follower in user.followers():
            posts.extend([self.__posts[i] for i in self.__users[follower].posts()])
        
        return posts
    
    def follow_by_handle(self, follower: str, followee: str) -> None:
        """
        First user follows second user by adding the second user's self.__users index to the first user's following and 
        the first user's index to the second user's followers.
        """
        
        follower, follower_index = self.__user_by_handle(follower, include_index=True)
        followee, followee_index = self.__user_by_handle(followee, include_index=True)

        assert follower is not None, "User that's following not found"
        assert followee is not None, "User to be followed not found"
        
        follower: User
        followee: User
        
        follower.add_following(followee_index)
        followee.add_follower(follower_index)
        
    def user_followers(self, user: str) -> list[User]:
        user: User = self.__user_by_name(user)
        if user is None:
            return []
        return [self.__users[i] for i in user.followers()]
    
    def user_following(self, user: str) -> list[User]:
        user: User = self.__user_by_name(user)
        if user is None:
            return []
        return [self.__users[i] for i in user.following()]