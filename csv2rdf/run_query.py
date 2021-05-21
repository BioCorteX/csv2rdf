import sys
import requests


def run_query(query_to_ask, debug=False):
    print(query_to_ask)
    request = requests.post('http://localhost:8080/graphql', json={'query': query_to_ask})
    if debug:
        print(request.request.url)
        print(request.request.body)
        print(request.request.headers)
    if request.status_code != 200:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query_to_ask))
    return request.json()


if __name__ == '__main__':
    from pathlib import Path
    query = Path(sys.argv[1]).read_text().replace('\n', '')

    result = run_query(query)
    print(f"{result}")
