import wx
import wx.xrc
import wx.adv
import wx.grid
import pandas as pd

pd.set_option('display.max_rows', None)
restaurant_data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv', header=0)
restaurant_data['INSPECTION DATE'] = pd.to_datetime(restaurant_data['INSPECTION DATE'])

# These variables will be used globally for accessing data, form values, etc.
data = None
current_query_number = None
current_frame = None


def set_visibility():
    if data is None:
        current_frame.m_button_currentQuery.Hide()
    else:
        current_frame.m_button_currentQuery.Show()

    if current_frame is None:
        return
    elif current_query_number == 0:
        current_frame.m_label_startDate.Show()
        current_frame.m_datePicker_start.Show()
        current_frame.m_label_endDate.Show()
        current_frame.m_datePicker_end.Show()
        current_frame.m_label_keyword.Hide()
        current_frame.m_text_keyword.Hide()
    elif current_query_number == 1 or current_query_number == 3 or current_query_number == 4:
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
        return


def query_0():
    start_date = current_frame.m_datePicker_start.GetValue().FormatDate()
    end_date = current_frame.m_datePicker_end.GetValue().FormatDate()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_data = restaurant_data[
        (restaurant_data['INSPECTION DATE'] >= start_date) & (restaurant_data['INSPECTION DATE'] <= end_date)]
    return filtered_data


def view_current_query(event):
    current_frame.Hide()
    results_frame = ResultsFrame(current_frame)
    results_frame.Show()
    event.Skip()


def change_query_form(event):
    global current_query_number
    current_query_number = current_frame.m_button_currentQuery.GetValue()
    set_visibility()
    event.Skip()


def run_query(event):
    if current_frame.m_choice1.GetSelection() == 0:
        global data
        data = query_0()

    # remove any rows from the view. loop through data and generate row for each.
    print(len(data))

    current_frame.Hide()
    results_frame = ResultsFrame(current_frame)
    results_frame.Show()

    print(data.head())  # Print the first few rows of the DataFrame
    print(data['CAMIS'])  # Print just the 'CAMIS' column

    for index, row in data.iterrows():
        item_index = results_frame.m_listCtrl.InsertItem(index, str(row['CAMIS']))
        results_frame.m_listCtrl.SetItem(item_index, 1, str(row['DBA']))
        results_frame.m_listCtrl.SetItem(item_index, 2, str(row['BORO']))
        results_frame.m_listCtrl.SetItem(item_index, 3, str(row['BUILDING']))
        results_frame.m_listCtrl.SetItem(item_index, 4, str(row['STREET']))
        results_frame.m_listCtrl.SetItem(item_index, 5, str(row['ZIPCODE']))
        results_frame.m_listCtrl.SetItem(item_index, 6, str(row['PHONE']))
        results_frame.m_listCtrl.SetItem(item_index, 7, str(row['CUISINE DESCRIPTION']))
        results_frame.m_listCtrl.SetItem(item_index, 8, str(row['INSPECTION DATE']))
        results_frame.m_listCtrl.SetItem(item_index, 9, str(row['ACTION']))
        results_frame.m_listCtrl.SetItem(item_index, 10, str(row['VIOLATION CODE']))
        results_frame.m_listCtrl.SetItem(item_index, 11, str(row['VIOLATION DESCRIPTION']))
        results_frame.m_listCtrl.SetItem(item_index, 12, str(row['CRITICAL FLAG']))
        results_frame.m_listCtrl.SetItem(item_index, 13, str(row['SCORE']))
        
        if pd.isna(row['GRADE']):
            results_frame.m_listCtrl.SetItem(item_index, 14, '')
        else:
            results_frame.m_listCtrl.SetItem(item_index, 14, str(row['GRADE']))
        if pd.isna(row['GRADE DATE']):
            results_frame.m_listCtrl.SetItem(item_index, 15, '')
        else:
            results_frame.m_listCtrl.SetItem(item_index, 15, str(row['GRADE DATE']))

        results_frame.m_listCtrl.SetItem(item_index, 16, str(row['RECORD DATE']))
        results_frame.m_listCtrl.SetItem(item_index, 17, str(row['INSPECTION TYPE']))

    event.Skip()


def return_to_home_frame(event, results_frame, home_frame):
    results_frame.Close()
    home_frame.Show()
    set_visibility()
    event.Skip()


class HomeFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Project Title Here", pos=wx.DefaultPosition,
                          size=wx.Size(1500, 900),
                          style=wx.CLOSE_BOX | wx.DEFAULT_FRAME_STYLE | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(1500, 900), wx.Size(-1, -1))

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

        default_start_date = wx.DateTime()
        default_start_date.ParseDate("01/01/2017")
        self.m_datePicker_start = wx.adv.DatePickerCtrl(self, wx.ID_ANY, default_start_date, wx.DefaultPosition,
                                                        wx.DefaultSize, wx.adv.DP_DEFAULT)
        bSizer1.Add(self.m_datePicker_start, 0, wx.ALL, 5)

        self.m_label_endDate = wx.StaticText(self, wx.ID_ANY, u"End Date", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_label_endDate.Wrap(-1)
        bSizer1.Add(self.m_label_endDate, 0, wx.ALL, 5)

        default_end_date = wx.DateTime()
        default_end_date.ParseDate("10/01/2017")
        self.m_datePicker_end = wx.adv.DatePickerCtrl(self, wx.ID_ANY, default_end_date, wx.DefaultPosition,
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

        global current_frame
        current_frame = self

        self.m_button_currentQuery.Bind(wx.EVT_BUTTON, view_current_query)
        self.m_choice1.Bind(wx.EVT_CHOICE, change_query_form)
        self.m_button_runQuery.Bind(wx.EVT_BUTTON, run_query)

    def __del__(self):
        pass


class ResultsFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Project Title Here", pos=wx.DefaultPosition,
                          size=wx.Size(1500, 900),
                          style=wx.CLOSE_BOX | wx.DEFAULT_FRAME_STYLE | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(1500, 900), wx.Size(-1, -1))

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_newQuery = wx.Button(self, wx.ID_ANY, u"< New Query", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_button_newQuery, 0, wx.ALL, 5)

        self.m_notebook_results = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel_data = wx.Panel(self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        # Create a wx.ListCtrl to replace the wx.grid.Grid
        self.m_listCtrl = wx.ListCtrl(self.m_panel_data, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                      wx.LC_REPORT | wx.BORDER_NONE)

        # Add columns to the ListCtrl
        self.m_listCtrl.InsertColumn(0, "CAMIS")
        self.m_listCtrl.InsertColumn(1, "DBA")
        self.m_listCtrl.InsertColumn(2, "BORO")
        self.m_listCtrl.InsertColumn(3, "BUILDING")
        self.m_listCtrl.InsertColumn(4, "STREET")
        self.m_listCtrl.InsertColumn(5, "ZIPCODE")
        self.m_listCtrl.InsertColumn(6, "PHONE")
        self.m_listCtrl.InsertColumn(7, "CUISINE DESCRIPTION")
        self.m_listCtrl.InsertColumn(8, "INSPECTION DATE")
        self.m_listCtrl.InsertColumn(9, "ACTION")
        self.m_listCtrl.InsertColumn(10, "VIOLATION CODE")
        self.m_listCtrl.InsertColumn(11, "VIOLATION DESCRIPTION")
        self.m_listCtrl.InsertColumn(12, "CRITICAL FLAG")
        self.m_listCtrl.InsertColumn(13, "SCORE")
        self.m_listCtrl.InsertColumn(14, "GRADE")
        self.m_listCtrl.InsertColumn(15, "GRADE DATE")
        self.m_listCtrl.InsertColumn(16, "RECORD DATE")
        self.m_listCtrl.InsertColumn(17, "INSPECTION TYPE")

        # for i in range(30):
        #    self.m_listCtrl.InsertItem(i, "")  # Insert an empty row

        bSizer3.Add(self.m_listCtrl, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_data.SetSizer(bSizer3)
        self.m_panel_data.Layout()
        bSizer3.Fit(self.m_panel_data)
        self.m_notebook_results.AddPage(self.m_panel_data, u"a page", True)
        self.m_panel_visualization = wx.Panel(self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              wx.TAB_TRAVERSAL)
        self.m_notebook_results.AddPage(self.m_panel_visualization, u"a page", False)

        bSizer6.Add(self.m_notebook_results, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_button_newQuery.Bind(wx.EVT_BUTTON, lambda event: return_to_home_frame(event, self, home_frame))

    def __del__(self):
        pass


if __name__ == "__main__":
    app = wx.App()
    home_frame = HomeFrame(None)
    home_frame.Show()
    set_visibility()
    app.MainLoop()
