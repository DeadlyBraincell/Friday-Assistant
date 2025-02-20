from googlesearch import search

def google_search(query):
    """Performs a Google search and returns top 5 results."""
    results = search(query, num_results=5)
    return results