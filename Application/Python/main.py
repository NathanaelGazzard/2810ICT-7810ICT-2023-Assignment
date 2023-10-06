import wx
import wx.xrc
import wx.adv

def view_current_query(event, current_frame):
    current_frame.Hide()
    results_frame = ResultsFrame(current_frame)
    results_frame.Show()
    event.Skip()

def change_query_form(event, current_frame, selected_option_index):
    if selected_option_index == 0:
        current_frame.m_label_startDate.Show()
        current_frame.m_datePicker_start.Show()
        current_frame.m_label_endDate.Show()
        current_frame.m_datePicker_end.Show()
        current_frame.m_label_keyword.Hide()
        current_frame.m_text_keyword.Hide()
    elif selected_option_index == 1 or selected_option_index == 3 or selected_option_index == 4:
        current_frame.m_label_startDate.Hide()
        current_frame.m_datePicker_start.Hide()
        current_frame.m_label_endDate.Hide()
        current_frame.m_datePicker_end.Hide()
        current_frame.m_label_keyword.Hide()
        current_frame.m_text_keyword.Hide()
    else:
        current_frame.m_label_startDate.Show()
        current_frame.m_datePicker_start.Show()
        current_frame.m_label_endDate.Show()
        current_frame.m_datePicker_end.Show()
        current_frame.m_label_keyword.Show()
        current_frame.m_text_keyword.Show()

    event.Skip()

def run_query(event):
    print("run query")
    event.Skip()

def return_to_home_frame(event, results_frame, home_frame):
    results_frame.Close()
    home_frame.Show()
    event.Skip()

class HomeFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Project Title Here", pos=wx.DefaultPosition,
                          size=wx.Size(1000, 600),
                          style=wx.CLOSE_BOX | wx.DEFAULT_FRAME_STYLE | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(1000, 600), wx.Size(1000, 600))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_currentQuery = wx.Button(self, wx.ID_ANY, u"Current Query >", wx.DefaultPosition, wx.DefaultSize,
                                               0)
        bSizer1.Add(self.m_button_currentQuery, 0, wx.ALL, 5)

        m_choice1Choices = [u"Inspection Details for Specified Period", u"Violations Distributed by Suburb",
                            u"Violation Keyword Search for Specified Period", u"Animal Violations by Suburb Over Time",
                            u"100 Most Improved by Boro Over Last Year"]
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        bSizer1.Add(self.m_choice1, 0, wx.ALL, 5)

        self.m_label_startDate = wx.StaticText(self, wx.ID_ANY, u"Start Date", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_label_startDate.Wrap(-1)
        bSizer1.Add(self.m_label_startDate, 0, wx.ALL, 5)

        self.m_datePicker_start = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition,
                                                        wx.DefaultSize, wx.adv.DP_DEFAULT)
        bSizer1.Add(self.m_datePicker_start, 0, wx.ALL, 5)

        self.m_label_endDate = wx.StaticText(self, wx.ID_ANY, u"End Date", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_label_endDate.Wrap(-1)
        bSizer1.Add(self.m_label_endDate, 0, wx.ALL, 5)

        self.m_datePicker_end = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition,
                                                      wx.DefaultSize, wx.adv.DP_DEFAULT)
        bSizer1.Add(self.m_datePicker_end, 0, wx.ALL, 5)

        self.m_label_keyword = wx.StaticText(self, wx.ID_ANY, u"Keyword", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_label_keyword.Wrap(-1)
        bSizer1.Add(self.m_label_keyword, 0, wx.ALL, 5)

        self.m_text_keyword = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_text_keyword, 0, wx.ALL, 5)

        self.m_button_runQuery = wx.Button(self, wx.ID_ANY, u"Run Query", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button_runQuery, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button_currentQuery.Bind(wx.EVT_BUTTON, lambda event: view_current_query(event, self))
        self.m_choice1.Bind(wx.EVT_CHOICE, lambda event: change_query_form(event, self, self.m_choice1.GetSelection()))
        self.m_button_runQuery.Bind(wx.EVT_BUTTON, run_query)

    def __del__(self):
        pass

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
        self.m_panel_visualization = wx.Panel(self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                               wx.TAB_TRAVERSAL)
        self.m_notebook_results.AddPage(self.m_panel_visualization, u"a page", True)

        bSizer6.Add(self.m_notebook_results, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button_newQuery.Bind(wx.EVT_BUTTON, lambda event: return_to_home_frame(event, self, home_frame))

    def __del__(self):
        pass

if __name__ == "__main__":
    app = wx.App()
    home_frame = HomeFrame(None)  # Create an instance of HomeFrame
    home_frame.Show()
    app.MainLoop()
