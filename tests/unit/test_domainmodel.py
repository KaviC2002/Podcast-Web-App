import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import os


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""

def test_podcast_add_episode(my_podcast):
    episode = Episode(1, my_podcast, "episode 1")
    my_podcast.add_episode(episode)
    assert episode in my_podcast.episodes
    assert len(my_podcast.episodes) == 1
    assert episode.podcast == my_podcast

    my_podcast.add_episode(episode)
    my_podcast.add_episode(episode)
    assert len(my_podcast.episodes) == 1


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes

# fixture provides a new class object for each test
@pytest.fixture
def my_episode(my_podcast):
    return Episode(1, my_podcast, "first episode   " )

@pytest.fixture
def my_review(my_podcast, my_user):
    return Review(1,  my_podcast, my_user, 5, "it was really good")
@pytest.fixture
def my_playlist(my_user):
    return Playlist(1, my_user, "my playlist")

def test_csvdatareader():
    # make sure the file to be accessed and the file tries to access that file are in the same folder.
    dir_name = os.path.dirname(os.path.abspath(__file__))
    # .. means going up twice(from this file to tests folder) and . means going up once(from this file to unit folder)
    # by using .. we can access the csv files in the tests folder
    # to access a file in another file in the tests folder use ../file in tests/file you want
    podcast_path = os.path.join(dir_name, "../data/mini_podcasts.csv")
    episode_path = os.path.join(dir_name, "../data/mini_episodes.csv")
    csv = CSVDataReader(podcast_path, episode_path)
    # check if all the fields are added as intended
    assert len(csv.podcast_list) == 2
    assert len(csv.episode_list) == 2
    assert len(csv.author_set) == 2
    assert len(csv.category_set) == 6
    assert csv.podcast_list[0].website == "http://www.blogtalkradio.com/dhourshow"
    assert csv.podcast_list[0].image == "http://is3.mzstatic.com/image/thumb/Music118/v4/b9/ed/86/b9ed8603-d94b-28c5-5f95-8b7061bf22fa/source/600x600bb.jpg"
    assert csv.podcast_list[0].title == "D-Hour Radio Network"
    assert csv.episode_list[0].title == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"
    # can't access set elements, convert a set to a list using list()
    assert list(csv.category_set)[0].name == "Society & Culture"
    assert list(csv.author_set)[0].name == "D Hour Radio Network"


def test_episode_intialization(my_episode, my_podcast):
    # the episode class only validates id, podcast and title, the other parameters can be empty string/None
    assert my_episode.id == 1
    assert my_episode.podcast == my_podcast
    assert my_episode.title == "first episode"
    assert my_episode.audio == ""
    assert my_episode.length == None
    assert my_episode.description == ""
    assert my_episode.pub_date == "Unspecified"
    assert repr(my_episode) == "<Episode 1: 'first episode'>"

    # check if the id, podcast, title validations are correct
    with pytest.raises(ValueError):
        episode_without_title = Episode(2, my_podcast, "")

    with pytest.raises(ValueError):
        episdoe_with_invalid_id = Episode(-1, my_podcast, "first episode")

    with pytest.raises(TypeError):
        episode_without_podcast = Episode(3, None, "first episode")

def test_episode_title_setter(my_episode):
    # check if the setter accepts a correct title removing empty space with strip()
    my_episode.title = "  second episode  "
    assert repr(my_episode) == "<Episode 1: 'second episode'>"
    # check if the setter doesn't accept invalid titles
    with pytest.raises(ValueError):
        my_episode.title = ""

    with pytest.raises(ValueError):
        my_episode.title = 123

def test_episode_description_setter(my_episode):
    # check if the setter only accepts string
    my_episode.description = "it's a first episode"
    assert my_episode.description == "it's a first episode"

    with pytest.raises(ValueError):
        my_episode.description = 123

def test_episode_podcast_setter(my_episode):
    # check if the setter only accept podcast objects
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    my_episode.podcast = podcast1
    assert my_episode.podcast == podcast1

    with pytest.raises(TypeError):
        my_episode.podcast = None

def test_episode_eq():
    # check if episodes are equal when their ids are the same
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    episode1 = Episode(1, podcast1, "first episode" )
    episode2 = Episode(2, podcast2, "second episode" )
    episode3 = Episode(3, podcast3, "third episode" )
    assert episode1 == episode1
    assert episode1 != episode2
    assert episode2 != episode3

def test_episode_hash():
    # check if episodes create the same hash when their ids are the same
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    episode1 = Episode(1, podcast1, "first episode" )
    episode2 = Episode(1, podcast2, "second episode" )
    episode3 = Episode(3, podcast3, "third episode" )
    episode_set = {episode1, episode2, episode3}
    assert len(episode_set) == 2  # Since episode1 and episode2 have the same ID

def test_episode_lt(my_podcast):
    # check if one episode with a smaller id is less than the other
    episode1 = Episode(1, my_podcast, "Amazing episode")
    episode2 = Episode(2, my_podcast, "Bad episode")
    episode3 = Episode(3, my_podcast, "Cool episode")
    assert episode1 < episode2
    assert episode2 < episode3
    assert episode3 > episode1


