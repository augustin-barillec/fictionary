def add_tag_to_text(text, tag):
    res = text.split('\n')
    res = [f'{tag}: ' + line for line in res]
    res = '\n'.join(res)
    return res


def add_tag_to_json(json, tag):
    for k in json:
        if k == 'text' and isinstance(json[k], str):
            json[k] = add_tag_to_text(json[k], tag)
        elif isinstance(json[k], dict):
            json[k] = add_tag_to_json(json[k], tag)
        elif isinstance(json[k], list):
            json[k] = [add_tag_to_json(e, tag) for e in json[k]]
    return json


def add_tag_to_json_list(json_list, tag):
    return [add_tag_to_json(j, tag) for j in json_list]
