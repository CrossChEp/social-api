import json
import os
from store.config import FILENAME


def create_request(user_sender: int, user_receiver: int):
    path = os.path.relpath(FILENAME)
    if not os.path.exists(path):
        req_list: dict = {}
    else:
        req_list = get_requests()

    with open(path, 'w') as out:
        next_index = 0
        if req_list:
            next_index = sorted(map(lambda x: int(x), req_list.keys()))[-1] + 1

        req_list[next_index] = {"user_sender": user_sender, "user_receiver": user_receiver}
        json.dump(req_list, out)
        return {"request_id": next_index}


def parse_request(request_id: int):
    request_id = str(request_id)

    data: dict = get_requests()

    request: dict = data.get(request_id)

    if request is None:
        return {}

    data.pop(request_id)

    with open(FILENAME, 'w') as file:
        json.dump(data, file)

    return request


def get_requests():
    if not os.path.exists(FILENAME):
        open(FILENAME, 'w').close()

    with open(FILENAME, 'r') as file:
        test_data = file.read()
        if test_data == "" or (test_data[0] != '{' or test_data[-1] != '}'):
            return {}

        file.seek(0)
        requests: dict = json.load(file)
        return requests


def delete_request(request_id: int):
    requests = get_requests()
    req: dict = requests.get(str(request_id))
    if req is None:
        raise KeyError("Not found request with given id")

    requests.pop(str(request_id))
    with open(FILENAME, 'w') as f:
        json.dump(requests, f)
