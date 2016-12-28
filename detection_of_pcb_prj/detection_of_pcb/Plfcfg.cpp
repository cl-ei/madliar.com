// Plfcfg.cpp : 实现文件
//

#include "stdafx.h"
#include "detection_of_pcb.h"
#include "Plfcfg.h"
#include "afxdialogex.h"

//*******************************************************************************//

//debug 函数
void PrintError(int e_code){
	char ErrorMsg[256]="失败！ 错误代码：";
	char buff[256]	;
	itoa(e_code,buff,10); 
	strcat(ErrorMsg,buff);

	CString s_ErrorMsg = CString(ErrorMsg);  
	USES_CONVERSION;  
	LPCWSTR wszEMsg = A2CW(W2A(s_ErrorMsg)); 

	AfxMessageBox(wszEMsg);
}

//*******************************************************************************//


// CPlfcfg 对话框

IMPLEMENT_DYNAMIC(CPlfcfg, CDialogEx)

CPlfcfg::CPlfcfg(CWnd* pParent /* = NULL */)
	: CDialogEx(CPlfcfg::IDD, pParent)
{
}

CPlfcfg::~CPlfcfg()
{
}

void CPlfcfg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CPlfcfg, CDialogEx)
	ON_BN_CLICKED(IDOK, &CPlfcfg::OnBnClickedOk)
	ON_WM_TIMER()
	ON_BN_CLICKED(IDCANCEL, &CPlfcfg::OnBnClickedCancel)
	ON_BN_CLICKED(IDC_BUTTON6, &CPlfcfg::OnBnClickedButton6)
	ON_BN_CLICKED(IDC_BUTTON4, &CPlfcfg::OnBnClickedButton4)
	ON_BN_CLICKED(IDC_BTN_APPLY, &CPlfcfg::OnBnClickedBtnApply)
END_MESSAGE_MAP()


// CPlfcfg 消息处理程序


void CPlfcfg::OnBnClickedOk()
{
	// TODO: 在此添加控件通知处理程序代码
	CDialogEx::OnOK();
}


void CPlfcfg::OnTimer(UINT_PTR nIDEvent)
{
	// TODO: 在此添加消息处理程序代码和/或调用默认值
	//CDialogEx::OnTimer(nIDEvent);

	int ecode = 0;
	static F64 pos[2] = {0,0};

	switch(nIDEvent){

	case 1:		//轴1定时器
		ecode=Moto.update_pos();
		if(ecode!=0){
			KillTimer(1);
			PrintError(ecode);			
		}else{
			SetDlgItemInt(IDC_DSTPOS0,Moto.get_dstpos(0));
			SetDlgItemInt(IDC_DSTPOS1,Moto.get_dstpos(3));

			SetDlgItemInt(IDC_POS0,Moto.get_pos(0));
			SetDlgItemInt(IDC_POS1,Moto.get_pos(1));
		}
		break;
	default:
		break;	
	}
}


BOOL CPlfcfg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// TODO:  在此添加额外的初始化
	
	//显示固件版本等信息
	if (Moto.firmware_ver != 0){
		SetDlgItemInt(IDC_FIRMVER,Moto.firmware_ver);
		SetDlgItemInt(IDC_DIRVER,Moto.driver_ver);
		SetDlgItemInt(IDC_DLLVER,Moto.dll_ver);
	}

	//设置应该勾选的选项
	// T型/S型运动模式
	CButton* pBtn = nullptr;

	if(Moto.get_sport_mode() == S_type){
		pBtn = (CButton*)GetDlgItem(IDC_RADIO1);
		pBtn->SetCheck(1);
	}else{
		pBtn = (CButton*)GetDlgItem(IDC_RADIO2);
		pBtn->SetCheck(1);
	}

	//设置速度和时间
	SetDlgItemInt(IDC_START_SPEED,Moto.get_speed(0));
	SetDlgItemInt(IDC_MAX_SPEED,Moto.get_speed(1));
	SetDlgItemInt(IDC_TACC,Moto.get_speed(2)*1000);
	SetDlgItemInt(IDC_TDEC,Moto.get_speed(3)*1000);

	//设置目的位置
	SetDlgItemInt(IDC_DSTPOS0,Moto.get_dstpos(0));
	SetDlgItemInt(IDC_DSTPOS1,Moto.get_dstpos(1));


	SetDlgItemInt(IDC_POS0,Moto.get_pos(0));
	SetDlgItemInt(IDC_POS1,Moto.get_pos(1));


	//测试轴
	pBtn = (CButton*)GetDlgItem(IDC_CHECK1);
	pBtn->SetCheck(1);

	//旋转方向
	pBtn = (CButton*)GetDlgItem(IDC_RADIO3);
	pBtn->SetCheck(1);

	//默认手动测试距离 ：10000
	SetDlgItemText(IDC_EDIT13,_T("10000"));

	Moto.return_to_org();

	return TRUE;  // return TRUE unless you set the focus to a control
	// 异常: OCX 属性页应返回 FALSE
}


void CPlfcfg::OnBnClickedCancel()
{
	// TODO: 在此添加控件通知处理程序代码
	CDialogEx::OnCancel();
}

//开始转动代码
void CPlfcfg::OnBnClickedButton6()
{
	//读取要测试轴
	CButton* pBtn = (CButton*)GetDlgItem(IDC_CHECK1);
	int Axis0 = pBtn->GetCheck();
	pBtn = (CButton*)GetDlgItem(IDC_CHECK2);
	int Axis1 = pBtn->GetCheck();
	
	//读取距离
	CString distance;
	GetDlgItemText(IDC_EDIT13,distance);
	float dst = _ttof(distance);
	
	//打开电机
	int ecode = 0;
	if(Axis0 == 1){
		ecode = Moto.move(0,dst);
		if( ecode != 0){
			PrintError(ecode);		
		}else{
			SetTimer(1,50,NULL);
		}
	}
	if(Axis1 == 1){
		ecode = Moto.move(3,dst);
		if(ecode !=0){
			PrintError(ecode);
		}else{
			SetTimer(1,50,NULL);
		}
	}
}


//无条件停止电机按钮
void CPlfcfg::OnBnClickedButton4()
{
	int ecode  = 0;
	ecode = c154_emg_stop(0);
	if( ecode !=0){
		PrintError(ecode);
	}	
}

// 应用按钮
void CPlfcfg::OnBnClickedBtnApply()
{
	//检查运动模式
	CButton* pBtn = (CButton*)GetDlgItem(IDC_RADIO1);
	int SportMode = pBtn->GetCheck();
	if(SportMode == 1){
		Moto.set_sport_mode(T_type);
	}else{
		Moto.set_sport_mode(S_type);
	}

	//设置速度
	CString buff;
	F64 speed[4]={0,0,0,0};

	
	GetDlgItemText(IDC_START_SPEED,buff);
	speed[0] = _ttof(buff);

	GetDlgItemText(IDC_MAX_SPEED,buff);
	speed[1] = _ttof(buff);

	GetDlgItemText(IDC_TACC,buff);
	speed[2] = _ttof(buff) / 1000;

	GetDlgItemText(IDC_TDEC,buff);
	speed[3] = _ttof(buff) / 1000;

	Moto.set_speed(speed);
}

