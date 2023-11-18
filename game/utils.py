def get_tag_contents(response, interest_tag):
    start_index, end_index, length = get_tag_indices(response, interest_tag)
    contents = response[start_index+length:end_index].lstrip(' ').rstrip(' ')
    return contents

def get_tag_indices(response, interest_tag):
    start_index = response.find(f"<{interest_tag}>")
    end_index = response.find(f"</{interest_tag}>")
    return start_index, end_index, len(f"<{interest_tag}>")