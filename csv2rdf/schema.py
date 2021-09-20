
def build_schema(node_columns, relations):
    nodes_properties = []
    nodes_types = {}
    # Define all node properties
    for node, columns in node_columns.items():
        if node not in nodes_types:
            nodes_types[node] = []
        for column in columns:
            if column.lower() == node.lower():
                nodes_properties.append('name: string @index(fulltext, term) .')
                nodes_types[node].append('name')
            else:
                if column.endswith("Float"):
                    nodes_properties.append(f'{column}: float .')
                elif column.endswith("Int"):
                    nodes_properties.append(f'{column}: int .')
                elif column.endswith("Bool"):
                    nodes_properties.append(f'{column}: bool .')
                elif column.endswith("Date"):
                    nodes_properties.append(f'{column}: dateTime .')

                nodes_properties.append(f'{column}: string .')
                nodes_types[node].append(column)

    # Edges
    for node1, relation, node2 in relations:
        if 'Property' in node2:
            node2 = 'Property'
        nodes_properties.append(f'{node1}{relation}{node2}: [uid] @reverse .')
        nodes_types[node1].append(f'{node1}{relation}{node2}')
        nodes_types[node1].append(f'to')

    schema = ''
    # type
    for node, columns in nodes_types.items():
        string = f"type {node} {{\n    "
        string += "\n    ".join(set(columns))
        string += "\n}\n\n"
        schema += string

    # s = f"type abstract_queue {{\n    "
    # s += "\n    ".join(set(columns))
    # s += "\n}\n\n"
    # schema += s

    schema += "\n"

    # Define node type with the calculated properties
    schema += "\n".join(set(nodes_properties))
    schema += '\nto: [uid] @reverse .'
    return schema

 
def create_schema(data, filename='schema_generated.dql'):
    node_columns = {}
    for node, df in data['nodes'].items():
        node_columns[node] = list(df.columns)

    relations = data['relations'].keys()
    schema = build_schema(node_columns, relations)

    with open(filename, 'w') as file:
        file.write(schema)
