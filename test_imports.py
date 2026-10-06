def test_modules_import():
    from src import data_preparation, regression_models, visualization
    assert data_preparation is not None
    assert regression_models is not None
    assert visualization is not None
