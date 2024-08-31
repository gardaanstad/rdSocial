from typing import *
from nltk.tokenize import word_tokenize
from collections import Counter
from post import Post

class InvertedIndex:
    def __init__(self):
        self.__index: dict[str, list[Post]] = {}
    
    def __repr__(self) -> str:
        return f"InvertedIndex({self.__index})"
    
    def __str__(self) -> str:
        return str([f"{term}: {posts}" for term, posts in self.__index.items()])
    
    def __tokenize(self, content: str) -> list[str]:
        return word_tokenize(content.casefold())
    
    def __normalize(self, word: str) -> str:
        return word.casefold()
    
    def index_post(self, post: Post):
        content = self.__tokenize(post.content())
        
        for word in content:
            if word not in self.__index:
                self.__index[word] = [post]
                continue
            self.__index[word].append(post)
    
    def __keyword_search(self, keyword: str) -> list[Post]:
        """
        Returns a list of posts that contain the given keyword.
        """
        
        keyword = self.__normalize(keyword)
        return self.__index.get(keyword, [])

    def search(self, query: str, top_k: int = None) -> list[Post]:
        """
        Returns a list of posts that match the given query.
        """
        
        assert isinstance(query, str), "Query must be a string"

        keywords = self.__tokenize(query)
        keyword_sets = [set(self.__keyword_search(keyword)) for keyword in keywords]
        all_posts = list(set.union(*keyword_sets)) # all posts that contain one or more of the keywords

        scored_posts: Counter[Post, int] = Counter()
        for post in all_posts:
            post_keywords = self.__tokenize(post.content())
            
            for post_keyword in post_keywords:
                if post_keyword in keywords:
                    scored_posts[post] += 1

        scored_posts = scored_posts.most_common(top_k)
        results = [post for (post, _) in scored_posts]

        return results