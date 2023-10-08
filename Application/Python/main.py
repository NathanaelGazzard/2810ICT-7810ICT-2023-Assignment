import wx
import wx.xrc
import wx.adv
import wx.grid
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

pd.set_option('display.max_rows', None)
restaurant_data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv', header=0)
restaurant_data['INSPECTION DATE'] = pd.to_datetime(restaurant_data['INSPECTION DATE'])
restaurant_data.fillna('', inplace=True)

data = None
current_query_number = None
current_frame = None
figures = []


def populate_results_data():
    current_frame.Hide()
    results_frame = ResultsFrame(current_frame)
    results_frame.Show()

    row_is_grey = False

    for index, row in data.iterrows():
        if row_is_grey:
            row_is_grey = False
            background_color = wx.Colour(240, 240, 240)
        else:
            row_is_grey = True
            background_color = wx.NullColour

        item_index = results_frame.m_listCtrl.InsertItem(index, str(row['CAMIS']))

        for col_index, column_name in enumerate(data.columns[1:]):
            results_frame.m_listCtrl.SetItem(item_index, col_index, str(row[column_name]))

        item = wx.ListItem()
        item.SetBackgroundColour(background_color)
        item.SetId(item_index)
        results_frame.m_listCtrl.SetItem(item)

    results_frame.display_matplotlib_figures(figures)

    return


def set_visibility():
    if data is None:
        current_frame.m_button_currentQuery.Hide()
    else:
        current_frame.m_button_currentQuery.Show()

    if current_frame is None:
        return

    if current_query_number in [0, 1, 2, 3]:
        current_frame.m_label_startDate.Show()
        current_frame.m_datePicker_start.Show()
        current_frame.m_label_endDate.Show()
        current_frame.m_datePicker_end.Show()
    else:
        current_frame.m_label_startDate.Hide()
        current_frame.m_datePicker_start.Hide()
        current_frame.m_label_endDate.Hide()
        current_frame.m_datePicker_end.Hide()

    if current_query_number == 2:
        current_frame.m_label_keyword.Show()
        current_frame.m_text_keyword.Show()
    else:
        current_frame.m_label_keyword.Hide()
        current_frame.m_text_keyword.Hide()

    return


