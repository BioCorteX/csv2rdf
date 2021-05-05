
import pydgraph
import json

def main():
    client_stub = pydgraph.DgraphClientStub("localhost:9080")
    client = pydgraph.DgraphClient(client_stub)
    query = """
{
   q(func: has(Species.name)) {
		Species.name
  }
}
"""

    res = client.txn(read_only=True).query(query)
    data = json.loads(res.json)
    for s in data['q']:

        query = """
{
  q(func: match(Species.name, \"""" + s['Species.name'] + """\", 1)) @filter(NOT eq(Species.name, \"""" + s['Species.name'] + """\")) {
		Species.name
  }
}
    """

        res2 = client.txn(read_only=True).query(query)
        data2 = json.loads(res2.json)
        if len(data2['q']) > 0:
            print(s['Species.name'])
            for s2 in data2['q']:
                print("  ", s2['Species.name'])
    # print('Response: {}'.format(data))

    client_stub.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))

