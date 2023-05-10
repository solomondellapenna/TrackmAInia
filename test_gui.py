import pytest
import wx
import gui

frame = None 

# run with command pytest ./test_gui.py -v -s to get setup
def setup_module(self):
    print("Setting up tests")
    self.app = wx.App()
    self.frame = gui.MyFrame()
    self.frame.Show()

# once tests complete
def teardown_module(self):
    self.app.MainLoop()

# Test Button Click
def test_on_model_click():
    # Create "mock" click
    def clickOK():
        clickEvent = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED )
        self.dlg.ProcessEvent(clickEvent)
    wx.CallAfter(clickOK)
    # Function call should succeed
    assert on_test_model_click() == 1 

def test_select_model_in_config():
    # Valid parameter
    assert frame.select_model_in_config("") == 0
    # Test filename
    assert frame.select_model_in_config("SAC_4_LIDAR_elevation_t") == 1


def test_on_model_selection():
    # Create "mock" combo selection
    def boxOK():
        boxEvent = wx.CommandEvent(wx.wxEVT_COMBOBOX)
        self.dlg.ProcessEvent(boxEvent)
        # frame.on_model_selection(boxEvent)
    wx.CallAfter(boxOK)
    assert frame.current_model == "SAC_4_LIDAR_elevation_t"