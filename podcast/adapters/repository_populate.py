from podcast.adapters.repository import AbstractRepository, RepositoryException
from podcast.domainmodel.model import Podcast, Episode, User, Review, Playlist, Author, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import os

def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    podcast_file_name = os.path.join(dir_name, "data/podcasts.csv")
    episode_file_name = os.path.join(dir_name, "data/episodes.csv")
    reader = CSVDataReader(podcast_file_name, episode_file_name)

    podcasts = reader.podcast_list
    episodes = reader.episode_list
    authors = list(reader.author_set)
    categories = list(reader.category_set)
    # add authors and categories to repo as well using the sets in the csv
    repo.add_multiple_podcasts(podcasts)
    repo.add_multiple_episodes(episodes)
    repo.add_multiple_authors(authors)
    repo.add_multiple_categories(categories)
