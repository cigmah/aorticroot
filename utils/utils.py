""" General utility functions shared across apps."""
from django.conf import settings

PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]

def paginate(page, objects, serializer):
    """Safely paginate a list of objects, returning a paginated object."""
    # Count how many items there are
    count = len(objects)

    # Calculate the item beginning and ending for the page size
    beginning = (page - 1) * PAGE_SIZE
    end = page * PAGE_SIZE

    # If there is nothing, then return nothing
    if count == 0:
        data = {
            "next": None,
            "previous": None,
            "results": [],
            "count": count
        }
        return data
    # If the beginning item it outside the count, then return nothing
    elif beginning >= count:
        previous = (page - 1) if page > 1 else None
        data = {
            "next": None,
            "previous": previous,
            "results": [],
            "count": count
        }
        return data
    # Otherwise subset and return the serialized objectives under results
    else:
        sample = objects[beginning:end]
        serialized = serializer(sample, many=True)

        # Fill in next and previous
        next = (page + 1) if end < count else None
        previous = (page - 1) if page > 1 else None

        # Format into a JSON object
        data = {
            "next": next,
            "previous": previous,
            "results": serialized.data,
            "count": count
        }
        return data
