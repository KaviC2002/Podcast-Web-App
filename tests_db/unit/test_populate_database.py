from sqlalchemy import select, inspect

from podcast.adapters.orm import mapper_registry

# run db test with python -m pytest -v tests_db


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # test if all the tables are created well in the db
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'playlist_podcasts',
                                           'playlists', 'podcast_categories', 'podcasts', 'reviews', 'users']


def test_database_populate_select_all_authors(database_engine):
    # test if all the authors are populated into the db table
    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table authors
        select_statement = select(mapper_registry.metadata.tables[name_of_authors_table])
        # must do mappings().all() to get a dictionary like result(table) instead of a tuple
        result = connection.execute(select_statement).mappings().all()

        all_authors = []
        for row in result:
            all_authors.append((
                row['author_id'],
                row['name'],
            ))

    assert len(all_authors) == 982

def test_database_populate_select_all_categories(database_engine):
    # test if all the categories are populated into the db table
    # Get table information
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table authors
        select_statement = select(mapper_registry.metadata.tables[name_of_categories_table])
        # must do mappings().all() to get a dictionary like result(table) instead of a tuple
        result = connection.execute(select_statement).mappings().all()

        all_categories = []
        for row in result:
            all_categories.append((
                row['category_id'],
                row['category_name'],
            ))

    assert len(all_categories) == 2166


def test_database_populate_select_all_episodes(database_engine):
    # test if all the episodes are populated into the db table
    # Get table information
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table authors
        select_statement = select(mapper_registry.metadata.tables[name_of_episodes_table])
        # must do mappings().all() to get a dictionary like result(table) instead of a tuple
        result = connection.execute(select_statement).mappings().all()

        all_episodes = []
        for row in result:
            all_episodes.append((
                row['episode_id'],
                row['podcast_id'],
                row['title'],
                row['audio_url'],
                row['length'],
                row['description'],
                row['pub_date'],
            ))

    assert len(all_episodes) == 5370

def test_database_populate_select_all_podcast_categories(database_engine):
    # test if all the association between podcast and categories are populated into the db table
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcast_categories_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table podcast categories
        select_statement = select(mapper_registry.metadata.tables[name_of_podcast_categories_table])
        # must do mappings().all() to get a dictionary like result(table) instead of a tuple
        result = connection.execute(select_statement).mappings().all()

        all_podcast_categories = []
        for row in result:
            all_podcast_categories.append((
                row['id'],
                row['podcast_id'],
                row['category_id'],
            ))

    assert len(all_podcast_categories) == 2166

def test_database_populate_select_all_podcasts(database_engine):
    # test if all the podcasts are populated into the db table
    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table podcasts
        select_statement = select(mapper_registry.metadata.tables[name_of_podcasts_table])
        # must do mappings().all() to get a dictionary like result(table) instead of a tuple
        result = connection.execute(select_statement).mappings().all()

        all_podcasts = []
        for row in result:
            all_podcasts.append((
                row['podcast_id'],
                row['title'],
                row['image_url'],
                row['description'],
                row['language'],
                row['website_url'],
                row['author_id'],
                row['itunes_id'],
            ))

    assert len(all_podcasts) == 982

