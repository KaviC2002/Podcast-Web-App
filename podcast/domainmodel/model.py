from __future__ import annotations
from datetime import datetime

def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")

def validate_review_rating(rating, minimum, maximum):
    if (minimum <= rating <= maximum) is False:
        raise ValueError(f"The minimum rating is {minimum} and the maximum rating is {maximum}")



class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image:str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self.reviews = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            # when an episode is added to a podcast now it belongs to that podcast so set episode's podcast to this object
            episode.podcast = self
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected an Review instance.")
        if review not in self.reviews:
            self.reviews.append(review)

    def remove_review(self, review: Review):
        if review in self.reviews:
            self.reviews.remove(review)



    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        # category id is not in the podcast. csv so we manually create category id
        # but there can be podcasts with the same categories but different id
        # so if the equality method uses category id, the set can have multiple same
        # categories. To avoid this, changed the id to name in the equality method
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._id < other._id

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []
        self._playlist = None
        self._reviews = []
        # self._playlist = Playlist(playlist_id=1, owner=self, name=f"{username}'s Playlist")

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


    @property
    def subscription_list(self):
        return self._subscription_list

    @property
    def playlist(self):
        return self._playlist

    @property
    def reviews(self):
        return self._reviews

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected an Review instance.")
        if review not in self._reviews:
            self._reviews.append(review)

    def remove_review(self, review: Review):
        if review in self._reviews:
            self._reviews.remove(review)

    def set_playlist(self, playlist: Playlist):
        if not isinstance(playlist, Playlist):
            raise TypeError("Expected a Playlist instance.")
        self._playlist = playlist

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))

class Episode:
    # TODO: Complete the implementation of the Episode class.
    def __init__(self, episode_id: int, podcast: Podcast, title: str= "Untitled", audio: str="", length: int = None
                 , description: str = "", pub_date: str = "Unspecified"):
        validate_non_negative_int(episode_id)
        validate_non_empty_string(title, "Episode title")
        # an episode must have a podcast that it belongs to the relationship between episode and podcast is like
        # the relationship between page and book, one can't exist with the other(composition)
        if not isinstance(podcast, Podcast):
            raise TypeError("podcast must be a Podcast object.")
        self.__id = episode_id
        self.__podcast = podcast
        self.__title = title.strip()
        self.__audio = audio
        self.__length = length
        self.__description = description
        self.__pub_date = pub_date

    @ property
    def id(self) -> int:
        return self.__id

    @ property
    def podcast(self) -> Podcast:
        return self.__podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self.__podcast = new_podcast

    @ property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Episode title")
        self.__title = new_title.strip()
    @ property
    def audio(self) -> str:
        return self.__audio

    @ property
    def length(self) -> int:
        return self.__length

    @ property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Episode description")
        self.__description = new_description

    @ property
    def pub_date(self) -> str:
        return self.__pub_date

    def __repr__(self):
        return f"<Episode {self.id}: '{self.title}'>"

    def __eq__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class Review:
    # TODO: Complete the implementation of the Review class.
    def __init__(self, review_id: int, podcast: Podcast, user: User, rating: int, content: str):
        validate_non_negative_int(review_id)
        validate_non_negative_int(rating)
        # usually, rating can't be 0 and the most commonly used rating systems are 5 point scale and 10 point scale
        # 5 point scale is used
        validate_review_rating(rating, 1, 5)
        validate_non_empty_string(content, "Review content")
        if not isinstance(user, User):
            raise TypeError("User must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = review_id
        self._user = user
        self._podcast = podcast
        self._rating = rating
        self._content = content
        self._timestamp = datetime.now()

# all the fields of the review class have no setter since changing a review that's already written doesn't make sense
    @property
    def id(self) -> int:
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @property
    def user(self) -> User:
        return self._user

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def content(self) -> str:
        return self._content

    def __repr__(self):
        return f"<Review of podcast {self.podcast.title}: by user {self.user.username}>"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self.rating < other.rating

    def __hash__(self):
        return hash(self.id)


class Playlist:
    def __init__(self, playlist_id: int, owner: User, name: str):
        # Validate inputs
        validate_non_negative_int(playlist_id)
        validate_non_empty_string(name, "Playlist name")

        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")

        # Initialize attributes
        self._id = playlist_id
        self._owner = owner
        self._name = name.strip()
        self._episodes = []  # List of episodes
        self._podcasts = []  # List of podcasts

    # Playlist ID property
    @property
    def id(self) -> int:
        return self._id

    # Owner of the playlist
    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    # Name of the playlist
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    # Episodes in the playlist
    @property
    def episodes(self):
        return self._episodes

    # Podcasts in the playlist
    @property
    def podcasts(self):
        return self._podcasts

    # Add episode to the playlist
    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self._episodes:  # Ensure no duplicates
            self._episodes.append(episode)

    # Remove episode from the playlist
    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    # Add podcast to the playlist (add once)
    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self._podcasts:
            self._podcasts.append(podcast)

    # Remove podcast from the playlist
    def remove_podcast(self, podcast: Podcast):
        if podcast in self._podcasts:
            self._podcasts.remove(podcast)

    # Representation of the playlist object
    def __repr__(self):
        return f"<Playlist {self.id}: Owned by {self.owner.username}>"

    # Equality check based on playlist ID and owner(User)
    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id == other.id and self.owner == self.owner

    # Less-than comparison for sorting (based on name)
    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.name < other.name

    # Hash method for using playlist in sets/dictionaries
    def __hash__(self):
        return hash(self.id)
