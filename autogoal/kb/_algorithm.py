import inspect
import warnings
import networkx as nx
from collections import namedtuple

from autogoal.grammar import GraphSpace, Graph, CfgInitializer
from autogoal.utils import nice_repr
from autogoal.kb._data import conforms, build_composite, Tuple


def build_pipelines(input, output, registry) -> 'PipelineBuilder':
    """
    Creates a `PipelineBuilder` instance that generates all pipelines
    from `input` to `output` types.

    ##### Parameters

    - `input`: type descriptor for the desired input.
    - `output`: type descriptor for the desired output.
    - `registry`: list of available classes to build the pipelines.
    """
    G = Graph()

    open_nodes = []
    closed_nodes = set()

    def connect_tuple_wrappers(node, output_type):
        if not isinstance(output_type, Tuple):
            return

        for index in range(0, len(output_type.inner)):
            internal_input = output_type.inner[index]

            for other_clss in registry:
                annotations = _get_annotations(other_clss)
                other_input = annotations.input

                if not (conforms(internal_input, other_input) and other_clss != node):
                    continue

                # `other_class` has input compatible with one element in the Tuple
                # build the output `Tuple[..., internal_output, ...]` of the wrapper class
                internal_output = annotations.output
                output_tuple = list(output_type.inner)
                output_tuple[index] = internal_output
                output_tuple_type = Tuple(*output_tuple)

                # dynamic class representing the wrapper algorithm
                other_wrapper = build_composite(index, output_type, output_tuple_type)
                open_nodes.append(other_wrapper)

                G.add_edge(node, other_wrapper)

    # Enqueue open nodes
    for clss in registry:
        if conforms(input, _get_annotations(clss).input):
            open_nodes.append(clss)
            G.add_edge(GraphSpace.Start, clss)

    connect_tuple_wrappers(GraphSpace.Start, input)

    if GraphSpace.Start not in G:
        raise ValueError("There are no classes compatible with input type.")

    while open_nodes:
        clss = open_nodes.pop(0)

        if clss in closed_nodes:
            continue

        closed_nodes.add(clss)
        output_type = _get_annotations(clss).output

        for other_clss in registry:
            other_input = _get_annotations(other_clss).input
            if conforms(output_type, other_input) and other_clss != clss:
                open_nodes.append(other_clss)
                G.add_edge(clss, other_clss)

        connect_tuple_wrappers(clss, output_type)

        if conforms(output_type, output):
            G.add_edge(clss, GraphSpace.End)

    if GraphSpace.End not in G:
        raise ValueError("No pipelines can be constructed from input to output.")

    reachable_from_end = set(nx.dfs_preorder_nodes(G.reverse(False), GraphSpace.End))
    unreachable_nodes = set(G.nodes) - reachable_from_end
    G.remove_nodes_from(unreachable_nodes)

    if not GraphSpace.Start in G:
        raise ValueError("No pipelines can be constructed from input to output.")

    return PipelineBuilder(G, registry)


@nice_repr
class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def send(self, msg: str, *args, **kwargs):
        found = False
        for step in self.steps:
            if hasattr(step, msg):
                getattr(step, msg)(*args, **kwargs)
                found = True
        if not found:
            warnings.warn(f'No step answered message {msg}.')

    def run(self, x):
        for step in self.steps:
            x = step.run(x)

        return x


class PipelineBuilder(GraphSpace):
    def __init__(self, graph, registry):
        super().__init__(graph, initializer=CfgInitializer(registry=registry))

    def sample(self, *args, **kwargs) -> Pipeline:
        path = super().sample(*args, **kwargs)
        return Pipeline(path)



Annotations = namedtuple("Annotations", ["input", "output"])


def _get_annotations(clss):
    run_method = clss.run
    input_type = inspect.signature(run_method).parameters["input"].annotation
    output_type = inspect.signature(run_method).return_annotation

    return Annotations(input=input_type, output=output_type)


def _has_input(clss, input):
    return conforms(input, _get_annotations(clss).input)


def _has_output(clss, output):
    return conforms(_get_annotations(clss).output, output)
