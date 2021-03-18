from autogoal.sampling import Sampler
import inspect
import abc
import types
import warnings
from typing import Any, Dict, List, Tuple, Type

import networkx as nx
from autogoal.utils import nice_repr
from autogoal.grammar import Graph, GraphSpace, generate_cfg
from autogoal.experimental.semantics import SemanticType, Seq, Vector


class Supervised(SemanticType):
    """Represents a supervised version of some type X.
    
    It is considered a subclass of X for semantic purposes, but not the other way around:

    >>> issubclass(Supervised[Vector], Vector)
    True
    >>> issubclass(Vector, Supervised[Vector])
    False
    
    """
    __internal_types = {}

    @classmethod
    def _specialize(cls, internal_type):
        try:
            return cls.__internal_types[internal_type]
        except KeyError:
            pass

        class SupervisedImp(Supervised):
            __internal = internal_type

            @classmethod
            def _name(cls):
                return f"Supervised[{cls.__internal}]"

            @classmethod
            def _conforms(cls, other: type) -> bool:
                if issubclass(cls.__internal, other):
                    return True

                return False

        cls.__internal_types[internal_type] = SupervisedImp

        return SupervisedImp


def algorithm(*types):
    from autogoal.grammar import Union, Symbol

    *inputs, output = types

    def match(cls):
        if not hasattr(cls, "run"):
            return False

        signature = inspect.signature(cls.run)
        input_types = [v.annotation for k,v in signature.parameters.items() if k != "self"]
        output_type = signature.return_annotation

        if len(inputs) != len(input_types):
            return False

        for expected, real in zip(inputs, input_types):
            if not issubclass(expected, real):
                return False

        if not issubclass(output, output_type):
            return False

        return True       

    class AlgorithmProduction:
        @classmethod
        def generate_cfg(cls, grammar, head):
            symbol = head or Symbol(cls.__name__)
            compatible = []

            for _, other_cls in grammar.namespace.items():
                if match(other_cls):
                    compatible.append(other_cls)

            if not compatible:
                raise ValueError(f"Cannot find any suitable implementation of algorithms with inputs: {inputs} and output: {output}")

            return Union(symbol.name, *compatible).generate_cfg(grammar, symbol)

    return AlgorithmProduction


class Algorithm(abc.ABC):
    """Represents an abstract algorithm with a run method.

    Provides introspection for the expected semantic input and output types.
    Users should inherit from `AlgorithmBase` instead of this class.
    """
    @abc.abstractclassmethod
    def input_types(cls) -> Tuple[type]:
        """Returns an ordered list of the expected semantic input types of the `run` method.
        """
        pass

    @abc.abstractclassmethod
    def output_type(cls) -> type:
        """Returns an ordered list of the expected semantic output type of the `run` method.
        """
        pass

    @abc.abstractmethod
    def run(self, *args):
        """Executes the algorithm.
        """
        pass

    @classmethod
    def is_compatible_with(cls: "Algorithm", input_types):
        """
        Determines if the current algorithm is compatible with a set of input types,
        i.e., if among those types we can find all the necessary inputs for this algorithm.

        >>> class A(AlgorithmBase):
        ...     def run(self, x:int) -> float:
        ...         pass
        >>> A.is_compatible_with([int])
        True
        """
        my_inputs = cls.input_types()

        for needed in my_inputs:
            for having in input_types:
                if issubclass(having, needed):
                    break
            else:
                return False

        return True


class AlgorithmBase(Algorithm):
    """Represents an algorithm. 

    Automatically implements the input and output introspection methods using the `inspect` module.
    Users inheriting from this class must provide type annotations in the `run` method.
    """
    @classmethod
    def input_types(cls) -> Tuple[type]:
        if not hasattr(cls, "__run_signature__"):
            cls.__run_signature__ = inspect.signature(cls.run)

        return tuple(param.annotation for name, param in cls.__run_signature__.parameters.items() if name != 'self')

    @classmethod
    def output_type(cls) -> type:
        if not hasattr(cls, "__run_signature__"):
            cls.__run_signature__ = inspect.signature(cls.run)

        return cls.__run_signature__.return_annotation



