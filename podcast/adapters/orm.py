from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    # author name is unique anyway since the csv data reader uses a set for authors
    # if unique = True error occurs
    Column('name', String(255), nullable=False, unique=False)
)

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

# Episodes should have links to its podcast through its foreign keys
episode_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_url', Text, nullable=True),
    Column('length', Integer),
    Column('description', String(255), nullable=True),
    Column('pub_date', Text, nullable=True)
)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64)) #, nullable=False)
)

# TASK 1 : Association table podcast_categories
# Resolve many-to-many relationship between podcast and categories
podcast_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id'))
)

playlist_podcasts_table = Table(
    'playlist_podcasts', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('playlist_id', ForeignKey('playlists.playlist_id'))
)

users_table = Table(
    'users', mapper_registry.metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    # Column('playlist_id', ForeignKey('playlists.playlist_id')),
)

# Reviews should have links to its podcast and user through its foreign keys
reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('timestamp', DateTime, nullable=False),
    Column('content', String(255), nullable=False),
    Column('rating', Integer, nullable=False),  # integer rating 1 - 5
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('user_id', ForeignKey('users.user_id')),
)

playlists_table = Table(
    'playlists', mapper_registry.metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    # unique must be true but false for debugging
    Column('name', String(255), unique=False),
)


def map_model_to_tables():

    mapper_registry.map_imperatively(Playlist, playlists_table, properties= {
        '_id': playlists_table.c.playlist_id,
        '_name':playlists_table.c.name,
        #'_owner': playlists_table.c.owner,
        # '_owner': relationship(User),
        # '_Playlist_owner': relationship(User),
        '_owner': relationship(User, back_populates='_playlist'),
        '_podcasts': relationship(Podcast, secondary=playlist_podcasts_table),
    })

    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.name,
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name,
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.title,
        '_image': podcast_table.c.image_url,
        '_description': podcast_table.c.description,
        '_language': podcast_table.c.language,
        '_website': podcast_table.c.website_url,
        '_itunes_id': podcast_table.c.itunes_id,
        '_author': relationship(Author),
        'episodes': relationship(Episode, back_populates='_Episode__podcast'),
        'categories': relationship(Category, secondary=podcast_categories_table),
        'reviews': relationship(Review, back_populates='_podcast'),
    })

    mapper_registry.map_imperatively(Episode, episode_table, properties={
        '_Episode__id': episode_table.c.episode_id,
        '_Episode__podcast': relationship(Podcast, back_populates='episodes'),
        '_Episode__title': episode_table.c.title,
        '_Episode__audio': episode_table.c.audio_url,
        '_Episode__length': episode_table.c.length,
        '_Episode__description': episode_table.c.description,
        '_Episode__pub_date': episode_table.c.pub_date,
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.user_id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
        '_reviews': relationship(Review, back_populates='_user'),
        # '_playlist': relationship(Playlist),
        '_playlist': relationship(Playlist, back_populates='_owner', uselist=False),
    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_id': reviews_table.c.review_id,
        '_timestamp': reviews_table.c.timestamp,
        '_content': reviews_table.c.content,
        '_rating': reviews_table.c.rating,
        '_user': relationship(User, back_populates='_reviews'),
        '_podcast': relationship(Podcast, back_populates='reviews'),
    })