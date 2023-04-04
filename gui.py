import wx
import os
import subprocess

# Global variables

# MODEL_PATH = "../models" # TODO: Change to actual model path
TMRLDATA_PATH = "Example-TmrlData/"
current_model = ""
terminals = []

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="HRNS Trackmania Model Tool")
        panel = wx.Panel(self)

        # TODO: Finish model selection menu
        # # Add text describing the dropdown menu
        # model_selection_text = wx.StaticText(panel, label="Select a model:")

        # # Create a dropdown menu with the available models in the MODEL_PATH
        # model_selection_combo_box = wx.ComboBox(panel, choices=os.listdir(MODEL_PATH), style=wx.CB_READONLY)
        # model_selection_combo_box.Bind(wx.EVT_COMBOBOX, self.on_model_selection)

        # # Get the current model
        # current_model = model_selection_combo_box.GetValue()

        # Create a button to train the model
        button = wx.Button(panel, label="Test model")
        button.Bind(wx.EVT_BUTTON, self.on_test_model_click)

        # Create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)

        # sizer.Add(model_selection_text, 0, wx.CENTER | wx.ALL, 5) # Add the model selection text to the sizer
        # sizer.Add(model_selection_combo_box, 0, wx.CENTER | wx.ALL, 5) # Add the model selection combo box to the sizer
        sizer.Add(button, 0, wx.CENTER | wx.ALL, 5) # Add the button to the sizer

        panel.SetSizer(sizer)

    def on_test_model_click(self, event):
        print("Test model button clicked!")

        # Start up terminals to run tmrl
        os.system("python -m tmrl --test")

    def on_model_selection(self, event):
        current_model = event.GetString()
        print("current_model =", current_model)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
