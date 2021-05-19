import hashlib
import sys
from typing import Dict
import pandas as pd
import time
# from numba import jit

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
        s += '_:' + row[index_blank_node] + ' <' + property + '> "' + str(row[index]) + '" .\n'
    return s


# def relations_row_to_rdf(row, index_blank_node1, edge, index_blank_node2):
#     s = '_:' + row[index_blank_node1] + ' <' + edge + '> _:' + row[index_blank_node2] + ' .'
#     return s


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
            df[':blank_node'] = df[uid_column].astype(str).apply(lambda x: hashlib.md5((node + x).lower().encode()).hexdigest())

            df = df.replace({'"': '\\"', '\\\\': '\\\\\\\\', '\n': '\\\\n'}, regex=True)

            # duplicate_index = df.duplicated(subset=':blank_node', keep=False)
            # if len(df[duplicate_index]) > 0:
            #     print(df[duplicate_index])
            #     raise AssertionError(f"Found duplicates in {node}")

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

            if 'Property' in node2:
                node2 = 'Property'

            edge = f"{node1}{edge}{node2}"

            if node1 == node2:
                node2 = node2 + '_1'

            property_columns = [column for column in list(df.columns) if column.lower() not in (node1.lower(), node2.lower())]
            df.loc[:, property_columns] = df[property_columns].replace({'"': '\\"', '\\\\': '\\\\\\\\', '\n': '\\\\n'}, regex=True)
            if len(property_columns) > 0:
                df["edge_properties"] = df[property_columns].apply(lambda row: " (" + ", ".join([f'{column}=' + ('"' if not column.endswith(("DateDisabled", "Float2", "Int2", "Bool")) else '') + f'{row[column]}' + ('"' if not column.endswith(("DateDisabled", "Float2", "Int2", "Bool")) else '') for column in list(row.index)]) + ")", axis=1)
            else:
                df["edge_properties"] = ''

            uid_column = [column for column in list(df.columns) if column.lower() == node1.lower()]
            uid_column = uid_column[0]
            # df[':blank_node1'] = df[uid_column].str.replace('[^a-z0-9A-Z\-_/]', '_', regex=True).str.replace('[^a-z0-9A-Z\-_]', '--', regex=True)
            df[':blank_node1'] = df[uid_column].astype(str).apply(lambda x: hashlib.md5((node1 + x).lower().encode()).hexdigest())

            uid_column = [column for column in list(df.columns) if column.lower() == node2.lower()]
            uid_column = uid_column[0]

            if node2 == node1 + '_1':
                # df[':blank_node2'] = df[uid_column].str.replace('[^a-z0-9A-Z\-_/]', '_', regex=True).str.replace('[^a-z0-9A-Z\-_]', '--', regex=True)
                df[':blank_node2'] = df[uid_column].astype(str).apply(lambda x: hashlib.md5((node1 + x).lower().encode()).hexdigest())

            else:
                df[':blank_node2'] = df[uid_column].astype(str).apply(lambda x: hashlib.md5((node2 + x).lower().encode()).hexdigest())


            # duplicate_index = df.duplicated(subset=[':blank_node1', ':blank_node2'], keep=False)
            # if len(df[duplicate_index]) > 0:
            #     print(df[duplicate_index])
            #     raise AssertionError(f"Found duplicates in node1: {node1} edge: {edge} node2: {node2}")

            # index_blank_node1 = [index for index, column in enumerate(list(df.columns)) if column == ':blank_node1']
            # index_blank_node1 = index_blank_node1[0]
            # index_blank_node2 = [index for index, column in enumerate(list(df.columns)) if column == ':blank_node2']
            # index_blank_node2 = index_blank_node2[0]
            # rdf = df.apply(relations_row_to_rdf, axis=1, index_blank_node1=index_blank_node1, edge=edge, index_blank_node2=index_blank_node2, raw=True)

            # for page in range(int(len(df)/100000) + 1):
            #     print(f".", end='', flush=True)
            #     df2 = df[page*100000:(page+1)*100000]
            #     rdf = '_:' + df2[':blank_node1'] + ' <' + edge + '> _:' + df2[':blank_node2'] + df["edge_properties"] + ' .'
            #     rdf = rdf.str.cat(sep='\n')
            #
            #     file.write(rdf)
            #     file.write('\n')
            # file.write('\n\n')


            prev_tracker = 0
            blank_node1_prev = ''
            blank_node2_prev = ''

            for i in range(len(df)):
                print(f".", end='', flush=True)
                df2 = df
                blank_node1 = df2[':blank_node1'].iloc[i]
                blank_node2 = df2[':blank_node2'].iloc[i]

                if 'Property' in node2:
                    if blank_node1 == blank_node1_prev and blank_node2 == blank_node2_prev:
                        # rdf = '_:' + df2[':blank_node1'].iloc[i] + str(prev_tracker) + ' <dgraph.type> "' + 'abstract_queue' + '" .\n'
                        # rdf += '_:' + df2[':blank_node1'].iloc[i] + str(prev_tracker) + ' <name> "' + df2[':blank_node1'].iloc[i] + str(prev_tracker) + '" .\n'
                        rdf = '_:' + df2[':blank_node1'].iloc[i] + str(prev_tracker) + ' <to> _:' + df2[':blank_node1'].iloc[i] + ' .'
                        rdf += '\n' + '_:' + df2[':blank_node2'].iloc[i] + ' <' + edge + '> _:' + df2[':blank_node1'].iloc[i] + str(prev_tracker) + df[
                            "edge_properties"].iloc[i] + ' .'
                        prev_tracker += 1

                    else:
                        prev_tracker = 0
                        rdf = '_:' + df2[':blank_node1'].iloc[i] + str(prev_tracker) + ' <to> _:' + \
                              df2[':blank_node1'].iloc[i] + ' .'
                        rdf += '\n' + '_:' + df2[':blank_node2'].iloc[i] + ' <' + edge + '> _:' + \
                               df2[':blank_node1'].iloc[i] + str(prev_tracker) + df[
                                   "edge_properties"].iloc[i] + ' .'
                        prev_tracker += 1
                        
                else:
                    rdf = '_:' + df2[':blank_node1'].iloc[i] + ' <' + edge + '> _:' + df2[':blank_node2'].iloc[i] + df["edge_properties"].iloc[i] + ' .'
                    prev_tracker = 0

                blank_node1_prev = df2[':blank_node1'].iloc[i]
                blank_node2_prev = df2[':blank_node2'].iloc[i]

                try:
                    rdf = rdf.str.cat(sep='\n')

                except AttributeError:
                    pass


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