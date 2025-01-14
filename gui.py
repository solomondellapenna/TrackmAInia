import wx
import os

# Global variables

TMRLDATA_PATH = "Example-TmrlData/" # TODO: Change to actual TmrlData path
current_model = ""


class MyFrame(wx.Frame):
    current_model
    def __init__(self):
        super().__init__(None, title="HRNS Trackmania Model Tool")
        panel = wx.Panel(self)

        # Add text describing the dropdown menu
        model_selection_text = wx.StaticText(panel, label="Select a model:")

        # Create a list of all models without .tmod extension
        model_folderpath = TMRLDATA_PATH + "weights/"
        model_list = [model_filepath[:-5] for model_filepath in os.listdir(model_folderpath)]

        # Create a dropdown menu with the available models in the model_folderpath
        model_selection_combo_box = wx.ComboBox(panel, choices=model_list, style=wx.CB_READONLY)
        model_selection_combo_box.Bind(wx.EVT_COMBOBOX, self.on_model_selection)

        # Get the current model
        current_model = model_selection_combo_box.GetValue()

        # Create a button to train the model
        button = wx.Button(panel, label="Test Model")
        button.Bind(wx.EVT_BUTTON, self.on_test_model_click)

        # Create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(model_selection_text, 0, wx.CENTER | wx.ALL, 5) # Add the model selection text to the sizer
        sizer.Add(model_selection_combo_box, 0, wx.CENTER | wx.ALL, 5) # Add the model selection combo box to the sizer
        sizer.Add(button, 0, wx.CENTER | wx.ALL, 5) # Add the button to the sizer

        panel.SetSizer(sizer)

    # Function that selects the model in the config file
    @classmethod
    def select_model_in_config(self, model_filename):
        if model_filename == "":
            print("select_model_in_config: No file selected")
            return 0

        print("model_filename =", model_filename)    
        config_filepath = TMRLDATA_PATH + "config/config.json"

        # Open file and read in model line
        with open(config_filepath, "r") as f:
            config_content = f.readlines()

        # Write to config file
        config_content[1] = "  \"RUN_NAME\": " + "\"" + model_filename + "\"" + ",\n"

        with open(config_filepath, "w") as f:
            f.writelines(config_content)
        return 1

    # Runs when the user clicks Test Model
    def on_test_model_click(self, event):
        global current_model
        print("Test model button clicked!")
        # Valid filename check
        valid_file = self.select_model_in_config(current_model)
        if valid_file == 0:
            return 0
        
        print("current_model =", current_model)        

        # Start up terminals to run tmrl
        try:
            os.system("python -m tmrl --test")
            return 1
        except:
            print("An error occured when trying to test model")
            return -1


    # Runs when the user selects a model in the dropdown menu
    def on_model_selection(self, event):
         # Update global model
        global current_model
        current_model = event.GetString()
        print("current_model =", current_model)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()