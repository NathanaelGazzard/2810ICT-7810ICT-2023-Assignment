import wx
import wx.xrc
import wx.adv


class ResultsFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Project Title Here", pos=wx.DefaultPosition,
                          size=wx.Size(1000, 600),
                          style=wx.CLOSE_BOX | wx.DEFAULT_FRAME_STYLE | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(1000, 600), wx.Size(1000, 600))

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_newQuery = wx.Button(self, wx.ID_ANY, u"< New Query", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_button_newQuery, 0, wx.ALL, 5)

        self.m_notebook_results = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel_data = wx.Panel(self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        self.m_notebook_results.AddPage(self.m_panel_data, u"a page", False)
        self.m_panel_visualtization = wx.Panel(self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                               wx.TAB_TRAVERSAL)
        self.m_notebook_results.AddPage(self.m_panel_visualtization, u"a page", True)

        bSizer6.Add(self.m_notebook_results, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button_newQuery.Bind(wx.EVT_BUTTON, self.back_to_query_form)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def back_to_query_form(self, event):
        event.Skip()
