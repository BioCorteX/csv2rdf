import json
import pydgraph


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
    for specie in data['q']:
        query = """
{
  q(func: match(Species.name, \"""" + specie['Species.name'] + """\", 1))
   @filter(NOT eq(Species.name, \"""" + specie['Species.name'] + """\")) {
		Species.name
  }
}
    """

        res2 = client.txn(read_only=True).query(query)
        data2 = json.loads(res2.json)
        if len(data2['q']) > 0:
            print(specie['Species.name'])
            for specie2 in data2['q']:
                print("  ", specie2['Species.name'])
    # print('Response: {}'.format(data))

    client_stub.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as exp:
        print('Error: {}'.format(exp))
