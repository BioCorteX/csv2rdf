import hashlib
from typing import Dict
import pandas as pd
import time


def node_row_to_rdf(row, node, columns, index_blank_node):
    string = ""
    for index, column in enumerate(columns):
        if column == ':blank_node':
            continue
        property_ = column
        if property_.lower() == node.lower():
            property_ = 'name'
            string += '_:' + row[index_blank_node] + ' <dgraph.type> "' + node + '" .\n'

        if pd.isna(row[index]):
            continue
        string += '_:' + row[index_blank_node] + ' <' + property_ + '> "' + str(row[index]) + '" .\n'
    return string


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
            df[':blank_node'] = df[uid_column].astype(str).apply(lambda x: hashlib.md5((node + x).encode()).hexdigest())

            df = df.replace({'"': '\\"', '\\\\': '\\\\\\\\', '\n': '\\\\n'}, regex=True)

            duplicate_index = df.duplicated(subset=':blank_node', keep=False)
            if len(df[duplicate_index]) > 0:
                print(df[duplicate_index])
                raise AssertionError(f"Found duplicates in {node}")

            index_blank_node = [index for index, column in enumerate(list(df.columns)) if column == ':blank_node']
            index_blank_node = index_blank_node[0]
            rdf = df.apply(node_row_to_rdf, axis=1, node=node, columns=list(df.columns),
                           index_blank_node=index_blank_node, raw=True)
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

            edge = f"{node1}{edge}{node2}"

            property_columns = [column for column in list(df.columns) if
                                column.lower() not in (node1.lower(), node2.lower())]
            df.loc[:, property_columns] = df[property_columns].replace({'"': '\\"', '\\\\': '\\\\\\\\', '\n': '\\\\n'},
                                                                       regex=True)
            if len(property_columns) > 0:
                def foreach(row):
                    string = []
                    for column in list(row.index):
                        quote = ''
                        if column.endswith(("DateDisabled", "Float", "Int", "Bool")):
                            quote = '"'
                        string.append(f'{column}=' + quote + f'{row[column]}' + quote)
                    return " (" + ", ".join(string) + ")"
                df["edge_properties"] = df[property_columns].apply(foreach, axis=1)
            else:
                df["edge_properties"] = ''

            uid_column = [column for column in list(df.columns) if column.lower() == node1.lower()]
            uid_column = uid_column[0]
            df[':blank_node1'] = df[uid_column].astype(str).apply(
                lambda x: hashlib.md5((node1 + x).encode()).hexdigest())

            uid_column = [column for column in list(df.columns) if column.lower() == node2.lower()]
            uid_column = uid_column[0]
            df[':blank_node2'] = df[uid_column].astype(str).apply(
                lambda x: hashlib.md5((node2 + x).encode()).hexdigest())

            duplicate_index = df.duplicated(subset=[':blank_node1', ':blank_node2'], keep=False)
            if len(df[duplicate_index]) > 0:
                print(df[duplicate_index])
                raise AssertionError(f"Found duplicates in node1: {node1} edge: {edge} node2: {node2}")

            for page in range(int(len(df) / 100000) + 1):
                print(".", end='', flush=True)
                df2 = df[page * 100000:(page + 1) * 100000]
                rdf = '_:' + df2[':blank_node1'] + ' <' + edge + '> _:' + df2[':blank_node2'] + df[
                    "edge_properties"] + ' .'
                rdf = rdf.str.cat(sep='\n')

                file.write(rdf)
                file.write('\n')
            file.write('\n\n')
            print(f" {time.time() - start_time:.2f} s")
