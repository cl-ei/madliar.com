// RunDlg.cpp : 实现文件
//

#include "stdafx.h"
#include "detection_of_pcb.h"
#include "RunDlg.h"
#include "afxdialogex.h"


// CRunDlg 对话框

IMPLEMENT_DYNAMIC(CRunDlg, CDialogEx)

CRunDlg::CRunDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(CRunDlg::IDD, pParent)
{	
}

CRunDlg::~CRunDlg()
{
}

void CRunDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BOOL CRunDlg::OnInitDialog(){
	CDialogEx::OnInitDialog();
	/* 额外的初始化 */

	CButton* pBtn = nullptr;
	pBtn = (CButton*)GetDlgItem(IDC_SHAPE_SEL);
	pBtn->SetCheck(1);

	return true;
}


BEGIN_MESSAGE_MAP(CRunDlg, CDialogEx)
	ON_BN_CLICKED(IDCANCEL, &CRunDlg::OnBnClickedCancel)
	ON_BN_CLICKED(IDC_RUN, &CRunDlg::OnBnClickedRun)
	ON_BN_CLICKED(IDC_BUTTON_MOVE, &CRunDlg::OnBnClickedButtonMove)
	ON_BN_CLICKED(IDC_SHAPE_SEL, &CRunDlg::OnBnClickedShapeSel)
END_MESSAGE_MAP()


// CRunDlg 消息处理程序


void CRunDlg::OnBnClickedCancel()
{
	// TODO: 在此添加控件通知处理程序代码
	CDialogEx::OnCancel();
}


void CRunDlg::OnBnClickedRun()
{
	// TODO: 在此添加控件通知处理程序代码
	
	I16 AxisArray[2] = {0, 3};
	F64 PosArray[2] = {1000, 2000};
	int 
	ecode = c154_start_tr_line2(AxisArray,PosArray,
		1000,5000,	0.05,0.05);

	ErrMsgBox("???：",ecode);
}


void CRunDlg::OnBnClickedButtonMove()
{
	// TODO: 在此添加控件通知处理程序代码
	Moto.move_absolute_xy(20000,60000);
}


void CRunDlg::OnBnClickedShapeSel()
{
	// TODO: 在此添加控件通知处理程序代码
}
