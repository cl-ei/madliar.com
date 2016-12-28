
// detection_of_pcbView.h : Cdetection_of_pcbView 类的接口
//

#pragma once


class Cdetection_of_pcbView : public CView
{
protected: // 仅从序列化创建
	Cdetection_of_pcbView();
	DECLARE_DYNCREATE(Cdetection_of_pcbView)

// 特性
public:
	Cdetection_of_pcbDoc* GetDocument() const;

// 操作
public:

// 重写
public:
	virtual void OnDraw(CDC* pDC);  // 重写以绘制该视图
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
protected:
	virtual BOOL OnPreparePrinting(CPrintInfo* pInfo);
	virtual void OnBeginPrinting(CDC* pDC, CPrintInfo* pInfo);
	virtual void OnEndPrinting(CDC* pDC, CPrintInfo* pInfo);

// 实现
public:
	virtual ~Cdetection_of_pcbView();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// 生成的消息映射函数
protected:
	afx_msg void OnFilePrintPreview();
	afx_msg void OnRButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnContextMenu(CWnd* pWnd, CPoint point);
	DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG  // detection_of_pcbView.cpp 中的调试版本
inline Cdetection_of_pcbDoc* Cdetection_of_pcbView::GetDocument() const
   { return reinterpret_cast<Cdetection_of_pcbDoc*>(m_pDocument); }
#endif

