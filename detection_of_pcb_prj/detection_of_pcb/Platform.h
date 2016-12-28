#pragma once
#include "./Library/Include/C154.h"

enum SportModeType{S_type,T_type};

#define AXIS_0  0
#define AXIS_1  3

class CPlatform
{
public:
	CPlatform(void);
	~CPlatform(void);

	I16 firmware_ver;
	I32 driver_ver;
	I32 dll_ver;	
protected:
	U16 CardID_InBit;
	I16 CardId;
	
	int m_Status;
	//运动模式选择，
	//T: 为恒定加速度运行模式，加速过程线性
	//S: 加速度为二阶速度曲线，可以减小电机震动，但配置较繁琐
	SportModeType m_SportMode;

	F64 m_StartVel;		//起始速度
	F64 m_MaxVel;		//最大速度
	F64 m_Tacc;		//加速时间
	F64 m_Tdec;		//减速时间

	//下面两参数任一为0时，运动曲线为纯S曲线
	F64 m_Sacc;		//S曲线加速阶段速度差值，必须小于 (0.5 * m_MaxVel)					
	F64 m_Sdec;		//S曲线减速阶段速度差值，必须小于 (0.5 * m_MaxVel)

	F64 m_Pos[2];		//当前位置，单位point
	F64 m_DstPos[2];		//目的位置
	F64 m_Border[2];	//轴界限
	F64 m_PosCam[2];	//摄像机位置
	F64 m_SizeCam[2];	//摄像机位置

	F64 m_PPCm;		//每厘米点数。用于设置平台大小

	


	HANDLE ChildThread;

public:
	int InitPlatform(void);

	int set_sport_mode(SportModeType);
	SportModeType get_sport_mode(void);

	int set_speed(F64 spd[]);
	F64 get_speed(int Arg_No);

	F64 get_dstpos(int Arg_No,bool update = true);

	int set_border(F64 b0,F64 b1);
	int move(I16 Axis , F64 distance);
	int move_absolute_xy(F64 pos_x,F64 pos_y);
	int update_pos();
	F64 get_pos(int Arg_No,bool update = true);

	int return_to_org(void);
};

//extern CPlatform Moto;