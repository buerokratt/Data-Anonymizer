from tests import LocalTestExecutor, LocalTestDatabase


def test_passing_state():
    executor = LocalTestExecutor(data_src=LocalTestDatabase(), data_dst=LocalTestDatabase())
    executor.start()
    states = set()
    while True:
        var = executor.get_state()
        states.add(var)
        if var == 'Done' or not var:
            break
    assert len(states.difference({'Standby', 'Getting data', 'Preprocessing', 'Transforming', 'Writing results', 'Done'})) == 0
