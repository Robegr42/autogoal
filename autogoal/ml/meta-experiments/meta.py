from autogoal.sampling import Sampler, MeanDevParam, UnormalizedWeightParam, WeightParam, DistributionParam
from autogoal.search import PESearch
from typing import Dict


class MetaSampler(Sampler):
    def __init__(self, hist_logs, random_state: int = None):
        super().__init__(random_state=random_state)
        self._model = {}
        self._updates = {}
        self.hist_logs = hist_logs
        

    @property
    def model(self):
        return self._model

    @property
    def updates(self):
        return self._updates


    def _get_model_params(self, handle, default):
        if handle in self._model:
            return self._model[handle]
        else:
            self._model[handle] = default
            return default


    def _register_update(self, handle, result):
        if handle not in self._updates:
            self._updates[handle] = []

        self._updates[handle].append(result)
        return result


    def _clamp(self, x, a, b):
        if x < a:
            return a
        if x > b:
            return b
        return x


    def choice(self, options, handle=None):
        return super().choice(options)


    def boolean(self, handle=None):
        return super().boolean()


    def categorical(self, options, handle=None):
        return super().categorical(options)


    def discrete(self, min=0, max=10, handle=None):
        return super().discrete()


    def continuous(self, min=0, max=1, handle=None):
        if handle is None:
            return super().continuous(min, max, handle)
        
        params = self._get_model_params(
            handle, MeanDevParam(mean=(min + max) / 2, dev=(max - min))
        )

        value = self.hist_logs[handle].pop(0)
        return self._register_update(handle, value)

class MetaSearch(PESearch):
    def __init__(self, logs = None, *args,  **kwargs):
        fit_fn = kwargs.pop("fitness_fn")

        def wrapper(solution):
            if len(self._logs)>0:
                result = self._logs.pop(0)
                return result["fitness"]
            else:
                return fit_fn(solution)

        super().__init__(*args, fitness_fn = wrapper, **kwargs)
        self._logs =logs


    def _update_best(self, best_fn, best_solution):
        if len(self._logs) > 0:
            return 0, None
            
        return super()._update_best(best_fn, best_solution)

    def _build_sampler(self):
        if len(self._logs) == 0:
            return super()._build_sampler()
        else:
            sampler = MetaSampler(self._logs[0]["pipeline_features"])
        self._samplers.append(sampler)

        return sampler
