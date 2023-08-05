#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2019/11/12 15:13
# @Email   : 986798607@qq.com
# @Software: PyCharm
# @License: GNU Lesser General Public License v3.0

"""
Notes:
    this part are one copy from deap,
    change the random to numpy.random
"""
import copy
import operator
import sys
from collections import Counter
from functools import wraps
from inspect import isclass

from deap.tools import Statistics, MultiStatistics
from numpy import random
from operator import attrgetter
from featurebox.symbol.dim import Dim, dnan
import numpy as np


# from featurebox.tools.tool import logg
# from featurebox.tools.tool import logg
######################################
# Generate                         #
######################################


def checkss(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        pset = kwargs["pset"]
        for i in result[0].bot():
            assert i in pset.dispose
        for i in result[0].top():
            assert i in pset.primitives + pset.terminals_and_constants

        return result

    return wrapper


def generate(pset, min_, max_, condition, personal_map=False, *kwargs):
    """

    Parameters
    ----------
    pset: SymbolSet
    min_: int
        Minimum height of the produced trees.
    max_: int
        Maximum Height of the produced trees.
    condition: collections.Callable
        The condition is a function that takes two arguments,
        the height of the tree to build and the current
        depth in the tree.
    kwargs: None
        placeholder for future
    personal_map:bool

    Returns
    -------

    """
    _ = kwargs
    type_ = object
    expr = []
    height = random.randint(min_, max_)
    stack = [(0, type_)]
    while len(stack) != 0:
        depth, type_ = stack.pop()
        if condition(height, depth):
            try:
                if personal_map:
                    p_t = pset.premap.get_ind_value(expr, pset)
                else:
                    p_t = pset.prob_ter_con_list
                if p_t is None:
                    p_t = pset.prob_ter_con_list

                term = pset.terminals_and_constants[random.choice(len(pset.terminals_and_constants),
                                                                  p=p_t)]

            except IndexError:
                _, _, traceback = sys.exc_info()
                raise IndexError("The symbol.generate function tried to add "
                                 "a terminalm, but there is "
                                 "none available.").with_traceback(traceback)
            if isclass(term):
                term = term()
            expr.append(term)
        else:
            try:
                prim = pset.primitives[random.choice(len(pset.primitives), p=pset.prob_pri_list)]
            except IndexError:
                _, _, traceback = sys.exc_info()
                raise IndexError("The symbol.generate function tried to add "
                                 "a primitive', but there is "
                                 "none available.").with_traceback(traceback)
            expr.append(prim)
            for arg in reversed(prim.args):
                stack.append((depth + 1, arg))

    dispose = list(random.choice(pset.dispose, len(expr), p=pset.prob_dispose_list))

    add_ = [i for i in pset.dispose if i.name == "MAdd"]
    mul_ = [i for i in pset.dispose if i.name == "MMul"]
    add_.extend(mul_)

    dispose[0] = random.choice(add_, p=[0.8, 0.2])

    re = []
    for i, j in zip(dispose, expr):
        re.extend((i, j))

    return re


def genGrow(pset, min_, max_, personal_map=False, ):
    """Generate an expression where each leaf might have a different depth
    between *min* and *max*.

    :param pset: Primitive set from which primitives are selected.
    :param min_: Minimum height of the produced trees.
    :param max_: Maximum Height of the produced trees.
    :param personal_map: bool
    :returns: A grown tree with leaves at possibly different depths.

    """

    def condition(height, depth):
        """Expression generation stops when the depth is equal to height
        or when it is randomly determined that a node should be a terminal.
        """
        return depth == height or (depth >= min_ and random.random() < pset.terminalRatio)

    return generate(pset, min_, max_, condition, personal_map=personal_map)


def compile_(expr, pset):
    """Compile the expression *expr*.

    :param expr: Expression to compile. It can either be a PrimitiveTree,
                 a string of Python code or any object that when
                 converted into string produced a valid Python code
                 expression.
    :param pset: Primitive set against which the expression is compile.
    :returns: a function if the primitive set has 1 or more arguments,
              or return the results produced by evaluating the tree.
    """
    if isinstance(expr, str):
        code = expr
    else:
        code = repr(expr)
    if len(pset.arguments) > 0:
        # This section is a stripped version of the lambdify
        # function of SymPy 0.6.6.
        args = ",".join(arg for arg in pset.arguments)
        code = "lambda {args}: {code}".format(args=args, code=code)
    try:
        return eval(code, pset.context, {})
    except MemoryError:
        _, _, traceback = sys.exc_info()
        raise MemoryError("DEAP : Error in tree evaluation :"
                          " Python cannot evaluate a tree higher than 90. "
                          "To avoid this problem, you should use bloat control on your "
                          "operators. See the DEAP documentation for more information. "
                          "DEAP will now abort.").with_traceback(traceback)


def compile_context(expr, context):
    """Compile the expression *expr*.

    :param expr: Expression to compile. It can either be a PrimitiveTree,
                 a string of Python code or any object that when
                 converted into string produced a valid Python code
                 expression.
    :param context: dict
    :returns: a function if the primitive set has 1 or more arguments,
              or return the results produced by evaluating the tree.
    """
    if isinstance(expr, str):
        code = expr
    else:
        code = repr(expr)

    try:
        return eval(code, context, {})
    except MemoryError:
        _, _, traceback = sys.exc_info()
        raise MemoryError("DEAP : Error in tree evaluation :"
                          " Python cannot evaluate a tree higher than 90. "
                          "To avoid this problem, you should use bloat control on your "
                          "operators. See the DEAP documentation for more information. "
                          "DEAP will now abort.").with_traceback(traceback)


def depart(individual):
    if len(individual) <= 10 or individual.height <= 8:
        return [individual, ]
    else:
        inds = []
        for index in np.arange(2, len(individual) - 4, step=2):
            slice_ = individual.searchSubtree(index)
            ind_new = individual.__class__(individual[slice_])
            if 6 <= len(ind_new) <= 10 or 4 <= ind_new.height <= 8:
                if len(ind_new.ter_site()) >= 2:
                    ind_new[0] = individual[0]
                    inds.append(ind_new)

        return inds


def genFull(pset, min_, max_, personal_map=False):
    """Generate an expression where each leaf has the same depth
    between *min* and *max*.

    :param pset: Primitive set from which primitives are selected.
    :param min_: Minimum height of the produced trees.
    :param max_: Maximum Height of the produced trees.
    :param personal_map:

    :returns: A full tree with all leaves at the same depth.
    """

    def condition(height, depth):
        """Expression generation stops when the depth is equal to height."""
        return depth == height

    return generate(pset, min_, max_, condition, personal_map=personal_map)


######################################
# crossover                        #
######################################
def cxOnePoint(ind10, ind20):
    """Randomly select crossover point in each individual and exchange each
    subtree with the point as root between each individual.

    :param ind10: First tree participating in the crossover.
    :param ind20: Second tree participating in the crossover.
    :returns: A tuple of two trees.
    """
    ind1 = copy.copy(ind10)
    ind2 = copy.copy(ind20)

    if len(ind1) < 4 or len(ind2) < 4:

        return ind1, ind2
    #
    else:
        index1 = random.choice(np.arange(2, len(ind1) - 1, 2))
        index2 = random.choice(np.arange(2, len(ind2) - 1, 2))
        slice1 = ind1.searchSubtree(index1)
        slice2 = ind2.searchSubtree(index2)

        ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2


######################################
# limitation                       #
######################################


def staticLimit(key, max_value):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            keep_inds = [copy.deepcopy(ind) for ind in args]
            new_inds = list(func(*args, **kwargs))
            for i, ind in enumerate(new_inds):

                if key(ind) > max_value:
                    new_inds[i] = keep_inds[random.choice(len(keep_inds))]

            return new_inds

        return wrapper

    return decorator


######################################
# mutate                       #
######################################
# @logg
# @checkss
def mutUniform(individual, expr, pset):
    """Randomly select a point in the tree *individual*, then replace the
    subtree at that point as a root by the expression generated using method
    :func:`expr`.

    :param individual: The tree to be mutated.
    :param expr: A function object that can generate an expression when
                 called.
    :param pset: SymbolSet
    :returns: A tuple of one tree.

    """
    index = random.choice(len(individual))
    if index % 2 == 1:
        index -= 1
    slice_ = individual.searchSubtree(index)

    individual[slice_] = expr(pset=pset)
    return individual,


# @logg
# @checkss
def mutNodeReplacement(individual, pset):
    """Replaces a randomly chosen primitive from *individual* by a randomly
    chosen primitive with the same number of arguments from the :attr:`pset`
    attribute of the individual.

    :param individual: The normal or typed tree to be mutated.
    :param pset: SymbolSet
    :returns: A tuple of one tree.
    """

    if len(individual) < 4:
        return individual,

    if random.random() <= 0.8:
        index = random.choice(np.arange(1, len(individual), step=2))
    else:
        index = random.choice(np.arange(0, len(individual), step=2))

    node = individual[index]

    if index % 2 == 0:
        for i in pset.dispose:
            assert i.arity == 1
        prims = pset.dispose
        p_d = np.array([pset.prob_dispose[repr(i)] for i in prims], 'float32')
        p_d /= np.sum(p_d)
        a = prims[random.choice(len(prims), p=p_d)]
        individual[index] = a
    else:

        if node.arity == 0:  # Terminal
            p_t = pset.prob_ter_con_list
            term = pset.terminals_and_constants[random.choice(len(pset.terminals_and_constants), p=p_t)]
            individual[index] = term
        else:  # Primitive
            prims = [p for p in pset.primitives if p.arity == node.arity]
            p_p = np.array([pset.prob_pri[repr(i)] for i in prims], 'float32')

            p_p /= np.sum(p_p)
            # except:
            a = prims[random.choice(len(prims), p=p_p)]

            individual[index] = a

    return individual,


# @logg
# @checkss
def mutDifferentReplacement(individual, pset):
    """Replaces a randomly chosen primitive from *individual* by a randomly
    chosen primitive with the same number of arguments from the :attr:`pset`
    attribute of the individual.
    decrease the probability of same terminals.

    :param individual: The normal or typed tree to be mutated.
    :param pset: SymbolSet
    :returns: A tuple of one tree.
    """
    if len(individual) < 4:
        return individual,

    ters = [repr(i) for i in individual.terminals()]
    pset_ters = [repr(i) for i in pset.terminals_and_constants]

    cou = Counter(ters)
    cou_mutil = {i: j for i, j in cou.items() if j >= 2}
    ks = list(cou_mutil.keys())
    nks = list(set(pset_ters) - (set(ks)))

    p_nks = np.array([pset.prob_ter_con[i] for i in nks])
    p_nks /= np.sum(p_nks)

    if cou_mutil:
        indexs = []
        for k, v in cou_mutil.items():
            indi = []
            for i in np.arange(1, len(individual), 2):
                if repr(individual[i]) == k:
                    indi.append(i)
            if indi:
                indexs.append(random.choice(indi))
        if len(indexs) <= len(nks):
            term = random.choice(nks, len(indexs), replace=False, p=p_nks)
        else:
            term = random.choice(nks, len(indexs), replace=True, p=p_nks)

        term_ters = []
        for name in term:
            for i in pset.terminals_and_constants:
                if repr(i) == name:
                    term_ters.append(i)

        for o, n in zip(indexs, term_ters):
            individual[o] = n

    return individual,


# @logg
# @checkss
def mutShrink(individual, pset=None):
    """This operator shrinks the *individual* by choosing randomly a branch and
    replacing it with one of the branch's arguments (also randomly chosen).

    :param individual: The tree to be shrinked.
    :param pset: SymbolSet.
    :returns: A tuple of one tree.
    """
    _ = pset
    # We don't want to "shrink" the root
    if len(individual) < 6 or individual.height <= 4:
        return individual,

    index = random.randint(0, len(individual))

    if index % 2 == 1:
        index -= 1
    slice_ = individual.searchSubtree(index)

    ter = [i for i in individual[slice_] if i.arity == 0]
    left = random.choice(ter)
    hat = random.choice(pset.dispose, p=pset.prob_dispose_list)

    del individual[slice_]
    individual.insert(index, left)
    individual.insert(index, hat)

    return individual,


# @logg
# @checkss
def mutNodeReplacementVerbose(individual, pset, personal_map=False):
    """
    # choice terminals_and_constants verbose
    Replaces a randomly chosen primitive from *individual* by a randomly
    chosen primitive with the same number of arguments from the :attr:`pset`
    attribute of the individual.

    :param individual: The normal or typed tree to be mutated.
    :param pset: SymbolSet
    :param personal_map: bool
    :returns: A tuple of one tree.
    """

    if len(individual) < 4:
        return individual,

    if random.random() <= 0.8:
        index = random.choice(np.arange(1, len(individual), step=2))
    else:
        index = random.choice(np.arange(0, len(individual), step=2))

    node = individual[index]

    if index % 2 == 0:
        for i in pset.dispose:
            assert i.arity == 1
        prims = pset.dispose
        p_d = np.array([pset.prob_dispose[repr(i)] for i in prims], 'float32')
        p_d /= np.sum(p_d)
        a = prims[random.choice(len(prims), p=p_d)]
        individual[index] = a
    else:

        if node.arity == 0:  # Terminal
            if personal_map:
                p_t = pset.premap.get_one_node_value(individual, pset, node=node, site=index)
                if p_t is None:
                    p_t = pset.prob_ter_con_list
            else:
                p_t = pset.prob_ter_con_list
            term = pset.terminals_and_constants[random.choice(len(pset.terminals_and_constants), p=p_t)]
            individual[index] = term
        else:  # Primitive
            prims = [p for p in pset.primitives if p.arity == node.arity]
            p_p = np.array([pset.prob_pri[repr(i)] for i in prims], 'float32')

            p_p /= np.sum(p_p)
            # except:
            a = prims[random.choice(len(prims), p=p_p)]

            individual[index] = a

    return individual,


# @logg
# @checkss
def mutDifferentReplacementVerbose(individual, pset, personal_map=False):
    """
    # choice terminals_and_constants verbose
    Replaces a randomly chosen primitive from *individual* by a randomly
    chosen primitive with the same number of arguments from the :attr:`pset`
    attribute of the individual.
    decrease the probability of same terminals.

    :param individual: The normal or typed tree to be mutated.
    :param pset: SymbolSet
    :param personal_map: bool

    :returns: A tuple of one tree.
    """
    if len(individual) < 4:
        return individual,

    ters = [repr(i) for i in individual.terminals()]
    pset_ters = [repr(i) for i in pset.terminals_and_constants]

    cou = Counter(ters)
    cou_mutil = {i: j for i, j in cou.items() if j >= 2}
    ks = list(cou_mutil.keys())
    nks = list(set(pset_ters) - (set(ks)))

    p_nks = np.array([pset.prob_ter_con[i] for i in nks])
    p_nks /= np.sum(p_nks)

    if cou_mutil:
        indexs = []
        for k, v in cou_mutil.items():
            indi = []
            for i in np.arange(1, len(individual), 2):
                if repr(individual[i]) == k:
                    indi.append(i)
            if indi:
                indexs.append(random.choice(indi))

        if personal_map:
            p_nks_new = pset.premap.get_nodes_value(ind=individual, pset=pset, node=None, site=indexs)
            if p_nks_new is not None:
                nks = list(pset.prob_ter_con.keys())
                p_nks = p_nks_new

        if len(indexs) <= len(nks):
            term = random.choice(nks, len(indexs), replace=False, p=p_nks)
        else:
            term = random.choice(nks, len(indexs), replace=True, p=p_nks)

        term_ters = []
        for name in term:
            for i in pset.terminals_and_constants:
                if repr(i) == name:
                    term_ters.append(i)

        for o, n in zip(indexs, term_ters):
            individual[o] = n

    return individual,


######################################
# select                       #
######################################


def selRandom(individuals, k):
    """Select *k* individuals at random from the input *individuals* with
    replacement. The list returned contains references to the input
    *individuals*.

    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :returns: A list of selected individuals.

    This function uses the :func:`numpy.random.choice` function
    """
    return [individuals[random.choice(len(individuals))] for _ in range(k)]


def selBest(individuals, k, fit_attr="fitness"):
    """Select the *k* best individuals among the input *individuals*. The
    list returned contains references to the input *individuals*.

    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param fit_attr: The attribute of individuals to use as selection criterion
    :returns: A list containing the k best individuals.
    """
    return sorted(individuals, key=attrgetter(fit_attr), reverse=True)[:k]


def selTournament(individuals, k, tournsize, fit_attr="fitness"):
    """Select the best individual among *tournsize* randomly chosen
    individuals, *k* times. The list returned contains
    references to the input *individuals*.

    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param tournsize: The number of individuals participating in each tournament.
    :param fit_attr: The attribute of individuals to use as selection criterion
    :returns: A list of selected individuals.

    This function uses the :func:`numpy.random.choice` function
    """
    chosen = []
    for i in range(k):
        aspirants = selRandom(individuals, tournsize)
        chosen.append(max(aspirants, key=attrgetter(fit_attr)))
    return chosen


def selKbestDim(pop, K_best=10, dim_type=None, fuzzy=False, fit_attr="fitness"):
    """
    select the individual with dim limitation.
    Parameters
    ----------
    pop: SymbolTree
        A list of individuals to select from.
    K_best:int
        The number of individuals to select.
    dim_type:Dim
    fuzzy:bool
        the dim or the dim with same base. such as m,m^2,m^3
    fit_attr:str
        The attribute of individuals to use as selection criterion
    Returns
    -------
    A list of selected individuals.
    """
    chosen = sorted(pop, key=operator.attrgetter(fit_attr))
    chosen.reverse()

    if dim_type is None:
        add_ind = chosen
    elif dim_type is 'integer':
        add_ind = [ind for ind in chosen if ind.y_dim.isinteger]
    elif dim_type is 'coef':
        add_ind = [ind for ind in chosen if not ind.y_dim.anyisnan()]
    elif isinstance(dim_type, list):
        add_ind = [ind for ind in chosen if ind.y_dim in dim_type]
    elif isinstance(dim_type, Dim):
        if fuzzy:
            add_ind = [ind for ind in chosen if ind.y_dim.is_same_base(dim_type)]
        else:
            add_ind = [ind for ind in chosen if ind.y_dim == dim_type]
    else:
        raise TypeError("dim_type should be None, 'integer', special Dim or list of Dim")
    if K_best is None:
        if len(add_ind) >= 5:
            K_best = round(len(add_ind) / 10)
        else:
            K_best = 0
    if len(add_ind) >= round(K_best):
        return add_ind[:round(K_best)]
    else:
        return add_ind


def Statis_func(stats=None):
    if stats is None:
        stats = {"fitness_dim_is_target_max": ("max",), "dim_is_traget": ("sum",)}

    func = {"max": np.max, "mean": np.mean, "min": np.mean, "std": np.std, "sum": np.sum}
    att = {"fitness": lambda ind: ind.fitness.values[0],
           "fitness_dim_is_True_max": lambda ind: ind.fitness.values[0] if ind.y_dim is not dnan else -np.inf,
           "fitness_dim_is_target_max": lambda ind: ind.fitness.values[0] if ind.dim_score else -np.inf,
           "fitness_dim_is_True_min": lambda ind: ind.fitness.values[0] if ind.y_dim is not dnan else np.inf,
           "fitness_dim_is_target_min": lambda ind: ind.fitness.values[0] if ind.dim_score else np.inf,
           "dim_is_True": lambda ind: 1 if ind.y_dim is not dnan else 0,
           "dim_is_traget": lambda ind: 1 if ind.dim_score else 0}

    sa_all = {}

    for a, f in stats.items():
        if a in att:
            a_s = att[a]
        else:
            a_s = a
            a = str(a).split(" ")[1]

        sa = Statistics(a_s)

        for i, fi in enumerate(f):
            assert fi in func
            ff = func[fi]

            sa.register(fi, ff)

        sa_all["Cal_%s" % a] = sa
    stats = MultiStatistics(sa_all)

    return stats


######################################
# shown                      #
######################################

def graph(expr):
    """Construct the graph of a tree expression. The tree expression must be
    valid. It returns in order a node list, an edge list, and a dictionary of
    the per node labels. The node are represented by numbers, the edges are
    tuples connecting two nodes (number), and the labels are values of a
    dictionary for which keys are the node numbers.

    :param expr: A tree expression to convert into a graph.
    :returns: A node list, an edge list, and a dictionary of labels.

    The returned objects can be used directly to populate a
    `pygraphviz <http://networkx.lanl.gov/pygraphviz/>`_ graph::

        import pygraphviz as pgv

        # [...] Execution of code that produce a tree expression

        nodes, edges, labels = graph(expr)

        g = pgv.AGraph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog="dot")

        for i in nodes:
            n = g.get_node(i)
            n.attr["label"] = labels[i]

        g.draw("tree.pdf")

    or a `NetworX <http://networkx.github.com/>`_ graph::

        import matplotlib.pyplot as plt
        import networkx as nx

        # [...] Execution of code that produce a tree expression

        nodes, edges, labels = graph(expr)

        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        pos = nx.graphviz_layout(g, prog="dot")

        nx.draw_networkx_nodes(g, pos)
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos, labels)
        plt.show()


    .. note::

       We encourage you to use `pygraphviz
       <http://networkx.lanl.gov/pygraphviz/>`_ as the nodes might be plotted
       out of order when using `NetworX <http://networkx.github.com/>`_.
    """
    nodes = list(range(len(expr)))
    edges = list()
    labels = dict()

    stack = []
    for i, node in enumerate(expr):
        if stack:
            edges.append((stack[-1][0], i))
            stack[-1][1] -= 1
        labels[i] = repr(node)
        stack.append([i, node.arity])
        while stack and stack[-1][1] == 0:
            stack.pop()

    return nodes, edges, labels


def varAnd(population, toolbox, cxpb, mutpb):
    offspring = copy.deepcopy(population)

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring


def varAndfus(population, toolbox, cxpb, mutpb, fus):
    offspring = copy.deepcopy(population)
    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    mutpb /= len(fus)

    for j in fus:
        for i in range(len(offspring)):
            if random.random() < mutpb:
                offspring[i], = j(individual=offspring[i])
                del offspring[i].fitness.values

    return offspring
