from typing import Dict
import pandas as pd
# from numba import jit


# @jit(parallel=True)
def row_to_rdf(row, node, columns, index_blank_node):
    s = ""
    for index, column in enumerate(columns):
        if column == ':blank_node':
            continue
        property = column
        if property.lower() == node.lower():
            property = 'name'
            s += '_:' + row[index_blank_node] + ' <dgraph.type> "' + node + '" .\n'

        if pd.isna(row[index]):
            continue
        s += '_:' + row[index_blank_node] + ' <' + node + '.' + property + '> "' + row[index] + '" .\n'
    return s


def create_rdf(data: Dict[str, Dict[str, pd.DataFrame]], filename):
    with open(filename, 'w') as file:
        for node, df in data['nodes'].items():
            uid_column = [column for column in list(df.columns) if column.lower() == node.lower()]
            uid_column = uid_column[0]
            df[':blank_node'] = df[uid_column].str.replace('[^a-z0-9A-Z\-_/]', '_', regex=True).str.replace('[^a-z0-9A-Z\-_]', '-', regex=True)
            df = df.replace({'"': '\\"', '\\\\': '\\\\\\\\', '\n': '\\\\n'}, regex=True)

            duplicate_index = df.duplicated(subset=':blank_node', keep=False)
            if len(df[duplicate_index]) > 0:
                print(df[duplicate_index])
                raise AssertionError(f"Found duplicates in {node}")

            index_blank_node = [index for index, column in enumerate(list(df.columns)) if column == ':blank_node']
            index_blank_node = index_blank_node[0]
            rdf = df.apply(row_to_rdf, axis=1, node=node, columns=list(df.columns), index_blank_node=index_blank_node, raw=True)
            rdf = rdf.str.cat(sep='\n')

            file.write(rdf)
            file.write('\n\n')


"""
    _:class <student> _:x .
    _:class <student> _:y .
    _:class <name> "awesome class" .
    _:class <dgraph.type> "Class" .
    _:x <name> "Alice" .
    _:x <dgraph.type> "Person" .
    _:x <dgraph.type> "Student" .
    _:x <planet> "Mars" .
    _:x <friend> _:y .
    _:y <name> "Bob" .
    _:y <dgraph.type> "Person" .
    _:y <dgraph.type> "Student" .
"""