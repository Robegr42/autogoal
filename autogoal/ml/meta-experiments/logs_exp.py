from autogoal.search import PESearch, RandomSearch
from autogoal.sampling import Sampler

from description import Algorithm, Problem, Extractor, MetaLogger

from pathlib import Path

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
    Problem(4,5),
    Problem(3,8),
    Problem(9,1),
    Problem(3,6)
    ]
new_pbls = [
    Problem(4,4),
    Problem(5,8),
    Problem(1,1),
    Problem(9,9)
    ]

Path("LOGS").mkdir(exist_ok= True)
Path("PGE").mkdir(exist_ok= True)


for i in range(len(pbls)):
    it = i
    ext = Extractor(pbls[it])

    r_logg = MetaLogger(None, extractor=ext, output_file= "LOGS/p{0}{1}.json".format(str(it+1), "random"), alg="random")
    r = RandomSearch(generator_fn = std_gen_fn, fitness_fn = std_fit_fn)
    r.run(generations=100, logger=r_logg)


for iter in range(30):
    for i in range(len(pbls)):
        it = i
        ext = Extractor(pbls[it])
        Path("PGE/P{0}".format(str(it+1))).mkdir(exist_ok= True)
        pes_logg = MetaLogger(None, extractor=ext, output_file= "PGE/P{0}/p{0}{1}{2}.json".format(str(it+1), "pge", str(iter)), alg="pge")
        pes = PESearch(generator_fn = std_gen_fn, fitness_fn = std_fit_fn)
        pes.run(generations=100, logger=pes_logg)


Path("NEW_TEST_PGE").mkdir(exist_ok= True)
for iter in range(30):
    for i in range(len(new_pbls)):
        it = i
        ext = Extractor(new_pbls[i])
        Path("NEW_TEST_PGE/P{0}".format(str(it+1))).mkdir(exist_ok= True)
        pes_logg = MetaLogger(None, extractor=ext, output_file= "NEW_TEST_PGE/P{0}/p{0}{1}{2}.json".format(str(it+1), "pge", str(iter)), alg="pge")

        pes = PESearch(generator_fn = std_gen_fn, fitness_fn = new_fit_fn)
        pes.run(generations=100, logger=pes_logg)