def build_input_args(algorithm:Algorithm, values:Dict[type,Any]):
    """Buils the correct input mapping for `algorithm` using the provided `values` mapping types to objects.

    The input can be a class that inherits from `Algorithm` or an instance of such a class.

    >>> class A(AlgorithmBase):
    ...    def run(self, a:int, b:str):
    ...        pass
    >>> values = { str:"hello", float:3.0, int:42 }
    >>> build_input_args(A, values)
    {'a': 42, 'b': 'hello'}
    >>> build_input_args(A(), values)
    {'a': 42, 'b': 'hello'}

    """

    parameters = [p for p in inspect.signature(algorithm.run).parameters if p != "self"]
    result = {}

    for name, type in zip(parameters, algorithm.input_types()):
        try:
            result[name] = values[type]
        except KeyError:
            for key in values:
                if issubclass(key, type):
                    result[name] = values[key]
                    break
            else:
                raise TypeError(f"Cannot find compatible input value for {type}")


    return result


@nice_repr
class Pipeline:
    """Represents a sequence of algorithms.

    Each algorithm must have a `run` method declaring it's input and output type.
    The pipeline instance also receives the input and output types.
    """
    def __init__(self, algorithms:List[Algorithm], input_types:List[Type[SemanticType]]) -> None:
        self.algorithms = algorithms
        self.input_types = input_types

    def run(self, *inputs):
        data = {}

        for i,t in zip(inputs, self.input_types):
            data[t] = i

        for algorithm in self.algorithms:
            args = build_input_args(algorithm, data)
            output = algorithm.run(**args)
            output_type = algorithm.output_type()
            data[output_type] = output

        return data[self.algorithms[-1].output_type()]

    def send(self, msg: str, *args, **kwargs):
        found = False

        for step in self.algorithms:
            if hasattr(step, msg):
                getattr(step, msg)(*args, **kwargs)
                found = True
            elif hasattr(step, "send"):
                step.send(msg, *args, **kwargs)
                found = True

        if not found:
            warnings.warn(f"No step answered message {msg}.")


def _make_seq_algorithm(algorithm: Algorithm):
    """Lift an algorithm with input types T1, T2, Tn to a meta-algorithm with types List[T1], List[T2], ...

    The generated class correctly defines the input and output types.

    >>> class A(AlgorithmBase):
    ...     def __init__(self, alpha):
    ...         self.alpha = 0.5
    ...     def run(self, x:int, y:str) -> float:
    ...         return self.alpha * (x + len(y))
    ...     def __repr__(self):
    ...         return f"A({self.alpha})"
    >>> B = _make_seq_algorithm(A)
    >>> b = B(0.5)
    >>> b
    SeqAlgorithm[A(0.5)]
    >>> b.run([1, 2], ["A", "BC"])
    [1.0, 2.0]
    >>> B.input_types()
    (Seq[<class 'int'>], Seq[<class 'str'>])
    >>> b.output_type()
    Seq[<class 'float'>]
    
    """
    
    output_type = algorithm.output_type()

    name = f"SeqAlgorithm[{algorithm.__name__}]"

    def init_method(self, *args, **kwargs):
        self.inner = algorithm(*args, **kwargs)

    def run_method(self, *args) -> Seq[output_type]:
        return [self.inner.run(*xs) for xs in zip(*args)]

    def repr_method(self):
        return f"SeqAlgorithm[{repr(self.inner)}]"

    def getattr_method(self, attr):
        return getattr(self.inner, attr)

    @classmethod
    def input_types_method(cls):
        return tuple(Seq[t] for t in algorithm.input_types())

    @classmethod
    def output_types_method(cls):
        return Seq[algorithm.output_type()]

    def body(ns):
        ns["__init__"] = init_method
        ns["run"] = run_method
        ns["__repr__"] = repr_method
        ns["__getattr__"] = getattr_method
        ns["input_types"] = input_types_method
        ns["output_type"] = output_types_method

    return types.new_class(name=name, bases=(Algorithm,), exec_body=body)


