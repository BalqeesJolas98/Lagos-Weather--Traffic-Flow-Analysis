def test_package_imports():
    from src import data_preparation,regression_models,visualization
    assert data_preparation is not None and regression_models is not None and visualization is not None
