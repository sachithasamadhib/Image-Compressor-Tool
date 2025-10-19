def merge_sort_by_date(history_list, ascending=True):
    """
    Sort history list by date using merge sort algorithm
    
    Args:
        history_list: List of history records with 'timestamp' field
        ascending: Boolean to determine sort order (True for oldest first, False for newest first)
    
    Returns:
        Sorted list of history records
    """
    if len(history_list) <= 1:
        return history_list
    
    # Divide
    mid = len(history_list) // 2
    left_half = history_list[:mid]
    right_half = history_list[mid:]
    
    # Recursively sort both halves
    left_sorted = merge_sort_by_date(left_half, ascending)
    right_sorted = merge_sort_by_date(right_half, ascending)
    
    # Merge the sorted halves
    return merge_by_date(left_sorted, right_sorted, ascending)


def merge_by_date(left, right, ascending):
    """
    Merge two sorted lists by date
    
    Args:
        left: Left sorted list
        right: Right sorted list  
        ascending: Sort order
        
    Returns:
        Merged sorted list
    """
    merged = []
    left_index = 0
    right_index = 0
    
    # Merge elements while both lists have elements
    while left_index < len(left) and right_index < len(right):
        left_date = left[left_index]['timestamp']
        right_date = right[right_index]['timestamp']
        
        # Compare dates based on sort order
        if (ascending and left_date <= right_date) or (not ascending and left_date >= right_date):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    
    # Add remaining elements from left list
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1
    
    # Add remaining elements from right list
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1
    
    return merged


def merge_sort_by_size(history_list, ascending=True):
    """
    Sort history list by original file size using merge sort algorithm
    
    Args:
        history_list: List of history records with 'original_size' field
        ascending: Boolean to determine sort order (True for smallest first, False for largest first)
    
    Returns:
        Sorted list of history records
    """
    if len(history_list) <= 1:
        return history_list
    
    # Divide
    mid = len(history_list) // 2
    left_half = history_list[:mid]
    right_half = history_list[mid:]
    
    # Recursively sort both halves
    left_sorted = merge_sort_by_size(left_half, ascending)
    right_sorted = merge_sort_by_size(right_half, ascending)
    
    # Merge the sorted halves
    return merge_by_size(left_sorted, right_sorted, ascending)


def merge_by_size(left, right, ascending):
    """
    Merge two sorted lists by file size
    
    Args:
        left: Left sorted list
        right: Right sorted list
        ascending: Sort order
        
    Returns:
        Merged sorted list
    """
    merged = []
    left_index = 0
    right_index = 0
    
    # Merge elements while both lists have elements
    while left_index < len(left) and right_index < len(right):
        left_size = left[left_index]['original_size']
        right_size = right[right_index]['original_size']
        
        # Compare sizes based on sort order
        if (ascending and left_size <= right_size) or (not ascending and left_size >= right_size):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    
    # Add remaining elements from left list
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1
    
    # Add remaining elements from right list
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1
    
    return merged


def merge_sort_by_compression_ratio(history_list, ascending=True):
    """
    Sort history list by compression ratio using merge sort algorithm
    
    Args:
        history_list: List of history records with 'compression_ratio' field
        ascending: Boolean to determine sort order (True for lowest ratio first, False for highest first)
    
    Returns:
        Sorted list of history records
    """
    if len(history_list) <= 1:
        return history_list
    
    # Divide
    mid = len(history_list) // 2
    left_half = history_list[:mid]
    right_half = history_list[mid:]
    
    # Recursively sort both halves
    left_sorted = merge_sort_by_compression_ratio(left_half, ascending)
    right_sorted = merge_sort_by_compression_ratio(right_half, ascending)
    
    # Merge the sorted halves
    return merge_by_compression_ratio(left_sorted, right_sorted, ascending)


def merge_by_compression_ratio(left, right, ascending):
    """
    Merge two sorted lists by compression ratio
    
    Args:
        left: Left sorted list
        right: Right sorted list
        ascending: Sort order
        
    Returns:
        Merged sorted list
    """
    merged = []
    left_index = 0
    right_index = 0
    
    # Merge elements while both lists have elements
    while left_index < len(left) and right_index < len(right):
        left_ratio = left[left_index]['compression_ratio']
        right_ratio = right[right_index]['compression_ratio']
        
        # Compare ratios based on sort order
        if (ascending and left_ratio <= right_ratio) or (not ascending and left_ratio >= right_ratio):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    
    # Add remaining elements from left list
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1
    
    # Add remaining elements from right list
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1
    
    return merged