class PipelineNode:
    def __init__(self, algorithm, input_types, output_types, registry=None) -> None:
        self.algorithm = algorithm
        self.input_types = set(input_types)
        self.output_types = set(output_types)
        self.grammar = generate_cfg(self.algorithm, registry=registry)

    def sample(self, sampler):
        return self.grammar.sample(sampler=sampler)

    @property
    def __name__(self):
        return self.algorithm.__name__

    def __eq__(self, o: object) -> bool:
        return isinstance(o, PipelineNode) and all([
            o.algorithm == self.algorithm,
            o.input_types == self.input_types,
        ])

    def __repr__(self) -> str:
        return f"<PipelineNode(algorithm={self.algorithm.__name__},input_types={[i.__name__ for i in self.input_types]},output_types={[o.__name__ for o in self.output_types]})>"

    def __hash__(self) -> int:
        return hash(repr(self))


class PipelineSpace(GraphSpace):
    def __init__(self, graph: Graph, input_types):
        super().__init__(graph, initializer=self.initialize)
        self.input_types = input_types

    def initialize(self, item: PipelineNode, sampler):
        return item.sample(sampler)

    def sample(self, *args, **kwargs):
        path = super().sample(*args, **kwargs)
        return Pipeline(path, input_types=self.input_types)


def build_pipeline_graph(input_types, output_type, registry, max_list_depth: int=3):
    """Build a graph of algorithms.

    Every node in the graph corresponds to a <autogoal.grammar.ContextFreeGrammar> that
    generates an instance of a class with a `run` method.

    Each `run` method must declare input and output types in the form:

        def run(self, a: type_1, b: type_2, ...) -> type_n:
            # ...
    """
    
    # We start by enlarging the registry with all List[...] algorithms

    pool = set(registry)

    print(pool)

    for algorithm in registry:
        for _ in range(max_list_depth):            
            algorithm = _make_seq_algorithm(algorithm)
            pool.add(algorithm)

    # For building the graph, we'll keep at each node the guaranteed output types

    # We start by collecting all the possible input nodes,
    # those that can process a subset of the input_types
    open_nodes: List[PipelineNode] = []

    for algorithm in registry:
        if not algorithm.is_compatible_with(input_types):
            continue

        open_nodes.append(PipelineNode(
            algorithm = algorithm,
            input_types = input_types,
            output_types = set(input_types) | set([algorithm.output_type()]),
            registry=registry,
        ))

    G = Graph()

    for node in open_nodes:
        G.add_edge(GraphSpace.Start, node)

    # We'll make a BFS exploration of the pipeline space.
    # For every open node we will add to the graph every node to which it can connect.
    closed_nodes = set()

    while open_nodes:
        node = open_nodes.pop(0)

        # These are the types that are available at this node
        guaranteed_types = node.output_types

        # Here are all the algorithms that could be added new at this point in the graph
        for algorithm in registry:
            if not algorithm.is_compatible_with(guaranteed_types):
                continue

            # We never want to apply the same exact algorithm twice
            if algorithm == node.algorithm:
                continue

            # And we never want an algorithm that doesn't provide a novel output type...
            if (algorithm.output_type() in guaranteed_types and 
                # ... unless it is an idempotent algorithm
                [algorithm.output_type()] != algorithm.input_types()
            ) :
                continue

            p = PipelineNode(
                algorithm = algorithm,
                input_types = guaranteed_types,
                output_types = guaranteed_types | set([algorithm.output_type()]),
                registry=registry,
            )

            G.add_edge(node, p)

            if p not in closed_nodes and p not in open_nodes:
                open_nodes.append(p)

        # Now we check to see if this node is a possible output
        if issubclass(node.algorithm.output_type(), output_type):
            G.add_edge(node, GraphSpace.End)

        closed_nodes.add(node)

    # Remove all nodes that are not connected to the end node    
    reachable_from_end = set(nx.dfs_preorder_nodes(G.reverse(False), GraphSpace.End))
    unreachable_nodes = set(G.nodes) - reachable_from_end
    G.remove_nodes_from(unreachable_nodes)

    return PipelineSpace(G, input_types=input_types)
