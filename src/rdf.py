import sys
from typing import Dict
import pandas as pd
import time
# from numba import jit

from pandas.util import hash_pandas_object


# @jit(parallel=True)
def node_row_to_rdf(row, node, columns, index_blank_node):
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


def relations_row_to_rdf(row, index_blank_node1, edge, index_blank_node2):
    s = '_:' + row[index_blank_node1] + ' <' + edge + '> _:' + row[index_blank_node2] + ' .'
    return s


def create_rdf(data: Dict[str, Dict[str, pd.DataFrame]], filename):
    with open(filename, 'w') as file:

        print("Writing Nodes to RDF")
        count = 0
        for node, df in data['nodes'].items():
            count += 1
            start_time = time.time()
            print(f"\t{node} ({len(df)} rows) ({count}/{len(data['nodes'])})", end=' ', flush=True)

            uid_column = [column for column in list(df.columns) if column.lower() == node.lower()]
            uid_column = uid_column[0]
            # df[':blank_node'] = df[uid_column].str.replace('[^a-z0-9A-Z\-_/]', '_', regex=True).str.replace('[^a-z0-9A-Z\-_]', '--', regex=True)
            df[':blank_node'] = hash_pandas_object(df[uid_column]).astype(str)
            df = df.replace({'"': '\\"', '\\\\': '\\\\\\\\', '\n': '\\\\n'}, regex=True)

            duplicate_index = df.duplicated(subset=':blank_node', keep=False)
            if len(df[duplicate_index]) > 0:
                print(df[duplicate_index])
                raise AssertionError(f"Found duplicates in {node}")

            index_blank_node = [index for index, column in enumerate(list(df.columns)) if column == ':blank_node']
            index_blank_node = index_blank_node[0]
            rdf = df.apply(node_row_to_rdf, axis=1, node=node, columns=list(df.columns), index_blank_node=index_blank_node, raw=True)
            rdf = rdf.str.cat(sep='\n')

            file.write(rdf)
            file.write('\n\n')
            print(f"{time.time() - start_time:.2f} s")

        print("Writing Relations to RDF")
        count = 0
        for relation, df in data['relations'].items():
            count += 1
            start_time = time.time()
            print(f"\t{relation} ({len(df)} rows) ({count}/{len(data['relations'])})", end=' ', flush=True)
            node1, edge, node2 = relation

            edge = f"{node1}.{edge}{node2}"

            uid_column = [column for column in list(df.columns) if column.lower() == node1.lower()]
            uid_column = uid_column[0]
            # df[':blank_node1'] = df[uid_column].str.replace('[^a-z0-9A-Z\-_/]', '_', regex=True).str.replace('[^a-z0-9A-Z\-_]', '--', regex=True)
            df[':blank_node1'] = hash_pandas_object(df[uid_column]).astype(str)

            uid_column = [column for column in list(df.columns) if column.lower() == node2.lower()]
            uid_column = uid_column[0]
            # df[':blank_node2'] = df[uid_column].str.replace('[^a-z0-9A-Z\-_/]', '_', regex=True).str.replace('[^a-z0-9A-Z\-_]', '--', regex=True)
            df[':blank_node2'] = hash_pandas_object(df[uid_column]).astype(str)

            df = df.replace({'"': '\\"', '\\\\': '\\\\\\\\', '\n': '\\\\n'}, regex=True)

            duplicate_index = df.duplicated(subset=[':blank_node1', ':blank_node2'], keep=False)
            if len(df[duplicate_index]) > 0:
                print(df[duplicate_index])
                raise AssertionError(f"Found duplicates in node1: {node1} edge: {edge} node2: {node2}")

            # index_blank_node1 = [index for index, column in enumerate(list(df.columns)) if column == ':blank_node1']
            # index_blank_node1 = index_blank_node1[0]
            # index_blank_node2 = [index for index, column in enumerate(list(df.columns)) if column == ':blank_node2']
            # index_blank_node2 = index_blank_node2[0]
            # rdf = df.apply(relations_row_to_rdf, axis=1, index_blank_node1=index_blank_node1, edge=edge, index_blank_node2=index_blank_node2, raw=True)

            for page in range(int(len(df)/100000) + 1):
                print(f".", end='', flush=True)
                df2 = df[page*100000:(page+1)*100000]
                rdf = '_:' + df2[':blank_node1'] + ' <' + edge + '> _:' + df2[':blank_node2'] + ' .'
                rdf = rdf.str.cat(sep='\n')

                file.write(rdf)
                file.write('\n')
            file.write('\n\n')
            print(f" {time.time() - start_time:.2f} s")


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