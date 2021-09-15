import re


def normalize_name(column, first_character=True):
    column = column[0].lower() + re.sub(r'(?!^)[A-Z]', lambda x: '_' + x.group(0).lower(), column[1:])

    column = column.replace(' ', "_").replace('/', '_').replace('-', '_').replace('.', '_').replace('(', '_').replace(')', '_').replace('&', 'and').lower()
    if first_character:
        property = re.sub(r'(?:^|_)(\w)', lambda x: x.group(1).upper(), column)
    else:
        property = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), column)
    return property


def normalize_list(columns, first_character=False):
    new_columns = []
    for column in columns:
        new_columns.append(normalize_name(column, first_character=first_character))
    return new_columns


def normalize_data(data):
    nodes = list(data['nodes'].keys())
    for node in nodes:
        normalize_node = normalize_name(node)
        data['nodes'][normalize_node] = data['nodes'].pop(node)
        data['nodes'][normalize_node].columns = normalize_list(list(data['nodes'][normalize_node].columns))

    relations = list(data['relations'].keys())
    for relation in relations:
        node1, edge, node2 = relation
        normalized_relation = normalize_name(node1), normalize_name(edge, first_character=False), normalize_name(node2)
        data['relations'][normalized_relation] = data['relations'].pop(relation)
        data['relations'][normalized_relation].columns = normalize_list(list(data['relations'][normalized_relation].columns))

    return data
