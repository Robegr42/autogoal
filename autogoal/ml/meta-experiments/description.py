from autogoal.ml._metalearning import DatasetFeatureLogger
from autogoal.ml._metalearning import SolutionInfo
from math import sqrt, cos
import json

class MetaLogger(DatasetFeatureLogger):
    def __init__(self, X, y=None, extractor=None, output_file="metalearning.json", problem_features=None, environment_features=None, alg = ""):
        super().__init__(X, y, extractor, output_file, problem_features, environment_features)
        self.alg = alg

    def begin(self, generations, pop_size):
        self.dataset_features_ = self.extractor.extract_features()
    
    def eval_solution(self, solution, fitness):
        if not hasattr(solution, "sampler_"):
            raise ("Cannot log if the underlying algorithm is not PESearch")

        features = {"alpha_h": [solution.alpha_h], "beta_h": [solution.beta_h]}

        info = SolutionInfo(
            uuid=self.run_id,
            fitness=fitness,
            problem_features= self.dataset_features_,
            environment_features=None,
            pipeline_features=features,
            feature_types=None,
        ).to_dict()
        
        info["algorithm"] = self.alg

        with open(self.output_file, "a") as fp:
            fp.write(json.dumps(info) + "\n")


class Problem:
    def __init__(self, pd1: float, pd2: float) -> None:
        self.pd1 = pd1
        self.pd2 = pd2


class Algorithm:
    def __init__(self, alpha: float, beta: float) -> None:
        self.alpha_h = alpha
        self.beta_h = beta

    def run(self, p: Problem)-> float:
        dist1 = abs(0.5-self.alpha_h)
        dist2 = abs(0.5-self.alpha_h)
        return cos(dist1)+cos(dist2)/(p.pd1 * p.pd2)


class Extractor:

    def __init__(self, p: Problem) -> None:
        self.p = p

    def extract_features(self):
        return {"feature_1":self.p.pd1, "feature_2":self.p.pd2}

