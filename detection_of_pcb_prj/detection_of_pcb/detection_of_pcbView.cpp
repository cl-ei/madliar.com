
// detection_of_pcbView.cpp : Cdetection_of_pcbView 类的实现
//

#include "stdafx.h"
// SHARED_HANDLERS 可以在实现预览、缩略图和搜索筛选器句柄的
// ATL 项目中进行定义，并允许与该项目共享文档代码。
#ifndef SHARED_HANDLERS
#include "detection_of_pcb.h"
#endif

#include "detection_of_pcbDoc.h"
#include "detection_of_pcbView.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// Cdetection_of_pcbView

IMPLEMENT_DYNCREATE(Cdetection_of_pcbView, CView)

BEGIN_MESSAGE_MAP(Cdetection_of_pcbView, CView)
	// 标准打印命令
	ON_COMMAND(ID_FILE_PRINT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_DIRECT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_PREVIEW, &Cdetection_of_pcbView::OnFilePrintPreview)
	ON_WM_CONTEXTMENU()
	ON_WM_RBUTTONUP()
END_MESSAGE_MAP()

// Cdetection_of_pcbView 构造/析构

Cdetection_of_pcbView::Cdetection_of_pcbView()
{
	// TODO: 在此处添加构造代码

}

Cdetection_of_pcbView::~Cdetection_of_pcbView()
{
}

BOOL Cdetection_of_pcbView::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: 在此处通过修改
	//  CREATESTRUCT cs 来修改窗口类或样式

	return CView::PreCreateWindow(cs);
}

// Cdetection_of_pcbView 绘制

void Cdetection_of_pcbView::OnDraw(CDC* /*pDC*/)
{
	Cdetection_of_pcbDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	if (!pDoc)
		return;

	// TODO: 在此处为本机数据添加绘制代码
}


// Cdetection_of_pcbView 打印


void Cdetection_of_pcbView::OnFilePrintPreview()
{
#ifndef SHARED_HANDLERS
	AFXPrintPreview(this);
#endif
}

BOOL Cdetection_of_pcbView::OnPreparePrinting(CPrintInfo* pInfo)
{
	// 默认准备
	return DoPreparePrinting(pInfo);
}

void Cdetection_of_pcbView::OnBeginPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: 添加额外的打印前进行的初始化过程
}

void Cdetection_of_pcbView::OnEndPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: 添加打印后进行的清理过程
}

void Cdetection_of_pcbView::OnRButtonUp(UINT /* nFlags */, CPoint point)
{
	ClientToScreen(&point);
	OnContextMenu(this, point);
}

void Cdetection_of_pcbView::OnContextMenu(CWnd* /* pWnd */, CPoint point)
{
#ifndef SHARED_HANDLERS
	theApp.GetContextMenuManager()->ShowPopupMenu(IDR_POPUP_EDIT, point.x, point.y, this, TRUE);
#endif
}


// Cdetection_of_pcbView 诊断

#ifdef _DEBUG
void Cdetection_of_pcbView::AssertValid() const
{
	CView::AssertValid();
}

void Cdetection_of_pcbView::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

Cdetection_of_pcbDoc* Cdetection_of_pcbView::GetDocument() const // 非调试版本是内联的
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(Cdetection_of_pcbDoc)));
	return (Cdetection_of_pcbDoc*)m_pDocument;
}
#endif //_DEBUG


// Cdetection_of_pcbView 消息处理程序