def query_0():
    start_date = current_frame.m_datePicker_start.GetValue().FormatDate()
    end_date = current_frame.m_datePicker_end.GetValue().FormatDate()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_data = restaurant_data[
        (restaurant_data['INSPECTION DATE'] >= start_date) & (restaurant_data['INSPECTION DATE'] <= end_date)]

    ###################################################### sample figures
    fig1, ax1 = plt.subplots()
    ax1.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
    ax1.set_title('Sample Plot 1')
    figures.append(fig1)

    fig2, ax2 = plt.subplots()
    ax2.scatter([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    ax2.set_title('Sample Plot 2')
    figures.append(fig2)

    #####################################################################

    return filtered_data


def query_1():
    # NOTE: this query assumes that the assignment description meant borough (BORO) when it refers to suburb.
    start_date = current_frame.m_datePicker_start.GetValue().FormatDate()
    end_date = current_frame.m_datePicker_end.GetValue().FormatDate()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_data = restaurant_data[
        (restaurant_data['INSPECTION DATE'] >= start_date) & (restaurant_data['INSPECTION DATE'] <= end_date)]

    filtered_data.sort_values(by='BORO', inplace=True)

    return filtered_data


def query_2(keyword):
    start_date = current_frame.m_datePicker_start.GetValue().FormatDate()
    end_date = current_frame.m_datePicker_end.GetValue().FormatDate()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # NOTE: at present, I'm only checking the 3 fields that I felt were most relevant. We can expand this to search the
    # other fields if needed
    filtered_data = restaurant_data[
        (restaurant_data['INSPECTION DATE'] >= start_date) & (restaurant_data['INSPECTION DATE'] <= end_date) &
        (restaurant_data['DBA'].str.contains(keyword, case=False, na=False) |
         restaurant_data['CUISINE DESCRIPTION'].str.contains(keyword, case=False, na=False) |
         restaurant_data['VIOLATION DESCRIPTION'].str.contains(keyword, case=False, na=False))]

    return filtered_data


def query_3():
    # NOTE: due to the wording of the assignment, this function only checks for rats and mice, as all the other
    # "animals" may be colloquially referred to as bugs. Below is a more extensive list of animals commented-out.
    # This list was obtained by temporarily creating a function that output a list of unique words contained in the
    # 'VIOLATION DESCRIPTION' column, then asking chatGPT to identify all the animals  in the list.

    # animals = ["rats", "mice", "flies", "roaches", "insects", "vermin"]

    animals = ["rats", "mice"]

    start_date = current_frame.m_datePicker_start.GetValue().FormatDate()
    end_date = current_frame.m_datePicker_end.GetValue().FormatDate()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_data = pd.DataFrame()

    for animal in animals:
        animal_data = restaurant_data[
            (restaurant_data['INSPECTION DATE'] >= start_date) & (restaurant_data['INSPECTION DATE'] <= end_date) &
            (restaurant_data['VIOLATION DESCRIPTION'].str.contains(animal, case=False, na=False))]

        filtered_data = pd.concat([filtered_data, animal_data], ignore_index=True)

    return filtered_data


def query_4():
    filtered_data = restaurant_data.dropna(subset=['BORO', 'DBA', 'INSPECTION DATE', 'SCORE'])

    filtered_data['SCORE'] = pd.to_numeric(filtered_data['SCORE'], errors='coerce')

    filtered_data = filtered_data.dropna(subset=['SCORE'])

    filtered_data['INSPECTION DATE'] = pd.to_datetime(filtered_data['INSPECTION DATE'])

    filtered_data['SCORE'] = pd.to_numeric(filtered_data['SCORE'], errors='coerce')

    filtered_data = filtered_data.dropna(subset=['SCORE'])

    filtered_data.sort_values(by=['BORO', 'DBA', 'INSPECTION DATE'], ascending=[True, True, True], inplace=True)

    top_10_results = pd.DataFrame()

    for boro in filtered_data['BORO'].unique():
        boro_data = filtered_data[filtered_data['BORO'] == boro].copy()

        boro_data['SCORE_DIFF'] = boro_data.groupby('DBA')['SCORE'].diff().fillna(0)

        top_10_dba = boro_data.groupby('DBA')['SCORE_DIFF'].sum().nlargest(3).index.tolist()

        top_10_boro_data = boro_data[boro_data['DBA'].isin(top_10_dba)]

        top_10_results = pd.concat([top_10_results, top_10_boro_data])

    print("ATTENTION: query_4 (5th query) is currently set to only display the 3 DBAs with the greatest score increase "
          "per boro, not the hundred most improved. It is unclear to me if a high score is a good or bad thing, though "
          "it seems to be bad. As such, a final number and query name should be decided that suit the scope of the "
          "dataset")
    return top_10_results


def view_current_query(event):
    current_frame.Hide()
    results_frame = ResultsFrame(current_frame)
    results_frame.Show()
    event.Skip()


def change_query_form(event):
    global current_query_number
    current_query_number = current_frame.m_choice1.GetSelection()
    set_visibility()
    event.Skip()


def run_query(event):
    global data

    if current_frame.m_choice1.GetSelection() == 0:
        data = query_0()
    elif current_frame.m_choice1.GetSelection() == 1:
        data = query_1()
    elif current_frame.m_choice1.GetSelection() == 2:
        data = query_2(current_frame.m_text_keyword.GetValue())
    elif current_frame.m_choice1.GetSelection() == 3:
        data = query_3()
    elif current_frame.m_choice1.GetSelection() == 4:
        data = query_4()

    populate_results_data()

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

        self.m_listCtrl = wx.ListCtrl(self.m_panel_data, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                      wx.LC_REPORT | wx.BORDER_NONE)

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

        bSizer3.Add(self.m_listCtrl, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_data.SetSizer(bSizer3)
        self.m_panel_data.Layout()
        bSizer3.Fit(self.m_panel_data)
        self.m_notebook_results.AddPage(self.m_panel_data, u"Query Results Data", True)

        self.m_panel_visualization = wx.ScrolledWindow(self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition,
                                                       wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_visualization.SetScrollRate(10, 10)

        self.m_notebook_results.AddPage(self.m_panel_visualization, u"Query Results Visualization", False)

        bSizer6.Add(self.m_notebook_results, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_button_newQuery.Bind(wx.EVT_BUTTON, lambda event: return_to_home_frame(event, self, home_frame))

    def __del__(self):
        pass

    def display_matplotlib_figures(self, figures):
        sizer = wx.BoxSizer(wx.VERTICAL)

        for figure in figures:
            canvas = FigureCanvas(self.m_panel_visualization, -1, figure)

            sizer.Add(canvas, 1, wx.EXPAND)

        self.m_panel_visualization.SetSizerAndFit(sizer)


if __name__ == "__main__":
    app = wx.App()
    home_frame = HomeFrame(None)
    home_frame.Show()
    current_query_number = 0
    set_visibility()
    app.MainLoop()
