Attribute VB_Name = "c154"
'  Copyright (C) 1995-2009 Adlink Technology INC.
'  All rights reserved.
Option Explicit
'
'  System Section 6.3
Declare Function c154_initial Lib "C154.dll" (CardID_InBit As Integer, ByVal Manual_ID As Integer) As Integer
Declare Function c154_close Lib "C154.dll" () As Integer
Declare Function c154_get_version Lib "C154.dll" (ByVal CardId As Integer, firmware_ver As Integer, driver_ver As Long, dll_ver As Long) As Integer
Declare Function c154_set_security_key Lib "C154.dll" (ByVal CardId As Integer, ByVal old_secu_code As Integer, ByVal new_secu_code As Integer) As Integer
Declare Function c154_check_security_key Lib "C154.dll" (ByVal CardId As Integer, ByVal secu_code As Integer) As Integer
Declare Function c154_reset_security_key Lib "C154.dll" (ByVal CardId As Integer) As Integer
Declare Function c154_config_from_file Lib "C154.dll" () As Integer
'
' Pulse Input/Output Configuration Section 6.4
Declare Function c154_set_pls_outmode Lib "C154.dll" (ByVal AxisNo As Integer, ByVal pls_outmode As Integer) As Integer
Declare Function c154_set_pls_iptmode Lib "C154.dll" (ByVal AxisNo As Integer, ByVal pls_iptmode As Integer, ByVal pls_logic As Integer) As Integer
Declare Function c154_set_feedback_src Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Src As Integer) As Integer
'
' Velocity mode motion Section 6.5
Declare Function c154_tv_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double) As Integer
Declare Function c154_sv_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal SVacc As Double) As Integer
Declare Function c154_sd_stop Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Tdec As Double) As Integer
Declare Function c154_emg_stop Lib "C154.dll" (ByVal AxisNo As Integer) As Integer
Declare Function c154_get_current_speed Lib "C154.dll" (ByVal AxisNo As Integer, speed As Double) As Integer
Declare Function c154_speed_override Lib "C154.dll" (ByVal CAxisNo As Integer, ByVal NewVelPercent As Double, ByVal Time As Double) As Integer
Declare Function c154_set_max_override_speed Lib "C154.dll" (ByVal AxisNo As Integer, ByVal OvrdSpeed As Double, ByVal Enable As Integer) As Integer
'
' Single Axis Position Mode Section 6.6
Declare Function c154_start_tr_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Dist As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Pos As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Dist As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Pos As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_set_move_ratio Lib "C154.dll" (ByVal AxisNo As Integer, ByVal move_ratio As Double) As Integer
'
' Linear Interpolated Motion Section 6.7
'  Two Axes Linear Interpolation function
Declare Function c154_start_tr_move_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal DistX As Double, ByVal DistY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_tr_move_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal DistX As Double, ByVal DistY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_move_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal PosX As Double, ByVal PosY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_move_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal PosX As Double, ByVal PosY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_move_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal DistX As Double, ByVal DistY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sr_move_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal DistX As Double, ByVal DistY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_move_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal PosX As Double, ByVal PosY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_move_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal PosX As Double, ByVal PosY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer

