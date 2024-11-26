from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

def get_number_of_podcast(repo: AbstractRepository):
    return repo.get_number_of_podcasts()
def get_podcasts(repo: AbstractRepository, page: int, per_page: int, page_window: int = 10, category_filter=None, author_filter=None, title_filter=None):
    # Retrieve all podcasts
    all_podcasts = repo.get_podcasts()

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
