import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="HRNS Trackmania Model Tool")

        panel = wx.Panel(self)
        button = wx.Button(panel, label="Click Me!")
        button.Bind(wx.EVT_BUTTON, self.on_button_click)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, 0, wx.CENTER | wx.ALL, 20)
        panel.SetSizer(sizer)

    def on_button_click(self, event):
        print("Button clicked!")

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
