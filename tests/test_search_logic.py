import pytest
from find_neighbors.search_logic import NeighborIndex


@pytest.fixture(scope='module')
def setup_index():
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
