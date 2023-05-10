import pytest
import gui

# def test_on_model_click():
#     assert on_test_model_click() == 0 

def test_select_model_in_config():
    # Valid parameter
    assert gui.MyFrame.select_model_in_config("") == 0

# def test_on_model_selection():
#     assert 0 