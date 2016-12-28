Option Strict Off
Option Explicit On 




Module C154_Series
    '/****************************************************************************/
    '/*      Function  Declerations                                              */
    '/****************************************************************************/

    ' System##
    Declare Function c154_initial Lib "C154.dll" Alias "c154_initial" (ByRef CardID_InBit As Integer, ByVal Manual_ID As Short) As Short
    Declare Function c154_close Lib "C154.dll" Alias "c154_close" () As Short
    Declare Function c154_get_version Lib "C154.dll" Alias "c154_get_version" (ByVal card_id As Short, ByRef firmware_ver As Short, ByRef driver_ver As Integer, ByRef dll_ver As Integer) As Short
    Declare Function c154_set_security_key Lib "C154.dll" Alias "c154_set_security_key" (ByVal CardId As Short, ByVal old_secu_code As Short, ByVal new_secu_code As Short) As Short
    Declare Function c154_check_security_key Lib "C154.dll" Alias "c154_check_security_key" (ByVal CardId As Short, ByVal secu_code As Short) As Short
    Declare Function c154_reset_security_key Lib "C154.dll" Alias "c154_reset_security_key" (ByVal CardId As Short) As Short
    Declare Function c154_config_from_file Lib "C154.dll" Alias "c154_config_from_file" () As Short
    Declare Function c154_get_CardType Lib "C154.dll" Alias "c154_get_CardType" (ByVal CardId As Short, ByRef Type As Integer) As Short

    'Pulse Input/Output Configuration Section
    Declare Function c154_set_pls_outmode Lib "C154.dll" Alias "c154_set_pls_outmode" (ByVal AxisNo As Short, ByVal pls_outmode As Short) As Short
    Declare Function c154_set_pls_iptmode Lib "C154.dll" Alias "c154_set_pls_iptmode" (ByVal AxisNo As Short, ByVal pls_iptmode As Short, ByVal pls_logic As Short) As Short
    Declare Function c154_set_feedback_src Lib "C154.dll" Alias "c154_set_feedback_src" (ByVal AxisNo As Short, ByVal Src As Short) As Short

    'Velocity mode motion Section
    Declare Function c154_tv_move Lib "C154.dll" Alias "c154_tv_move" (ByVal AxisNo As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double) As Short
    Declare Function c154_sv_move Lib "C154.dll" Alias "c154_sv_move" (ByVal AxisNo As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal SVacc As Double) As Short
    Declare Function c154_sd_stop Lib "C154.dll" Alias "c154_sd_stop" (ByVal AxisNo As Short, ByVal Tdec As Double) As Short
    Declare Function c154_emg_stop Lib "C154.dll" Alias "c154_emg_stop" (ByVal AxisNo As Short) As Short
    Declare Function c154_get_current_speed Lib "C154.dll" Alias "c154_get_current_speed" (ByVal AxisNo As Short, ByRef speed As Double) As Short
    Declare Function c154_speed_override Lib "C154.dll" Alias "c154_speed_override" (ByVal AxisNo As Short, ByVal NewVelPercent As Double, ByVal Time As Double) As Short
    Declare Function c154_set_max_override_speed Lib "C154.dll" Alias "c154_set_max_override_speed" (ByVal AxisNo As Short, ByVal OvrdSpeed As Double, ByVal Enable As Short) As Short

    'Single Axis Position Mode Section
    Declare Function c154_start_tr_move Lib "C154.dll" Alias "c154_start_tr_move" (ByVal AxisNo As Short, ByVal Dist As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_move Lib "C154.dll" Alias "c154_start_ta_move" (ByVal AxisNo As Short, ByVal Pos As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_move Lib "C154.dll" Alias "c154_start_sr_move" (ByVal AxisNo As Short, ByVal Dist As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_move Lib "C154.dll" Alias "c154_start_sa_move" (ByVal AxisNo As Short, ByVal Pos As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_set_move_ratio Lib "C154.dll" Alias "c154_set_move_ratio" (ByVal AxisNo As Short, ByVal move_ratio As Double) As Short

    'Two Axes Linear Interpolation function
    Declare Function c154_start_tr_move_xy Lib "C154.dll" Alias "c154_start_tr_move_xy" (ByVal CardNo As Short, ByVal DistX As Double, ByVal DistY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_tr_move_zu Lib "C154.dll" Alias "c154_start_tr_move_zu" (ByVal CardNo As Short, ByVal DistZ As Double, ByVal DistU As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_move_xy Lib "C154.dll" Alias "c154_start_ta_move_xy" (ByVal CardNo As Short, ByVal PosX As Double, ByVal PosY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_move_zu Lib "C154.dll" Alias "c154_start_ta_move_zu" (ByVal CardNo As Short, ByVal PosZ As Double, ByVal PosU As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_move_xy Lib "C154.dll" Alias "c154_start_sr_move_xy" (ByVal CardNo As Short, ByVal DistX As Double, ByVal DistY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sr_move_zu Lib "C154.dll" Alias "c154_start_sr_move_zu" (ByVal CardNo As Short, ByVal DistZ As Double, ByVal DistU As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_move_xy Lib "C154.dll" Alias "c154_start_sa_move_xy" (ByVal CardNo As Short, ByVal PosX As Double, ByVal PosY As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_move_zu Lib "C154.dll" Alias "c154_start_sa_move_zu" (ByVal CardNo As Short, ByVal PosZ As Double, ByVal PosU As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short

    'Any 2 of former or later 4 axes linear interpolation function
    Declare Function c154_start_tr_line2 Lib "C154.dll" Alias "c154_start_tr_line2" (ByRef AxisArray As sAxisArray4, ByRef DistArray As sDistA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_line2 Lib "C154.dll" Alias "c154_start_ta_line2" (ByRef AxisArray As sAxisArray4, ByRef PosArray As sPosA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_line2 Lib "C154.dll" Alias "c154_start_sr_line2" (ByRef AxisArray As sAxisArray4, ByRef DistArray As sDistA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_line2 Lib "C154.dll" Alias "c154_start_sa_line2" (ByRef AxisArray As sAxisArray4, ByRef PosArray As sPosA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short

    'Any 3 of former or later 4 axes linear interpolation function
    Declare Function c154_start_tr_line3 Lib "C154.dll" Alias "c154_start_tr_line3" (ByRef AxisArray As sAxisArray4, ByRef DistArray As sDistA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_line3 Lib "C154.dll" Alias "c154_start_ta_line3" (ByRef AxisArray As sAxisArray4, ByRef PosArray As sPosA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_line3 Lib "C154.dll" Alias "c154_start_sr_line3" (ByRef AxisArray As sAxisArray4, ByRef DistArray As sDistA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_line3 Lib "C154.dll" Alias "c154_start_sa_line3" (ByRef AxisArray As sAxisArray4, ByRef PosArray As sPosA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short

    'Former or later 4 Axes linear interpolation function
    Declare Function c154_start_tr_line4 Lib "C154.dll" Alias "c154_start_tr_line4" (ByRef AxisArray As sAxisArray4, ByRef DistArray As sDistA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_line4 Lib "C154.dll" Alias "c154_start_ta_line4" (ByRef AxisArray As sAxisArray4, ByRef PosArray As sPosA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_line4 Lib "C154.dll" Alias "c154_start_sr_line4" (ByRef AxisArray As sAxisArray4, ByRef DistArray As sDistA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_line4 Lib "C154.dll" Alias "c154_start_sa_line4" (ByRef AxisArray As sAxisArray4, ByRef PosArray As sPosA4, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short

    'Two Axes Arc Interpolation function
    Declare Function c154_start_tr_arc_xy Lib "C154.dll" Alias "c154_start_tr_arc_xy" (ByVal CardNo As Short, ByVal OffsetCx As Double, ByVal OffsetCy As Double, ByVal OffsetEx As Double, ByVal OffsetEy As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_arc_xy Lib "C154.dll" Alias "c154_start_ta_arc_xy" (ByVal CardNo As Short, ByVal Cx As Double, ByVal Cy As Double, ByVal Ex As Double, ByVal Ey As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_arc_xy Lib "C154.dll" Alias "c154_start_sr_arc_xy" (ByVal CardNo As Short, ByVal OffsetCx As Double, ByVal OffsetCy As Double, ByVal OffsetEx As Double, ByVal OffsetEy As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_arc_xy Lib "C154.dll" Alias "c154_start_sa_arc_xy" (ByVal CardNo As Short, ByVal Cx As Double, ByVal Cy As Double, ByVal Ex As Double, ByVal Ey As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_tr_arc_zu Lib "C154.dll" Alias "c154_start_tr_arc_zu" (ByVal CardNo As Short, ByVal OffsetCz As Double, ByVal OffsetCu As Double, ByVal OffsetEz As Double, ByVal OffsetEu As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_arc_zu Lib "C154.dll" Alias "c154_start_ta_arc_zu" (ByVal CardNo As Short, ByVal Cz As Double, ByVal Cu As Double, ByVal Ez As Double, ByVal Eu As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_arc_zu Lib "C154.dll" Alias "c154_start_sr_arc_zu" (ByVal CardNo As Short, ByVal OffsetCz As Double, ByVal OffsetCu As Double, ByVal OffsetEz As Double, ByVal OffsetEu As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_arc_zu Lib "C154.dll" Alias "c154_start_sa_arc_zu" (ByVal CardNo As Short, ByVal Cz As Double, ByVal Cu As Double, ByVal Ez As Double, ByVal Eu As Double, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short

    Declare Function c154_start_tr_arc2 Lib "C154.dll" Alias "c154_start_tr_arc2" (ByRef AxisArray As sAxisArray4, ByRef OffsetCenter As sArcOffsetCenter, ByRef OffsetEnd As sArcOffsetEnd, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_ta_arc2 Lib "C154.dll" Alias "c154_start_ta_arc2" (ByRef AxisArray As sAxisArray4, ByRef CenterPos As sArcCenter, ByRef EndPos As sArcEnd, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double) As Short
    Declare Function c154_start_sr_arc2 Lib "C154.dll" Alias "c154_start_sr_arc2" (ByRef AxisArray As sAxisArray4, ByRef OffsetCenter As sArcOffsetCenter, ByRef OffsetEnd As sArcOffsetEnd, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short
    Declare Function c154_start_sa_arc2 Lib "C154.dll" Alias "c154_start_sa_arc2" (ByRef AxisArray As sAxisArray4, ByRef CenterPos As sArcCenter, ByRef EndPos As sArcEnd, ByVal CW_CCW As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double) As Short

    'Home Return Mode Section
    Declare Function c154_set_home_config Lib "C154.dll" Alias "c154_set_home_config" (ByVal AxisNo As Short, ByVal home_mode As Short, ByVal org_logic As Short, ByVal ez_logic As Short, ByVal ez_count As Short, ByVal erc_out As Short) As Short
    Declare Function c154_home_move Lib "C154.dll" Alias "c154_home_move" (ByVal AxisNo As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double) As Short
    Declare Function c154_home_search Lib "C154.dll" Alias "c154_home_search" (ByVal AxisNo As Short, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal ORGOffset As Double) As Short

    'Manual Pulser Motion Section
    Declare Function c154_set_pulser_iptmode Lib "C154.dll" Alias "c154_set_pulser_iptmode" (ByVal AxisNo As Short, ByVal InputMode As Short, ByVal Inverse As Short) As Short
    Declare Function c154_disable_pulser_input Lib "C154.dll" Alias "c154_disable_pulser_input" (ByVal AxisNo As Short, ByVal Disable As Integer) As Short
    Declare Function c154_pulser_vmove Lib "C154.dll" Alias "c154_pulser_vmove" (ByVal AxisNo As Short, ByVal SpeedLimit As Double) As Short
    Declare Function c154_pulser_pmove Lib "C154.dll" Alias "c154_pulser_pmove" (ByVal AxisNo As Short, ByVal Dist As Double, ByVal SpeedLimit As Double) As Short
    Declare Function c154_set_pulser_ratio Lib "C154.dll" Alias "c154_set_pulser_ratio" (ByVal AxisNo As Short, ByVal DivF As Short, ByVal MultiF As Short) As Short

    'Motion Status Section
    Declare Function c154_motion_done Lib "C154.dll" Alias "c154_motion_done" (ByVal AxisNo As Short) As Short

    'Motion Interface I/O Section
    Declare Function c154_set_servo Lib "C154.dll" Alias "c154_set_servo" (ByVal AxisNo As Short, ByVal on_off As Short) As Short
    Declare Function c154_set_clr_mode Lib "C154.dll" Alias "c154_set_clr_mode" (ByVal AxisNo As Short, ByVal clr_mode As Short) As Short
    Declare Function c154_set_inp Lib "C154.dll" Alias "c154_set_inp" (ByVal AxisNo As Short, ByVal inp_enable As Short, ByVal inp_logic As Short) As Short
    Declare Function c154_set_alm Lib "C154.dll" Alias "c154_set_alm" (ByVal AxisNo As Short, ByVal alm_logic As Short, ByVal alm_mode As Short) As Short
    Declare Function c154_set_erc Lib "C154.dll" Alias "c154_set_erc" (ByVal AxisNo As Short, ByVal erc_logic As Short, ByVal erc_pulse_width As Short, ByVal erc_mode As Short) As Short
    Declare Function c154_set_erc_out Lib "C154.dll" Alias "c154_set_erc_out" (ByVal AxisNo As Short) As Short
    Declare Function c154_clr_erc Lib "C154.dll" Alias "c154_clr_erc" (ByVal AxisNo As Short) As Short
    Declare Function c154_set_sd Lib "C154.dll" Alias "c154_set_sd" (ByVal AxisNo As Short, ByVal sd_logic As Short, ByVal sd_latch As Short, ByVal sd_mode As Short) As Short
    Declare Function c154_enable_sd Lib "C154.dll" Alias "c154_enable_sd" (ByVal AxisNo As Short, ByVal Enable As Short) As Short
    Declare Function c154_set_limit_logic Lib "C154.dll" Alias "c154_set_limit_logic" (ByVal AxisNo As Short, ByVal Logic As Short) As Short
    Declare Function c154_set_limit_mode Lib "C154.dll" Alias "c154_set_limit_mode" (ByVal AxisNo As Short, ByVal limit_mode As Short) As Short
    Declare Function c154_get_io_status Lib "C154.dll" Alias "c154_get_io_status" (ByVal AxisNo As Short, ByRef io_sts As Integer) As Short

    'Interrupt Control Section
    Declare Function c154_int_control Lib "C154.dll" Alias "c154_int_control" (ByVal card_id As Short, ByVal intFlag As Short) As Short
    Declare Function c154_wait_error_interrupt Lib "C154.dll" Alias "c154_wait_error_interrupt" (ByVal AxisNo As Short, ByVal TimeOut_ms As Integer) As Short
    Declare Function c154_wait_motion_interrupt Lib "C154.dll" Alias "c154_wait_motion_interrupt" (ByVal AxisNo As Short, ByVal IntFactorBitNo As Short, ByVal TimeOut_ms As Integer) As Short
    Declare Function c154_set_motion_int_factor Lib "C154.dll" Alias "c154_set_motion_int_factor" (ByVal AxisNo As Short, ByVal int_factor As Integer) As Short

    'Position Control and Counters Section
    Declare Function c154_get_position Lib "C154.dll" Alias "c154_get_position" (ByVal AxisNo As Short, ByRef Pos As Double) As Short
    Declare Function c154_set_position Lib "C154.dll" Alias "c154_set_position" (ByVal AxisNo As Short, ByVal Pos As Double) As Short
    Declare Function c154_get_command Lib "C154.dll" Alias "c154_get_command" (ByVal AxisNo As Short, ByRef Cmd As Integer) As Short
    Declare Function c154_set_command Lib "C154.dll" Alias "c154_set_command" (ByVal AxisNo As Short, ByVal Cmd As Integer) As Short
    Declare Function c154_get_error_counter Lib "C154.dll" Alias "c154_get_error_counter" (ByVal AxisNo As Short, ByRef Error_Count As Short) As Short
    Declare Function c154_reset_error_counter Lib "C154.dll" Alias "c154_reset_error_counter" (ByVal AxisNo As Short) As Short
    Declare Function c154_set_general_counter Lib "C154.dll" Alias "c154_set_general_counter" (ByVal AxisNo As Short, ByVal CntSrc As Short, ByVal CntValue As Double) As Short
    Declare Function c154_get_general_counter Lib "C154.dll" Alias "c154_get_general_counter" (ByVal AxisNo As Short, ByRef Pos As Double) As Short

    'Continuous Motion Section
    Declare Function c154_set_continuous_move Lib "C154.dll" Alias "c154_set_continuous_move" (ByVal AxisNo As Short, ByVal conti_logic As Short) As Short
    Declare Function c154_check_continuous_buffer Lib "C154.dll" Alias "c154_check_continuous_buffer" (ByVal AxisNo As Short) As Short
    Declare Function c154_dwell_move Lib "C154.dll" Alias "c154_dwell_move" (ByVal AxisNo As Short, ByVal miniSecond As Double) As Short

    'Multiple Axes Simultaneous Operation Section
    Declare Function c154_set_tr_move_all Lib "C154.dll" Alias "c154_set_tr_move_all" (ByVal TotalAxes As Short, ByRef AxisArray As sAxisArray4, ByRef DistA As sDistA4, ByRef StrVelA As sStrVelA4, ByRef MaxVelA As sMaxVelA4, ByRef TaccA As sTaccA4, ByRef TdecA As sTdecA4) As Short
    Declare Function c154_set_sa_move_all Lib "C154.dll" Alias "c154_set_sa_move_all" (ByVal TotalAxes As Short, ByRef AxisArray As sAxisArray4, ByRef PosA As sPosA4, ByRef StrVelA As sStrVelA4, ByRef MaxVelA As sStrVelA4, ByRef TaccA As sStrVelA4, ByRef TdecA As sTdecA4, ByRef SVaccA As sSVaccA4, ByRef SVdecA As sSVdecA4) As Short
    Declare Function c154_set_ta_move_all Lib "C154.dll" Alias "c154_set_ta_move_all" (ByVal TotalAxes As Short, ByRef AxisArray As sAxisArray4, ByRef PosA As sPosA4, ByRef StrVelA As sStrVelA4, ByRef MaxVelA As sStrVelA4, ByRef TaccA As sStrVelA4, ByRef TdecA As sTdecA4) As Short
    Declare Function c154_set_sr_move_all Lib "C154.dll" Alias "c154_set_sr_move_all" (ByVal TotalAxes As Short, ByRef AxisArray As sAxisArray4, ByRef DistA As sDistA4, ByRef StrVelA As sStrVelA4, ByRef MaxVelA As sStrVelA4, ByRef TaccA As sStrVelA4, ByRef TdecA As sTdecA4, ByRef SVaccA As sSVaccA4, ByRef SVdecA As sSVdecA4) As Short
    Declare Function c154_start_move_all Lib "C154.dll" Alias "c154_start_move_all" (ByVal FirstAxisNo As Short) As Short
    Declare Function c154_stop_move_all Lib "C154.dll" Alias "c154_stop_move_all" (ByVal FirstAxisNo As Short) As Short

    'General I/O Function
    Declare Function c154_set_gpio_output Lib "C154.dll" Alias "c154_set_gpio_output" (ByVal card_id As Short, ByVal do_value As Integer) As Short
    Declare Function c154_get_gpio_output Lib "C154.dll" Alias "c154_get_gpio_output" (ByVal card_id As Short, ByRef do_status As Integer) As Short
    Declare Function c154_get_gpio_input Lib "C154.dll" Alias "c154_get_gpio_input" (ByVal card_id As Short, ByRef di_status As Integer) As Short
    Declare Function c154_set_gpio_input_function Lib "C154.dll" Alias "c154_set_gpio_input_function" (ByVal card_id As Short, ByVal channel As Short, ByVal selectNo As Short, ByVal logic As Short) As Short

    'Soft Limit
    Declare Function c154_disable_soft_limit Lib "C154.dll" Alias "c154_disable_soft_limit" (ByVal AxisNo As Short) As Short
    Declare Function c154_enable_soft_limit Lib "C154.dll" Alias "c154_enable_soft_limit" (ByVal AxisNo As Short, ByVal Action As Short) As Short
    Declare Function c154_set_soft_limit Lib "C154.dll" Alias "c154_set_soft_limit" (ByVal AxisNo As Short, ByVal Plus_Limit As Integer, ByVal Neg_Limit As Integer) As Short

    'Backlas Compensation / Vibration Suppression
    Declare Function c154_backlash_comp Lib "C154.dll" Alias "c154_backlash_comp" (ByVal AxisNo As Short, ByVal CompPulse As Short, ByVal Mode As Short) As Short
    Declare Function c154_suppress_vibration Lib "C154.dll" Alias "c154_suppress_vibration" (ByVal AxisNo As Short, ByVal ReverseTime As Integer, ByVal ForwardTime As Integer) As Short
    Declare Function c154_set_fa_speed Lib "C154.dll" Alias "c154_set_fa_speed" (ByVal AxisNo As Short, ByVal FA_Speed As Double) As Short

    ' Hardware Access Function
    Declare Function c154_read_reg Lib "C154.dll" Alias "c154_read_reg" (ByVal card_id As Short, ByVal Offset As Integer, ByRef Value As Integer) As Short
    Declare Function c154_write_reg Lib "C154.dll" Alias "c154_write_reg" (ByVal card_id As Short, ByVal Offset As Integer, ByVal Value As Integer) As Short
    Declare Function c154_read_reg2 Lib "C154.dll" Alias "c154_read_reg2" (ByVal card_id As Short, ByVal Offset As Integer, ByRef Value As Integer) As Short
    Declare Function c154_write_reg2 Lib "C154.dll" Alias "c154_write_reg2" (ByVal card_id As Short, ByVal Offset As Integer, ByVal Value As Integer) As Short

    'reserve function
    Declare Function c154_get_target_pos Lib "C154.dll" Alias "i_get_target_pos" (ByVal AxisNo As Short, ByRef Value As Integer) As Short
    Declare Function c154_reset_target_pos Lib "C154.dll" Alias "i_reset_target_pos" (ByVal AxisNo As Short, ByVal Value As Integer) As Short

    Declare Function c154_get_tr_move_profile Lib "C154.dll" Alias "i_get_tr_move_profile" (ByVal AxisNo As Short, ByVal Dist As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByRef pStrVel As Double, ByRef pMaxVel As Double, ByRef pTacc As Double, ByRef pTdec As Double, ByRef pTconst As Double) As Short
    Declare Function c154_get_ta_move_profile Lib "C154.dll" Alias "i_get_ta_move_profile" (ByVal AxisNo As Short, ByVal Pos As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByRef pStrVel As Double, ByRef pMaxVel As Double, ByRef pTacc As Double, ByRef pTdec As Double, ByRef pTconst As Double) As Short
    Declare Function c154_get_sr_move_profile Lib "C154.dll" Alias "i_get_sr_move_profile" (ByVal AxisNo As Short, ByVal Dist As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double, ByRef pStrVel As Double, ByRef pMaxVel As Double, ByRef pTacc As Double, ByRef pTdec As Double, ByRef pSVacc As Double, ByRef pSVdec As Double, ByRef pTconst As Double) As Short
    Declare Function c154_get_sa_move_profile Lib "C154.dll" Alias "i_get_sa_move_profile" (ByVal AxisNo As Short, ByVal Pos As Double, ByVal StrVel As Double, ByVal MaxVel As Double, ByVal Tacc As Double, ByVal Tdec As Double, ByVal SVacc As Double, ByVal SVdec As Double, ByRef pStrVel As Double, ByRef pMaxVel As Double, ByRef pTacc As Double, ByRef pTdec As Double, ByRef pSVacc As Double, ByRef pSVdec As Double, ByRef pTconst As Double) As Short



End Module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Public Structure sAxisArray154
    Dim AxisArray1 As Short
    Dim AxisArray2 As Short
    Dim AxisArray3 As Short
    Dim AxisArray4 As Short
End Structure

Public Structure sDistA154
    Dim DistA1 As Double
    Dim DistA2 As Double
    Dim DistA3 As Double
    Dim DistA4 As Double
End Structure

Public Structure sStrVelA154
    Dim StrVelA1 As Double
    Dim StrVelA2 As Double
    Dim StrVelA3 As Double
    Dim StrVelA4 As Double
End Structure

Public Structure sMaxVelA154
    Dim MaxVelA1 As Double
    Dim MaxVelA2 As Double
    Dim MaxVelA3 As Double
    Dim MaxVelA4 As Double
End Structure

Public Structure sTaccA154
    Dim TaccA1 As Double
    Dim TaccA2 As Double
    Dim TaccA3 As Double
    Dim TaccA4 As Double
End Structure

Public Structure sTdecA154
    Dim TdecA1 As Double
    Dim TdecA2 As Double
    Dim TdecA3 As Double
    Dim TdecA4 As Double
End Structure

Public Structure sPosA154
    Dim PosA1 As Double
    Dim PosA2 As Double
    Dim PosA3 As Double
    Dim PosA4 As Double
End Structure

Public Structure sSVaccA154
    Dim SVaccA1 As Double
    Dim SVaccA2 As Double
    Dim SVaccA3 As Double
    Dim SVaccA4 As Double
End Structure

Public Structure sSVdecA154
    Dim SVdecA1 As Double
    Dim SVdecA2 As Double
    Dim SVdecA3 As Double
    Dim SVdecA4 As Double
End Structure

Public Structure sArcCenter
    Dim ArcCenterX As Double
    Dim ArcCenterY As Double
End Structure

Public Structure sArcEnd
    Dim ArcEndX As Double
    Dim ArcEndY As Double
End Structure

Public Structure sArcOffsetCenter
    Dim ArcCenterX As Double
    Dim ArcCenterY As Double
End Structure

Public Structure sArcOffsetEnd
    Dim ArcEndX As Double
    Dim ArcEndY As Double
End Structure

