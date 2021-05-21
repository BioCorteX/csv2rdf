import sys
import requests


def run_query(query, debug=False):
    print(query)
    request = requests.post('http://localhost:8080/graphql', json={'query': query})
    if debug:
        print(request.request.url)
        print(request.request.body)
        print(request.request.headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
from pathlib import Path
query = Path(sys.argv[1]).read_text().replace('\n', '')

result = run_query(query)
print(f"{result}")
