import re
from contextlib import redirect_stdout
from io import StringIO
from typing import Union, Optional

from rdflib import Graph
from rdflib.compare import to_isomorphic, IsomorphicGraph, graph_diff

from biolinkml import METAMODEL_NAMESPACE


def to_graph(inp: Union[Graph, str], fmt: Optional[str] = "turtle") -> Graph:
    """
    Convert inp into a graph
    :param inp: Graph, file name, url or text
    :param fmt: expected format of inp
    :return: Graph representing inp
    """
    if isinstance(inp, Graph):
        return inp
    g = Graph()
    if not inp.strip().startswith('{') and '\n' not in inp and '\r' not in inp:
        with open(inp) as f:
            inp = f.read()
    g.parse(data=inp, format=fmt)
    return g


def print_triples(g: Graph) -> None:
    """
    Print the contents of g into stdout
    :param g: graph to print
    """
    g.bind('meta', METAMODEL_NAMESPACE)
    g_text = re.sub(r'@prefix.*\n', '', g.serialize(format="turtle").decode())
    print(g_text)


def compare_rdf(expected: Union[Graph, str], actual: Union[Graph, str], fmt: Optional[str] = "turtle") -> Optional[str]:
    """
    Compare expected to actual, returning a string if there is a difference
    :param expected: expected RDF. Can be Graph, file name, uri or text
    :param actual: actual RDF. Can be Graph, file name, uri or text
    :param fmt: RDF format
    :return: None if they match else summary of difference
    """
    def rem_metadata(g: Graph) -> IsomorphicGraph:
        g_iso = to_isomorphic(g)
        for t in list(g_iso.triples((None, METAMODEL_NAMESPACE.generation_date, None))):
            g_iso.remove(t)
        for t in list(g_iso.triples((None, METAMODEL_NAMESPACE.source_file_date, None))):
            g_iso.remove(t)
        for t in list(g_iso.triples((None, METAMODEL_NAMESPACE.source_file_size, None))):
            g_iso.remove(t)
        return g_iso

    expected_graph = to_graph(expected, fmt)
    expected_isomorphic = rem_metadata(expected_graph)
    actual_graph = to_graph(actual, fmt)
    actual_isomorphic = rem_metadata(actual_graph)

    # Graph compare takes a Looong time
    in_both, in_old, in_new = graph_diff(expected_isomorphic, actual_isomorphic)
    # if old_iso != new_iso:
    #     in_both, in_old, in_new = graph_diff(old_iso, new_iso)
    old_len = len(list(in_old))
    new_len = len(list(in_new))
    if old_len or new_len:
        txt = StringIO()
        with redirect_stdout(txt):
            if old_len:
                print("----- Expected graph -----")
                print_triples(in_old)
            if new_len:
                print("----- Actual Graph -----")
                print_triples(in_new)
        return txt.getvalue()
    return None
