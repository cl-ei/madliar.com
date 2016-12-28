#pragma once


// CRunDlg 对话框

class CRunDlg : public CDialogEx
{
	DECLARE_DYNAMIC(CRunDlg)

public:
	CRunDlg(CWnd* pParent = NULL);   // 标准构造函数
	virtual ~CRunDlg();

// 对话框数据
	enum { IDD = IDD_RUNDLG };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

	DECLARE_MESSAGE_MAP()
public:
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedOk();
	afx_msg void OnBnClickedCancel();
	afx_msg void OnBnClickedButton1();
	afx_msg void OnBnClickedRun();
	afx_msg void OnBnClickedButtonMove();
	afx_msg void OnBnClickedShapeSel();
};
