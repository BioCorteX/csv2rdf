def build_schema(node_columns, relations):
    nodes_properties = {}
    # Define all node properties
    for node, columns in node_columns.items():
        if node not in nodes_properties:
            nodes_properties[node] = []
        for column in columns:
            if column.lower() == node.lower():
                nodes_properties[node].append('name: String! @id @search(by: [term, exact, regexp])')
            else:
                nodes_properties[node].append(f'{column}: String')

    # Edges
    for node1, relation, node2 in relations:
        nodes_properties[node1].append(f'{relation}{node2}: [{node2}]')

    # Define node type with the calculated properties
    node_str = []
    for node, properties in nodes_properties.items():
        s = f"\ntype {node} {{"
        s += "\n    "
        s += "\n    ".join(properties)
        s += "\n}"
        node_str.append(s)
    schema = '\n'.join(node_str)
    return schema


def create_schema(data, filename='schema_generated.graphql'):
    node_columns = {}
    for node, df in data['nodes'].items():
        node_columns[node] = list(df.columns)

    relations = data['relations'].keys()
    schema = build_schema(node_columns, relations)

    with open(filename, 'w') as file:
        file.write(schema)

