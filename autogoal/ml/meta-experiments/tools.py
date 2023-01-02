from typing import Dict, List, Tuple
from math import sqrt
import json

def distance_similarity(x: Tuple, y: Tuple)-> float:
    return sqrt((y[1]-y[0])**2 - (x[1]-x[0])**2)


def from_str_to_dict(str_dict: List[str]) -> List[Dict]:
    return [json.loads(i) for i in str_dict]


def extract(json_file)->List[str]:
    data = ""
    with open(json_file, "r") as fp:
        data = fp.read().split("\n")[:-1]
    return data


def extract_p_feats(d: Dict)->Tuple[int, int]:
    return d["problem_features"]["feature_1"], d["problem_features"]["feature_2"]


def get_k_fitness(k: int, dicts: List[Dict]):
    return sorted(dicts, key= lambda x : x["fitness"], reverse=True)[:k]


def get_best_fn(dicts: List[Dict])-> Tuple[float, float, int]:
    temp = sorted(dicts, key= lambda x : x["fitness"], reverse=True)
    best_fn = temp[0]["fitness"]
    pos = _get_pos("fitness", best_fn, dicts)
    return best_fn, pos, len(dicts)


def _get_pos(key, value, dicts: List[Dict]):
    for i in range(len(dicts)):
        if value == dicts[i][key]:
            return i
    return -1


def get_first_best_pos(k, dicts: List[Dict]):
    temp = sorted(dicts[k+1:], key= lambda x : x["fitness"], reverse=True)
    return _get_pos("fitness", temp[0]["fitness"], dicts)


def get_list_tuple(x, index):
    res = []
    for i in x:
        res.append(i[index])
    return res








 
