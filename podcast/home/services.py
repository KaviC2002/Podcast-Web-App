from podcast.adapters.repository import AbstractRepository

def get_podcast(repo: AbstractRepository):
    return repo.get_podcasts()

def get_pagination_podcasts(repo: AbstractRepository, page: int, per_page: int, page_window: int = 10):
    # Retrieve all podcasts and calculate the total number of pages
    all_podcasts = repo.get_podcasts()
    total_podcasts = len(all_podcasts)
    total_pages = (total_podcasts + per_page - 1) // per_page

    # Calculate start and end indices for the current page
    start = (page - 1) * per_page
    end = start + per_page

    # Get the podcasts for the current page
    podcasts = all_podcasts[start:end]

    # Calculate previous and next page numbers
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # Pagination window
    start_page = max(1, page - page_window // 2)
    end_page = min(start_page + page_window - 1, total_pages)

    # Adjust start_page if the window exceeds total_pages
    if end_page < total_pages:
        start_page = start_page
    else:
        start_page = max(1, total_pages - page_window + 1)

    # Return all relevant pagination information
    return podcasts, total_pages, prev_page, next_page, start_page, end_page