# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from forward_declare import forward_declare
import wx
import wx.xrc
import wx.adv
import wx.grid

###########################################################################
## Class home_frame
###########################################################################

class home_frame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Project Title Here", pos = wx.DefaultPosition, size = wx.Size( 1500,900 ), style = wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 1500,900 ), wx.Size( 1500,900 ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_button_currentQuery = wx.Button( self, wx.ID_ANY, u"Current Query >", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_button_currentQuery, 0, wx.ALL, 5 )

		m_choice1Choices = [ u"Inspection Details for Specified Period", u"Violations Distributed by Suburb", u"Violation Keyword Search for Specified Period", u"Animial Violations by Suburb Over Time", u"100 Most Improved by Boro Over Last Year" ]
		self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
		self.m_choice1.SetSelection( 0 )
		bSizer1.Add( self.m_choice1, 0, wx.ALL, 5 )

		self.m_label_startDate = wx.StaticText( self, wx.ID_ANY, u"Start Date", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_label_startDate.Wrap( -1 )

		bSizer1.Add( self.m_label_startDate, 0, wx.ALL, 5 )

		self.m_datePicker_start = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		bSizer1.Add( self.m_datePicker_start, 0, wx.ALL, 5 )

		self.m_label_endDate = wx.StaticText( self, wx.ID_ANY, u"End Date", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_label_endDate.Wrap( -1 )

		bSizer1.Add( self.m_label_endDate, 0, wx.ALL, 5 )

		self.m_datePicker_end = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		bSizer1.Add( self.m_datePicker_end, 0, wx.ALL, 5 )

		self.m_label_keyword = wx.StaticText( self, wx.ID_ANY, u"Keyword", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_label_keyword.Wrap( -1 )

		bSizer1.Add( self.m_label_keyword, 0, wx.ALL, 5 )

		self.m_text_keyword = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_text_keyword, 0, wx.ALL, 5 )

		self.m_button_runQuery = wx.Button( self, wx.ID_ANY, u"Run Query", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_button_runQuery, 0, wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button_currentQuery.Bind( wx.EVT_BUTTON, self.view_current_query )
		self.m_choice1.Bind( wx.EVT_CHOICE, self.change_query_form )
		self.m_button_runQuery.Bind( wx.EVT_BUTTON, self.run_query )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def view_current_query( self, event ):
		event.Skip()

	def change_query_form( self, event ):
		event.Skip()

	def run_query( self, event ):
		event.Skip()


###########################################################################
## Class results
###########################################################################

class results ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Project Title Here", pos = wx.DefaultPosition, size = wx.Size( 1500,900 ), style = wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 1500,900 ), wx.Size( 1500,900 ) )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_button_newQuery = wx.Button( self, wx.ID_ANY, u"< New Query", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button_newQuery, 0, wx.ALL, 5 )

		self.m_notebook_results = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_data = forward_declare( self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_grid3 = wx.grid.Grid( self.m_panel_data, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_grid3.CreateGrid( 1, 18 )
		self.m_grid3.EnableEditing( True )
		self.m_grid3.EnableGridLines( True )
		self.m_grid3.EnableDragGridSize( False )
		self.m_grid3.SetMargins( 0, 0 )

		# Columns
		self.m_grid3.AutoSizeColumns()
		self.m_grid3.EnableDragColMove( False )
		self.m_grid3.EnableDragColSize( True )
		self.m_grid3.SetColLabelValue( 0, u"CAMIS" )
		self.m_grid3.SetColLabelValue( 1, u"DBA" )
		self.m_grid3.SetColLabelValue( 2, u"BORO" )
		self.m_grid3.SetColLabelValue( 3, u"BUILDING" )
		self.m_grid3.SetColLabelValue( 4, u"STREET" )
		self.m_grid3.SetColLabelValue( 5, u"ZIPCODE" )
		self.m_grid3.SetColLabelValue( 6, u"PHONE" )
		self.m_grid3.SetColLabelValue( 7, u"CUISINE DESCRIPTION" )
		self.m_grid3.SetColLabelValue( 8, u"INSPECTION DATE" )
		self.m_grid3.SetColLabelValue( 9, u"ACTION" )
		self.m_grid3.SetColLabelValue( 10, u"VIOLATION CODE" )
		self.m_grid3.SetColLabelValue( 11, u"VIOLATION DESCRIPTION" )
		self.m_grid3.SetColLabelValue( 12, u"CRITICAL FLAG" )
		self.m_grid3.SetColLabelValue( 13, u"SCORE" )
		self.m_grid3.SetColLabelValue( 14, u"GRADE" )
		self.m_grid3.SetColLabelValue( 15, u"GRADE DATE" )
		self.m_grid3.SetColLabelValue( 16, u"RECORD DATE" )
		self.m_grid3.SetColLabelValue( 17, u"INSPECTION TYPE" )
		self.m_grid3.SetColLabelValue( 18, wx.EmptyString )
		self.m_grid3.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_grid3.EnableDragRowSize( True )
		self.m_grid3.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_grid3.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer3.Add( self.m_grid3, 0, wx.ALL, 5 )


		self.m_panel_data.SetSizer( bSizer3 )
		self.m_panel_data.Layout()
		bSizer3.Fit( self.m_panel_data )
		self.m_notebook_results.AddPage( self.m_panel_data, u"a page", True )
		self.m_panel_visualtization = wx.Panel( self.m_notebook_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook_results.AddPage( self.m_panel_visualtization, u"a page", False )

		bSizer6.Add( self.m_notebook_results, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button_newQuery.Bind( wx.EVT_BUTTON, self.back_to_query_form )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def back_to_query_form( self, event ):
		event.Skip()


