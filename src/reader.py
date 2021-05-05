import os
import pandas as pd
import glob


def read_csv(filepath):
    filepath_cache = filepath + '.cache'
    if os.path.isfile(filepath_cache):
        df = pd.read_pickle(filepath_cache)
    else:
        df = pd.read_csv(filepath)
        df.to_pickle(filepath_cache)
    return df


def read_nodes(data_path, nodes_path='nodes'):
    node_files = glob.glob(os.path.join(data_path, nodes_path, '*.csv'))
    node_files = {os.path.splitext(os.path.basename(file))[0].lower(): file for file in node_files if not os.path.basename(file).startswith('--')}

    node_dfs = {}
    for node, file in node_files.items():
        node_dfs[node] = read_csv(file)

    return node_dfs


def read_relations(data_path, relations_path='relations'):
    relation_files = glob.glob(os.path.join(data_path, relations_path, '*.csv'))
    relation_files = {os.path.splitext(os.path.basename(file))[0].lower(): file for file in relation_files if not os.path.basename(file).startswith('--')}

    relation_dfs = {}
    for relation, file in relation_files.items():
        relation_dfs[tuple(relation.split("->-"))] = read_csv(file)

    return relation_dfs


def read(version='v1.2', data_root_path='data'):
    data_path = os.path.join(data_root_path, version)
    data = {
        'nodes': read_nodes(data_path),
        'relations': read_relations(data_path)
    }
    return data
