///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "noname.h"

///////////////////////////////////////////////////////////////////////////

MyFrame1::MyFrame1( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );

	wxBoxSizer* bSizerMyFrame1;
	bSizerMyFrame1 = new wxBoxSizer( wxVERTICAL );

	wxBoxSizer* bSizerMainFrame;
	bSizerMainFrame = new wxBoxSizer( wxVERTICAL );

	m_panel_QueryPanel = new wxPanel( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	bSizerMainFrame->Add( m_panel_QueryPanel, 1, wxEXPAND | wxALL, 0 );


	bSizerMyFrame1->Add( bSizerMainFrame, 1, wxALL|wxEXPAND, 0 );


	this->SetSizer( bSizerMyFrame1 );
	this->Layout();

	this->Centre( wxBOTH );
}

MyFrame1::~MyFrame1()
{
}
