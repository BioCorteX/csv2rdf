def build_schema(node_columns, relations):
    nodes_properties = []
    # Define all node properties
    for node, columns in node_columns.items():
        # if node not in nodes_properties:
        #     nodes_properties[node] = []
        for column in columns:
            if column.lower() == node.lower():
                nodes_properties.append('name: string @index(fulltext, term) .')
            else:
                nodes_properties.append(f'{column}: string .')

    # Edges
    for node1, relation, node2 in relations:
        nodes_properties.append(f'{relation}: [uid] @reverse .')

    # Define node type with the calculated properties
    schema = "\n".join(set(nodes_properties))
    return schema


def create_schema(data, filename='schema_generated.dql'):
    node_columns = {}
    for node, df in data['nodes'].items():
        node_columns[node] = list(df.columns)

    relations = data['relations'].keys()
    schema = build_schema(node_columns, relations)

    with open(filename, 'w') as file:
        file.write(schema)

