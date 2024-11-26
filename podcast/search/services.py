
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast
from typing import List


def search_podcasts(repo: AbstractRepository, query, filter_by):
    query = query.lower()  # Make the query lowercase

    if filter_by == 'title':
        return repo.search_by_title(query)
    elif filter_by == 'category':
        return repo.search_by_category(query)
    elif filter_by == 'author':
        return repo.search_by_author(query)
    else:
        return []


def get_searched_podcasts(all_podcasts: List[Podcast], page: int, per_page: int, page_window: int = 10, category_filter=None, author_filter=None, title_filter=None):

    # Apply filtering based on provided filters
    if category_filter:
        all_podcasts = [podcast for podcast in all_podcasts if category_filter in [cat.name for cat in podcast.categories]]
    if author_filter:
        all_podcasts = [podcast for podcast in all_podcasts if podcast.author.name == author_filter]
    if title_filter:
        all_podcasts = [podcast for podcast in all_podcasts if podcast.title == title_filter]

    # Calculate the total number of pages
    total_podcasts = len(all_podcasts)
    total_pages = (total_podcasts + per_page - 1) // per_page

    # Calculate start and end indices for the current page
    start = (page - 1) * per_page
    end = min(start + per_page, total_podcasts)

    # Get the podcasts for the current page
    podcasts = all_podcasts[start:end]

    # Calculate previous and next page numbers
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # Pagination window
    start_page = max(1, page - page_window // 2)
    end_page = min(start_page + page_window - 1, total_pages)

    # Adjust start_page if the window exceeds total_pages
    if end_page >= total_pages:
        start_page = max(1, total_pages - page_window + 1)

    return podcasts, total_pages, prev_page, next_page, start_page, end_page