' Any 2 of former or later 4 axes linear interpolation function
Declare Function c154_start_tr_line2 Lib "C154.dll" (AxisArray As Integer, DistArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_line2 Lib "C154.dll" (AxisArray As Integer, PosArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_line2 Lib "C154.dll" (AxisArray As Integer, DistArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_line2 Lib "C154.dll" (AxisArray As Integer, PosArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
'
' Any 3 of former or later 4 axes linear interpolation function
Declare Function c154_start_tr_line3 Lib "C154.dll" (AxisArray As Integer, DistArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_line3 Lib "C154.dll" (AxisArray As Integer, PosArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_line3 Lib "C154.dll" (AxisArray As Integer, DistArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_line3 Lib "C154.dll" (AxisArray As Integer, PosArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
'
' Former or later 4 Axes linear interpolation function
Declare Function c154_start_tr_line4 Lib "C154.dll" (AxisArray As Integer, DistArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_line4 Lib "C154.dll" (AxisArray As Integer, PosArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_line4 Lib "C154.dll" (AxisArray As Integer, DistArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_line4 Lib "C154.dll" (AxisArray As Integer, PosArray As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
' /*
' I16 FNTYPE c154_tv_line2(I16 *AxisArray, F64 StrVel, F64 MaxVel, F64 Tacc);
' I16 FNTYPE c154_sv_line2(I16 *AxisArray,  F64 StrVel, F64 MaxVel, F64 Tacc, F64 SVacc);
' */
'
' Circular Interpolation Motion Section 6.8
'  Two Axes Arc Interpolation function
Declare Function c154_start_tr_arc_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal OffsetCx As Double, ByVal OffsetCy As Double, ByVal OffsetEx As Double, ByVal OffsetEy As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_arc_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal Cx As Double, ByVal Cy As Double, ByVal Ex As Double, ByVal Ey As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_arc_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal OffsetCx As Double, ByVal OffsetCy As Double, ByVal OffsetEx As Double, ByVal OffsetEy As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_arc_xy Lib "C154.dll" (ByVal CardId As Integer, ByVal Cx As Double, ByVal Cy As Double, ByVal Ex As Double, ByVal Ey As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
'
Declare Function c154_start_tr_arc_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal OffsetCx As Double, ByVal OffsetCy As Double, ByVal OffsetEx As Double, ByVal OffsetEy As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_arc_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal Cx As Double, ByVal Cy As Double, ByVal Ex As Double, ByVal Ey As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_arc_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal OffsetCx As Double, ByVal OffsetCy As Double, ByVal OffsetEx As Double, ByVal OffsetEy As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_arc_zu Lib "C154.dll" (ByVal CardId As Integer, ByVal Cx As Double, ByVal Cy As Double, ByVal Ex As Double, ByVal Ey As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
'
Declare Function c154_start_tr_arc2 Lib "C154.dll" (AxisArray As Integer, OffsetCenter As Double, OffsetEnd As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_ta_arc2 Lib "C154.dll" (AxisArray As Integer, CenterPos As Double, EndPos As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Integer
Declare Function c154_start_sr_arc2 Lib "C154.dll" (AxisArray As Integer, OffsetCenter As Double, OffsetEnd As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
Declare Function c154_start_sa_arc2 Lib "C154.dll" (AxisArray As Integer, CenterPos As Double, EndPos As Double, ByVal CW_CCW As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Integer
'
' Home Return Mode Section 6.9
Declare Function c154_set_home_config Lib "C154.dll" (ByVal AxisNo As Integer, ByVal home_mode As Integer, ByVal org_logic As Integer, ByVal ez_logic As Integer, ByVal ez_count As Integer, ByVal erc_out As Integer) As Integer
Declare Function c154_home_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double) As Integer
Declare Function c154_home_search Lib "C154.dll" (ByVal AxisNo As Integer, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal ORGOffset As Double) As Integer
'
' Manual Pulser Motion Section 6.10
Declare Function c154_set_pulser_iptmode Lib "C154.dll" (ByVal AxisNo As Integer, ByVal InputMode As Integer, ByVal Inverse As Integer) As Integer
Declare Function c154_disable_pulser_input Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Disable As Integer) As Integer
Declare Function c154_pulser_vmove Lib "C154.dll" (ByVal AxisNo As Integer, ByVal SpeedLimit As Double) As Integer
Declare Function c154_pulser_pmove Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Dist As Double, ByVal SpeedLimit As Double) As Integer
Declare Function c154_set_pulser_ratio Lib "C154.dll" (ByVal AxisNo As Integer, ByVal DivF As Integer, ByVal MultiF As Integer) As Integer
'
' Motion Status Section 6.11
Declare Function c154_motion_done Lib "C154.dll" (ByVal AxisNo As Integer) As Integer
'
' Motion Interface I/O Section 6.12
Declare Function c154_set_servo Lib "C154.dll" (ByVal AxisNo As Integer, ByVal on_off As Integer) As Integer
Declare Function c154_set_clr_mode Lib "C154.dll" (ByVal AxisNo As Integer, ByVal clr_mode As Integer, ByVal targetCounterInBit As Integer) As Integer
Declare Function c154_set_inp Lib "C154.dll" (ByVal AxisNo As Integer, ByVal inp_enable As Integer, ByVal inp_logic As Integer) As Integer
Declare Function c154_set_alm Lib "C154.dll" (ByVal AxisNo As Integer, ByVal alm_logic As Integer, ByVal alm_mode As Integer) As Integer
Declare Function c154_set_erc Lib "C154.dll" (ByVal AxisNo As Integer, ByVal erc_logic As Integer, ByVal erc_pulse_width As Integer, ByVal erc_mode As Integer) As Integer
Declare Function c154_set_erc_out Lib "C154.dll" (ByVal AxisNo As Integer) As Integer
Declare Function c154_clr_erc Lib "C154.dll" (ByVal AxisNo As Integer) As Integer
Declare Function c154_set_sd Lib "C154.dll" (ByVal AxisNo As Integer, ByVal sd_logic As Integer, ByVal sd_latch As Integer, ByVal sd_mode As Integer) As Integer
Declare Function c154_enable_sd Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Enable As Integer) As Integer
Declare Function c154_set_limit_logic Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Logic As Integer) As Integer
Declare Function c154_set_limit_mode Lib "C154.dll" (ByVal AxisNo As Integer, ByVal limit_mode As Integer) As Integer
Declare Function c154_get_io_status Lib "C154.dll" (ByVal AxisNo As Integer, io_sts As Integer) As Integer
'
' Interrupt Control Section 6.13
Declare Function c154_int_control Lib "C154.dll" (ByVal CardId As Integer, ByVal intFlag As Integer) As Integer
Declare Function c154_wait_error_interrupt Lib "C154.dll" (ByVal AxisNo As Integer, ByVal TimeOut_ms As Long) As Integer
Declare Function c154_wait_motion_interrupt Lib "C154.dll" (ByVal AxisNo As Integer, ByVal IntFactorBitNo As Integer, ByVal TimeOut_ms As Long) As Integer
Declare Function c154_set_motion_int_factor Lib "C154.dll" (ByVal AxisNo As Integer, ByVal int_factor As Long) As Integer
'
' Position Control and Counters Section 6.14
Declare Function c154_get_position Lib "C154.dll" (ByVal AxisNo As Integer, Pos As Double) As Integer
Declare Function c154_set_position Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Pos As Double) As Integer
Declare Function c154_get_command Lib "C154.dll" (ByVal AxisNo As Integer, Cmd As Long) As Integer
Declare Function c154_set_command Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Cmd As Long) As Integer
Declare Function c154_get_error_counter Lib "C154.dll" (ByVal AxisNo As Integer, error As Integer) As Integer
Declare Function c154_reset_error_counter Lib "C154.dll" (ByVal AxisNo As Integer) As Integer
Declare Function c154_set_general_counter Lib "C154.dll" (ByVal AxisNo As Integer, ByVal CntSrc As Integer, ByVal CntValue As Double) As Integer
Declare Function c154_get_general_counter Lib "C154.dll" (ByVal AxisNo As Integer, CntValue As Double) As Integer
'

Declare Function c154_set_latch_source Lib "C154.dll" (ByVal AxisNo As Integer, ByVal LtcSrc As Integer) As Integer
Declare Function c154_set_ltc_logic Lib "C154.dll" (ByVal AxisNo As Integer, ByVal LtcLogic As Integer) As Integer
Declare Function c154_get_latch_data Lib "C154.dll" (ByVal AxisNo As Integer, ByVal CounterNo As Integer, Pos As Double) As Integer

' Continuous Motion Section 6.16
Declare Function c154_set_continuous_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Enable As Integer) As Integer
Declare Function c154_check_continuous_buffer Lib "C154.dll" (ByVal AxisNo As Integer) As Integer
Declare Function c154_dwell_move Lib "C154.dll" (ByVal AxisNo As Integer, ByVal milliSecond As Double) As Integer
'
' Multiple Axes Simultaneous Operation Section 6.17
Declare Function c154_set_tr_move_all Lib "C154.dll" (ByVal TotalAxes As Integer, AxisArray As Integer, DistA As Double, StrVelA As Double, MaxVelA As Double, TaccA As Double, TdecA As Double) As Integer
Declare Function c154_set_sa_move_all Lib "C154.dll" (ByVal TotalAx As Integer, AxisArray As Integer, PosA As Double, StrVelA As Double, MaxVelA As Double, TaccA As Double, TdecA As Double, SVaccA As Double, SVdecA As Double) As Integer
Declare Function c154_set_ta_move_all Lib "C154.dll" (ByVal TotalAx As Integer, AxisArray As Integer, PosA As Double, StrVelA As Double, MaxVelA As Double, TaccA As Double, TdecA As Double) As Integer
Declare Function c154_set_sr_move_all Lib "C154.dll" (ByVal TotalAx As Integer, AxisArray As Integer, DistA As Double, StrVelA As Double, MaxVelA As Double, TaccA As Double, TdecA As Double, SVaccA As Double, SVdecA As Double) As Integer
Declare Function c154_start_move_all Lib "C154.dll" (ByVal FirstAxisNo As Integer) As Integer
Declare Function c154_stop_move_all Lib "C154.dll" (ByVal FirstAxisNo As Integer) As Integer
'
' General-purposed Input/Output Section 6.18
Declare Function c154_set_gpio_output Lib "C154.dll" (ByVal CardId As Integer, ByVal DoValue As Integer) As Integer
Declare Function c154_get_gpio_output Lib "C154.dll" (ByVal CardId As Integer, DoValue As Integer) As Integer
Declare Function c154_get_gpio_input Lib "C154.dll" (ByVal CardId As Integer, DiValue As Integer) As Integer
Declare Function c154_set_gpio_input_function Lib "C154.dll" (ByVal CardId As Integer, ByVal Channel As Integer, ByVal SelectNo As Integer, ByVal Logic As Integer) As Integer
'

Declare Function c154_set_sync_stop_mode Lib "C154.dll"(ByVal AxisNo As Integer,ByVal stop_mode As Integer) As Integer
Declare Function c154_set_sync_option Lib "C154.dll"(ByVal AxisNo As Integer, ByVal sync_stop_on As Integer, ByVal cstop_output_on As Integer, ByVal sync_option1 As Integer, ByVal sync_option2 As Integer)As Integer
Declare Function c154_set_sync_signal_source Lib "C154.dll"(ByVal AxisNo As Integer, ByVal sync_axis As Integer)As Integer
Declare Function c154_set_sync_signal_mode Lib "C154.dll"(ByVal AxisNo As Integer, ByVal mode As Integer)As Integer


' Soft Limit 6.19
Declare Function c154_disable_soft_limit Lib "C154.dll" (ByVal AxisNo As Integer) As Integer
Declare Function c154_enable_soft_limit Lib "C154.dll" (ByVal AxisNo As Integer, ByVal Action As Integer) As Integer
Declare Function c154_set_soft_limit Lib "C154.dll" (ByVal AxisNo As Integer, ByVal PlusLimit As Long, ByVal MinusLimit As Long) As Integer
'
' Backlas Compensation / Vibration Suppression 6.20
Declare Function c154_backlash_comp Lib "C154.dll" (ByVal AxisNo As Integer, ByVal CompPulse As Integer, ByVal Mode As Integer) As Integer
Declare Function c154_suppress_vibration Lib "C154.dll" (ByVal AxisNo As Integer, ByVal ReverseTime As Integer, ByVal ForwardTime As Integer) As Integer
Declare Function c154_set_fa_speed Lib "C154.dll" (ByVal AxisNo As Integer, ByVal FA_Speed As Double) As Integer
'

