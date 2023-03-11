import wx
import os

# Global variables

MODEL_PATH = "../models"
current_model = ""

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="HRNS Trackmania Model Tool")
        panel = wx.Panel(self)

        # Add text describing the dropdown menu
        model_selection_text = wx.StaticText(panel, label="Select a model:")

        # Create a dropdown menu with the available models in the MODEL_PATH
        model_selection_combo_box = wx.ComboBox(panel, choices=os.listdir(MODEL_PATH), style=wx.CB_READONLY)
        model_selection_combo_box.Bind(wx.EVT_COMBOBOX, self.on_model_selection)

        # Get the current model
        current_model = model_selection_combo_box.GetValue()

        # Create a button to train the model
        button = wx.Button(panel, label="Train model")
        button.Bind(wx.EVT_BUTTON, self.on_button_click)

        # Create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(model_selection_text, 0, wx.CENTER | wx.ALL, 20) # Add the model selection text to the sizer
        sizer.Add(button, 0, wx.CENTER | wx.ALL, 20) # Add the button to the sizer
        sizer.Add(model_selection_combo_box, 0, wx.CENTER | wx.ALL, 20) # Add the model selection combo box to the sizer

        panel.SetSizer(sizer)

    def on_button_click(self, event):
        print("Button clicked!")

    def on_model_selection(self, event):
        print("Model selected!")
        current_model = event.GetString()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
