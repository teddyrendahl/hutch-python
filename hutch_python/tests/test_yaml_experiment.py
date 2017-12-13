from hutch_python.yaml_experiment import load_objs


def test_load_experiment():
    info = ['sample_expname']
    objs = load_objs(info)
    assert 'some_plan' in objs
