from autogoal.search import RandomSearch, PESearch
from autogoal.sampling import Sampler

from description import Algorithm, Problem, Extractor, MetaLogger
from meta import MetaSearch
from tools import extract, from_str_to_dict, get_k_fitness

from pathlib import Path
import sys
import os

def std_gen_fn(sampler:Sampler) -> Algorithm:
    alpha = round(sampler.continuous(handle="alpha_h"),10)
    beta = round(sampler.continuous(handle="beta_h"),10)
    return Algorithm(alpha, beta)


def std_fit_fn(alg: Algorithm) -> float:
    return round(alg.run(pbls[it]), 5)


def new_fit_fn(alg: Algorithm) -> float:
    return round(alg.run(new_pbls[it]), 5)


it = 0
pbls = [
    Problem(1,2),
    Problem(2,8),
    Problem(4,5),
    Problem(3,6)
    ]
new_pbls = [
    Problem(4,4),
    Problem(5,8),
    Problem(1,1),
    Problem(9,9)
    ]

k = int(sys.argv[1])

archives = list(os.walk("LOGS/"))[0][2]
f_logs = []

training_logs=[]



Path("TRAINING_LOGS_{0}".format(k)).mkdir(exist_ok= True)

Path("TEST_META_{0}".format(str(k))).mkdir(exist_ok= True)

for iter in range(30):
    for i in range(len(pbls)):
        it = i
        ext = Extractor(pbls[i])

        Path("TRAINING_LOGS_{0}/P{1}".format(str(k), str(it+1))).mkdir(exist_ok=True, parents= True)
        direc = "TRAINING_LOGS_{0}/P{1}/p{1}{2}_k{0}_{3}.json".format(str(k), str(it+1), "meta", str(iter))

        m_logger = MetaLogger(None, extractor=ext, output_file= direc, alg="meta")

        training_logs=[]
        for i in archives:
            for j in from_str_to_dict(extract("LOGS/"+i)):
                training_logs.append(j)

        f_logs = get_k_fitness(k, training_logs)

        m_search = MetaSearch(logs = f_logs, generator_fn = std_gen_fn, fitness_fn = std_fit_fn, evaluation_timeout=0, memory_limit=0)
        m_search.run(generations= 100, logger=m_logger)


# for iter in range(30):
#     for i in range(len(new_pbls)):
#         it = i
#         ext = Extractor(new_pbls[i])

#         training_logs=[]
#         for i in archives:
#             for j in from_str_to_dict(extract("LOGS/"+i)):
#                 training_logs.append(j)

#         f_logs = get_k_fitness(k, training_logs)
        
#         Path("TEST_META_{0}/P{1}".format(str(k), str(it+1))).mkdir(exist_ok=True, parents= True)
#         direc = "TEST_META_{0}/P{1}/p{1}{2}_k{0}_{3}.json".format(str(k), str(it+1), "meta", str(iter))

#         m_logger = MetaLogger(None, extractor=ext, output_file= direc, alg="meta")

#         m_search = MetaSearch(logs = f_logs, generator_fn = std_gen_fn, fitness_fn = new_fit_fn, evaluation_timeout=0, memory_limit=0)
#         m_search.run(generations= 100, logger=m_logger)

