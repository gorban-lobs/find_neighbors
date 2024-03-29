import pytest
import numpy as np

from find_neighbors.search_logic import NeighborIndex


@pytest.fixture(scope='function')
def setup_index_f():
    users = ((i, 'u' + str(i),
              i * 10, i * 10)
             for i in range(10))
    return NeighborIndex(users)


@pytest.fixture(scope='module')
def setup_index_m():
    users = ((i, 'u' + str(i),
              i * 10, i * 10)
             for i in range(10))
    return NeighborIndex(users)


@pytest.fixture(
    scope='function',
    params=[
        ((0, 10), 10),
        ((3, 5), 2),
        ((6, 6), 0)])
def param_init_ni(request):
    users = [[i, 'u' + str(i),
              i * 10, i * 10]
             for i in range(10)]
    beg, end = request.param[0]
    return (users[beg:end], request.param[1])


def test_init_ni(param_init_ni):
    users, res = param_init_ni
    assert len(NeighborIndex(users).get_ids_list()) == res


@pytest.fixture(
    scope='function',
    params=[
        ((0, 0), 22),
        ((0, 0), 23),
        ((0, 0), 30)])
def param_add_items(request):
    return request.param


def test_add_items(setup_index_f, param_add_items):
    coord, label = param_add_items
    setup_index_f.add_items([coord], [label])
    assert label in setup_index_f.get_ids_list()


@pytest.fixture(
    scope='function',
    params=[
        ((10.0, 11.0, 120, 1), [1]),
        ((20.0, 21.0, 3000, 3), [2, 3, 1]),
        ((20.0, 21.0, 10000, 3), [2, 3, 1]),
        ((30.0, 30.0, 300, 4), [3]),
        ((-35.0, -35.0, 1000, 4), [])])
def param_search_neighbors(request):
    return request.param


def test_search_neighbors(setup_index_m, param_search_neighbors):
    params, res = param_search_neighbors
    assert setup_index_m.search_neighbors(*params).tolist() == res


@pytest.fixture(
    scope='function',
    params=[
        ((0, 0), (6371, 0, 0)),
        ((90, 0), (0, 6371, 0)),
        ((90, 90), (0, 0, 6371)),
        ((-123, 90), (0, 0, 6371))])
def param_circle_to_3d_coords(request):
    return (np.array(request.param[0]), np.array(request.param[1]))


def test_circle_to_3d_coords(setup_index_m, param_circle_to_3d_coords):
    inp, res = param_circle_to_3d_coords
    eps = 0.1
    assert np.abs(sum(setup_index_m.circle_to_3d_coords(inp) - res)) < eps


@pytest.fixture(
    scope='function',
    params=[
        (7756.84, 8339.62),
        (111.19, 111.19),
        (9009.95, 10007.54),
        (555.80, 555.97),
        (8018.80, 8673.20)])
def param_chord_to_circle_dist(request):
    return request.param


def test_chord_to_circle_dist(setup_index_m, param_chord_to_circle_dist):
    inp, res = param_chord_to_circle_dist
    eps = 0.1
    assert np.abs(setup_index_m.chord_to_circle_dist(inp) - res) < eps