def test_review_intialization(my_review, my_user, my_podcast):
    # check if a review object is created when all the parameters are valid
    assert my_review.id == 1
    assert my_review.rating == 5
    assert my_review.content == "it was really good"
    assert repr(my_review.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"
    assert repr(my_review.user) == "<User 1: shyamli>"

    # check if a review object is not created when there is an invalid parameter
    # a review rating must be 0 ~ 10 and can't be decimal/negative
    with pytest.raises(ValueError):
        review_with_negative_rating = Review(2, my_podcast, my_user, -1, "it was really bad")
    with pytest.raises(ValueError):
        review_with_zero_rating =  Review(3, my_podcast, my_user, 0, "it was bad")
    with pytest.raises(ValueError):
        review_with_too_high_rating = Review(4, my_podcast, my_user, 100, "it was a 100/100")
    with pytest.raises(ValueError):
        review_with_decimal_rating = Review(5, my_podcast, my_user, 3.5, "it was good")
    # a review must have content/podcast/user
    with pytest.raises(ValueError):
        review_without_content = Review(8, my_podcast,  my_user, 5, "")

    with pytest.raises(TypeError):
        review_without_podcast = Review(6, None, my_user, 5, "it was good")
    with pytest.raises(TypeError):
        review_without_user = Review(7, my_podcast, None, 5, "it was good")

def test_review_eq(my_user, my_podcast):
    # check if reviews with the same id are equal
    review1 = Review(1, my_podcast, my_user, 5, "it was really good")
    review2 = Review(1, my_podcast, my_user, 3, "it was good")
    review3 = Review(3, my_podcast, my_user, 5, "it was really good" )
    assert review1 == review2
    assert review2 != review3
    assert review1 != review3

def test_review_hash(my_user, my_podcast):
    # check if reviews with the same id create the same hash
    # sets only contain unique elements
    # sets use hash/eq to determine if the elements are the same and if they are, only leave 1 unique element
    review1 = Review(1, my_podcast, my_user, 5, "it was really good")
    review2 = Review(2, my_podcast, my_user, 5, "it was really good")
    review3 = Review(3, my_podcast, my_user, 5, "it was really good" )
    playlist_set = set()
    playlist_set.add(review1)
    playlist_set.add(review2)
    playlist_set.add(review3)
    assert sorted(playlist_set) == [review1, review2, review3]
    playlist_set.discard(review1)
    playlist_set.discard(review2)
    assert list(playlist_set) == [review3]

def test_review_lt(my_user, my_podcast):
    # reviews should be sorted by rating not id
    # check if a review with a lower rating is less than the other
    review1 = Review(1, my_podcast, my_user, 1, "it was really good")
    review2 = Review(1, my_podcast, my_user, 3, "it was really good")
    review3 = Review(1, my_podcast, my_user, 5, "it was really good" )
    assert review1 < review2
    assert review2 < review3
    assert review3 > review1
    review_list = [review3, review2, review1]
    assert sorted(review_list) == [review1, review2, review3]


def test_playlist_initialization(my_playlist, my_user):
    # check if a playlist object is created when id, name and own are valid
    assert my_playlist.id == 1
    assert my_playlist.name == "my playlist"
    assert repr(my_playlist.owner) == "<User 1: shyamli>"

    assert repr(my_playlist) == "<Playlist 1: Owned by shyamli>"

    # check if empty space in a name is removed using strip()
    playlist_with_space = Playlist(2, my_user, "my playlist2   ")
    assert playlist_with_space.name == "my playlist2"

    # check if there is no owner, a playlist is not created
    with pytest.raises(TypeError):
        playlist_without_owner = Playlist(3, None, "my playlist3")

def test_playlist_name_setter(my_playlist):
    # check if the setter can change a playlist name removing space using strip()
    my_playlist.name = "my playlist   "
    assert my_playlist.name == "my playlist"

    # check if the setter doesn't accept empty strings and int
    with pytest.raises(ValueError):
        my_playlist.name = ""

    with pytest.raises(ValueError):
        my_playlist.name = 123

def test_playlist_owner_setter(my_playlist):
    # check if the setter can change the owner
    new_user = User(2, "asma", "pw67890")
    my_playlist.owner = new_user
    assert my_playlist.owner == new_user
    # check if the setter doesn't accept an owner is not a user object
    with pytest.raises(TypeError):
        my_playlist.owner = "not a user"

def test_playlist_eq(my_user):
    # check if playlists with the same id are equal
    new_user = User(2, "asma", "pw67890")
    playlist1 = Playlist(1, my_user, "playlist1")
    playlist2 = Playlist(1, new_user, "playlist2")
    playlist3 = Playlist(3, my_user, "playlist1")
    assert playlist1 == playlist2
    assert playlist1 != playlist3
    assert playlist2 != playlist3


def test_playlist_hash(my_user):
    # check if playlists with the same id create the same hash
    # sets only contain unique elements
    # sets use hash/eq to determine if the elements are the same and if they are, only leave 1 unique element
    # all these playlist have the same fields except for the id but the playlist eq/hash uses id
    # so they should be different despite sharing the same parameters except for the id
    playlist1 = Playlist(1, my_user, "playlist1")
    playlist2 = Playlist(2, my_user, "playlist1")
    playlist3 = Playlist(3, my_user, "playlist1")
    playlist_set = set()
    playlist_set.add(playlist1)
    playlist_set.add(playlist2)
    playlist_set.add(playlist3)
    assert sorted(playlist_set) == [playlist1, playlist2, playlist3]
    playlist_set.discard(playlist1)
    playlist_set.discard(playlist2)
    assert list(playlist_set) == [playlist3]

def test_playlist_lt(my_user):
    # check if a playlist with a smaller id is less than the other playlist
    playlist1 = Playlist(1, my_user, "playlist1")
    playlist2 = Playlist(2, my_user, "playlist2")
    playlist3 = Playlist(3, my_user, "playlist3")
    assert playlist1 < playlist2
    assert playlist2 < playlist3
    assert playlist3 > playlist1
    playlist_list = [playlist3, playlist2, playlist1]
    assert sorted(playlist_list) == [playlist1, playlist2, playlist3]
