
// detection_of_pcb.h : detection_of_pcb 应用程序的主头文件
//
#pragma once

#ifndef __AFXWIN_H__
	#error "在包含此文件之前包含“stdafx.h”以生成 PCH 文件"
#endif

#include "resource.h"       // 主符号

#include "Plfcfg.h"
#include "platform.h"

// Cdetection_of_pcbApp:
// 有关此类的实现，请参阅 detection_of_pcb.cpp
//

class Cdetection_of_pcbApp : public CWinAppEx
{
public:
	Cdetection_of_pcbApp();


// 重写
public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();

// 实现
	UINT  m_nAppLook;
	BOOL  m_bHiColorIcons;

	virtual void PreLoadState();
	virtual void LoadCustomState();
	virtual void SaveCustomState();

	afx_msg void OnAppAbout();
	DECLARE_MESSAGE_MAP()
	afx_msg void OnPlfCfg();
	afx_msg void OnCfgPlatform();
};

void ErrMsgBox(char *msg,int error_code);

extern Cdetection_of_pcbApp theApp;
