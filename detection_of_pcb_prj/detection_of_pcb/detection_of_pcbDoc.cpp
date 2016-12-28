
// detection_of_pcbDoc.cpp : Cdetection_of_pcbDoc 类的实现
//

#include "stdafx.h"
// SHARED_HANDLERS 可以在实现预览、缩略图和搜索筛选器句柄的
// ATL 项目中进行定义，并允许与该项目共享文档代码。
#ifndef SHARED_HANDLERS
#include "detection_of_pcb.h"
#endif

#include "detection_of_pcbDoc.h"

#include <propkey.h>


#include "RunDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// Cdetection_of_pcbDoc

IMPLEMENT_DYNCREATE(Cdetection_of_pcbDoc, CDocument)

BEGIN_MESSAGE_MAP(Cdetection_of_pcbDoc, CDocument)
	ON_COMMAND(ID_32775, &Cdetection_of_pcbDoc::OnRun)
END_MESSAGE_MAP()


// Cdetection_of_pcbDoc 构造/析构

Cdetection_of_pcbDoc::Cdetection_of_pcbDoc()
{
	// TODO: 在此添加一次性构造代码

}

Cdetection_of_pcbDoc::~Cdetection_of_pcbDoc()
{
}

BOOL Cdetection_of_pcbDoc::OnNewDocument()
{
	if (!CDocument::OnNewDocument())
		return FALSE;

	// TODO: 在此添加重新初始化代码
	// (SDI 文档将重用该文档)

	return TRUE;
}




// Cdetection_of_pcbDoc 序列化

void Cdetection_of_pcbDoc::Serialize(CArchive& ar)
{
	if (ar.IsStoring())
	{
		// TODO: 在此添加存储代码
	}
	else
	{
		// TODO: 在此添加加载代码
	}
}

#ifdef SHARED_HANDLERS

// 缩略图的支持
void Cdetection_of_pcbDoc::OnDrawThumbnail(CDC& dc, LPRECT lprcBounds)
{
	// 修改此代码以绘制文档数据
	dc.FillSolidRect(lprcBounds, RGB(255, 255, 255));

	CString strText = _T("TODO: implement thumbnail drawing here");
	LOGFONT lf;

	CFont* pDefaultGUIFont = CFont::FromHandle((HFONT) GetStockObject(DEFAULT_GUI_FONT));
	pDefaultGUIFont->GetLogFont(&lf);
	lf.lfHeight = 36;

	CFont fontDraw;
	fontDraw.CreateFontIndirect(&lf);

	CFont* pOldFont = dc.SelectObject(&fontDraw);
	dc.DrawText(strText, lprcBounds, DT_CENTER | DT_WORDBREAK);
	dc.SelectObject(pOldFont);
}

// 搜索处理程序的支持
void Cdetection_of_pcbDoc::InitializeSearchContent()
{
	CString strSearchContent;
	// 从文档数据设置搜索内容。
	// 内容部分应由“;”分隔

	// 例如:  strSearchContent = _T("point;rectangle;circle;ole object;")；
	SetSearchContent(strSearchContent);
}

void Cdetection_of_pcbDoc::SetSearchContent(const CString& value)
{
	if (value.IsEmpty())
	{
		RemoveChunk(PKEY_Search_Contents.fmtid, PKEY_Search_Contents.pid);
	}
	else
	{
		CMFCFilterChunkValueImpl *pChunk = NULL;
		ATLTRY(pChunk = new CMFCFilterChunkValueImpl);
		if (pChunk != NULL)
		{
			pChunk->SetTextValue(PKEY_Search_Contents, value, CHUNK_TEXT);
			SetChunkValue(pChunk);
		}
	}
}

#endif // SHARED_HANDLERS

// Cdetection_of_pcbDoc 诊断

#ifdef _DEBUG
void Cdetection_of_pcbDoc::AssertValid() const
{
	CDocument::AssertValid();
}

void Cdetection_of_pcbDoc::Dump(CDumpContext& dc) const
{
	CDocument::Dump(dc);
}
#endif //_DEBUG


// Cdetection_of_pcbDoc 命令


void Cdetection_of_pcbDoc::OnRun()
{
	// TODO: 在此添加命令处理程序代码
	CRunDlg RunDlg;
	RunDlg.DoModal();

}
