
#ifndef _MPc154_H
#define _MPc154_H

#define _MYWIN32

#include "./Library/Include/type_def.h"

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _MYWIN32
#define FNTYPE PASCAL
#endif

// System Section 6.3
I16 FNTYPE c154_initial(U16 *CardID_InBit, I16 Manual_ID);
I16 FNTYPE c154_close(void);
I16 FNTYPE c154_get_version(I16 card_id, I16 *firmware_ver, I32 *driver_ver, I32 *dll_ver);
I16 FNTYPE c154_get_PCB_version( I16 card_id, U32 *PCB_ver );
I16 FNTYPE c154_set_security_key(I16 CardId, I16 old_secu_code, I16 new_secu_code);
I16 FNTYPE c154_check_security_key(I16 CardId, I16 secu_code);
I16 FNTYPE c154_reset_security_key(I16 CardId);
I16 FNTYPE c154_config_from_file();

//Pulse Input/Output Configuration Section 6.4
I16 FNTYPE c154_set_pls_outmode(I16 AxisNo, I16 pls_outmode);
I16 FNTYPE c154_set_pls_iptmode(I16 AxisNo, I16 pls_iptmode, I16 pls_logic);
I16 FNTYPE c154_set_feedback_src(I16 AxisNo, I16 Src);

//Velocity mode motion Section 6.5
I16 FNTYPE c154_tv_move(I16 AxisNo, F64 StrVel, F64 MaxVel, F64 Tacc);
I16 FNTYPE c154_sv_move(I16 AxisNo, F64 StrVel, F64 MaxVel, F64 Tacc, F64 SVacc);
I16 FNTYPE c154_sd_stop(I16 AxisNo, F64 Tdec);
I16 FNTYPE c154_emg_stop(I16 AxisNo);
I16 FNTYPE c154_get_current_speed(I16 AxisNo, F64 *speed);
I16 FNTYPE c154_speed_override(I16 CAxisNo, F64 NewVelPercent, F64 Time);
//I16 FNTYPE c154_speed_override2(I16 CAxisNo, F64 NewVel, F64 Time);
I16 FNTYPE c154_set_max_override_speed(I16 AxisNo, F64 OvrdSpeed, I16 Enable);

//Single Axis Position Mode Section 6.6
I16 FNTYPE c154_start_tr_move(I16 AxisNo, F64 Dist, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_ta_move(I16 AxisNo, F64 Pos, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_sr_move(I16 AxisNo, F64 Dist, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);
I16 FNTYPE c154_start_sa_move(I16 AxisNo, F64 Pos, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);
I16 FNTYPE c154_set_move_ratio(I16 AxisNo, F64 move_ratio);
//I16 FNTYPE c154_position_override(I16 AxisNo, F64 NewPos);

//Linear Interpolated Motion Section 6.7
  // Two Axes Linear Interpolation function
I16 FNTYPE c154_start_tr_move_xy(I16 CardId, F64 DistX, F64 DistY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_tr_move_zu(I16 CardId, F64 DistX, F64 DistY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);

I16 FNTYPE c154_start_ta_move_xy(I16 CardId, F64 PosX, F64 PosY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_ta_move_zu(I16 CardId, F64 PosX, F64 PosY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);

I16 FNTYPE c154_start_sr_move_xy(I16 CardId, F64 DistX, F64 DistY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);
I16 FNTYPE c154_start_sr_move_zu(I16 CardId, F64 DistX, F64 DistY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);

I16 FNTYPE c154_start_sa_move_xy(I16 CardId, F64 PosX, F64 PosY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);
I16 FNTYPE c154_start_sa_move_zu(I16 CardId, F64 PosX, F64 PosY, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);

//Any 2 of former or later 4 axes linear interpolation function
I16 FNTYPE c154_start_tr_line2(I16 *AxisArray, F64 *DistArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_ta_line2(I16 *AxisArray, F64 *PosArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_sr_line2(I16 *AxisArray, F64 *DistArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);
I16 FNTYPE c154_start_sa_line2(I16 *AxisArray, F64 *PosArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);

//Any 3 of former or later 4 axes linear interpolation function
I16 FNTYPE c154_start_tr_line3(I16 *AxisArray, F64 *DistArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_ta_line3(I16 *AxisArray, F64 *PosArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_sr_line3(I16 *AxisArray, F64 *DistArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);
I16 FNTYPE c154_start_sa_line3(I16 *AxisArray, F64 *PosArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);

//Former or later 4 Axes linear interpolation function
I16 FNTYPE c154_start_tr_line4(I16 *AxisArray, F64 *DistArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_ta_line4(I16 *AxisArray, F64 *PosArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec);
I16 FNTYPE c154_start_sr_line4(I16 *AxisArray, F64 *DistArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);
I16 FNTYPE c154_start_sa_line4(I16 *AxisArray, F64 *PosArray, F64 StrVel, F64 MaxVel, F64 Tacc, F64 Tdec, F64 SVacc, F64 SVdec);

//Circular Interpolation Motion Section 6.8
  // Two Axes Arc Interpolation function
I16 FNTYPE c154_start_tr_arc_xy(I16 CardId, F64 OffsetCx, F64 OffsetCy, F64 OffsetEx, F64 OffsetEy, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec);
I16 FNTYPE c154_start_ta_arc_xy(I16 CardId, F64 Cx, F64 Cy, F64 Ex, F64 Ey, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec);
I16 FNTYPE c154_start_sr_arc_xy(I16 CardId, F64 OffsetCx, F64 OffsetCy, F64 OffsetEx, F64 OffsetEy, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec,F64 SVacc,F64 SVdec);
I16 FNTYPE c154_start_sa_arc_xy(I16 CardId, F64 Cx, F64 Cy, F64 Ex, F64 Ey, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec,F64 SVacc,F64 SVdec);

I16 FNTYPE c154_start_tr_arc_zu(I16 CardId, F64 OffsetCx, F64 OffsetCy, F64 OffsetEx, F64 OffsetEy, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec);
I16 FNTYPE c154_start_ta_arc_zu(I16 CardId, F64 Cx, F64 Cy, F64 Ex, F64 Ey, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec);
I16 FNTYPE c154_start_sr_arc_zu(I16 CardId, F64 OffsetCx, F64 OffsetCy, F64 OffsetEx, F64 OffsetEy, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec,F64 SVacc,F64 SVdec);
I16 FNTYPE c154_start_sa_arc_zu(I16 CardId, F64 Cx, F64 Cy, F64 Ex, F64 Ey, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec,F64 SVacc,F64 SVdec);

I16 FNTYPE c154_start_tr_arc2(I16 *AxisArray, F64 *OffsetCenter, F64 *OffsetEnd, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec);
I16 FNTYPE c154_start_ta_arc2(I16 *AxisArray, F64 *CenterPos, F64 *EndPos, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec);
I16 FNTYPE c154_start_sr_arc2(I16 *AxisArray, F64 *OffsetCenter, F64 *OffsetEnd, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec, F64 SVacc,F64 SVdec);
I16 FNTYPE c154_start_sa_arc2(I16 *AxisArray, F64 *CenterPos, F64 *EndPos, I16 CW_CCW, F64 StrVel,F64 MaxVel,F64 Tacc,F64 Tdec, F64 SVacc,F64 SVdec);

//Home Return Mode Section 6.10
I16 FNTYPE c154_set_home_config(I16 AxisNo, I16 home_mode, I16 org_logic, I16 ez_logic, I16 ez_count, I16 erc_out);
I16 FNTYPE c154_home_move(I16 AxisNo, F64 StrVel, F64 MaxVel, F64 Tacc);
I16 FNTYPE c154_home_search(I16 AxisNo, F64 StrVel, F64 MaxVel, F64 Tacc, F64 ORGOffset);

//Manual Pulser Motion Section 6.11
I16 FNTYPE c154_set_pulser_iptmode(I16 AxisNo, I16 InputMode, I16 Inverse);
I16 FNTYPE c154_disable_pulser_input(I16 AxisNo, U16 Disable );
I16 FNTYPE c154_pulser_vmove(I16 AxisNo, F64 SpeedLimit);
I16 FNTYPE c154_pulser_pmove(I16 AxisNo, F64 Dist, F64 SpeedLimit);
I16 FNTYPE c154_set_pulser_ratio(I16 AxisNo, I16 DivF, I16 MultiF);

//Motion Status Section 6.12
I16 FNTYPE c154_motion_done(I16 AxisNo);

//Motion Interface I/O Section 6.13
I16 FNTYPE c154_set_servo(I16 AxisNo, I16 on_off);
I16 FNTYPE c154_set_clr_mode(I16 AxisNo, I16 clr_mode, I16 targetCounterInBit);
I16 FNTYPE c154_set_inp(I16 AxisNo, I16 inp_enable, I16 inp_logic);
I16 FNTYPE c154_set_alm(I16 AxisNo, I16 alm_logic, I16 alm_mode);
I16 FNTYPE c154_set_erc(I16 AxisNo, I16 erc_logic, I16 erc_pulse_width, I16 erc_mode);
I16 FNTYPE c154_set_erc_out(I16 AxisNo);
I16 FNTYPE c154_clr_erc(I16 AxisNo); 
I16 FNTYPE c154_set_sd(I16 AxisNo, I16 sd_logic, I16 sd_latch, I16 sd_mode);
I16 FNTYPE c154_enable_sd(I16 AxisNo, I16 enable);
I16 FNTYPE c154_set_limit_logic(I16 AxisNo, I16 Logic );
I16 FNTYPE c154_set_limit_mode(I16 AxisNo, I16 limit_mode);
I16 FNTYPE c154_get_io_status(I16 AxisNo, U16 *io_sts);

//Interrupt Control Section 6.14
I16 FNTYPE c154_int_control(I16 CardId, I16 intFlag);
I16 FNTYPE c154_wait_error_interrupt(I16 AxisNo, I32 TimeOut_ms );
I16 FNTYPE c154_wait_motion_interrupt(I16 AxisNo, I16 IntFactorBitNo, I32 TimeOut_ms );
I16 FNTYPE c154_set_motion_int_factor(I16 AxisNo, U32 int_factor );

//Position Control and Counters Section 6.15
I16 FNTYPE c154_get_position(I16 AxisNo, F64 *Pos);
I16 FNTYPE c154_set_position(I16 AxisNo, F64 Pos);
I16 FNTYPE c154_get_command(I16 AxisNo, I32 *Cmd);
I16 FNTYPE c154_set_command(I16 AxisNo, I32 Cmd);
I16 FNTYPE c154_get_error_counter(I16 AxisNo, I16 *error);
I16 FNTYPE c154_reset_error_counter(I16 AxisNo);
I16 FNTYPE c154_set_general_counter(I16 AxisNo, I16 CntSrc, F64 CntValue);
I16 FNTYPE c154_get_general_counter(I16 AxisNo, F64 *CntValue);
I16 FNTYPE c154_get_target_pos(I16 AxisNo, F64 *pos);


//Position Compare and Latch Section 6.16
I16 FNTYPE c154_set_latch_source(I16 AxisNo, I16 LtcSrc);
I16 FNTYPE c154_set_ltc_logic(I16 AxisNo, I16 LtcLogic);
I16 FNTYPE c154_get_latch_data(I16 AxisNo, I16 CounterNo, F64 *Pos);

//Continuous Motion Section 6.17
I16 FNTYPE c154_set_continuous_move(I16 AxisNo, I16 Enable);
I16 FNTYPE c154_check_continuous_buffer(I16 AxisNo);
I16 FNTYPE c154_dwell_move(I16 AxisNo, F64 milliSecond);

//Multiple Axes Simultaneous Operation Section 6.18
I16 FNTYPE c154_set_tr_move_all(I16 TotalAxes, I16 *AxisArray, F64 *DistA, F64 *StrVelA, F64 *MaxVelA, F64 *TaccA, F64 *TdecA);
I16 FNTYPE c154_set_sa_move_all(I16 TotalAx, I16 *AxisArray, F64 *PosA, F64 *StrVelA, F64 *MaxVelA, F64 *TaccA, F64 *TdecA, F64 *SVaccA, F64 *SVdecA);
I16 FNTYPE c154_set_ta_move_all(I16 TotalAx, I16 *AxisArray, F64 *PosA, F64 *StrVelA, F64 *MaxVelA, F64 *TaccA, F64 *TdecA);
I16 FNTYPE c154_set_sr_move_all(I16 TotalAx, I16 *AxisArray, F64 *DistA, F64 *StrVelA, F64 *MaxVelA, F64 *TaccA, F64 *TdecA, F64 *SVaccA, F64 *SVdecA);
I16 FNTYPE c154_start_move_all(I16 FirstAxisNo);
I16 FNTYPE c154_stop_move_all(I16 FirstAxisNo);

I16 FNTYPE c154_set_sync_stop_mode(I16 AxisNo, I16 stop_mode);
I16 FNTYPE c154_set_sync_option(I16 AxisNo, I16 sync_stop_on, I16 cstop_output_on, I16 sync_option1, I16 sync_option2);
I16 FNTYPE c154_set_sync_signal_source(I16 AxisNo, I16 sync_axis);
I16 FNTYPE c154_set_sync_signal_mode(I16 AxisNo, I16 mode);

//General-purposed Input/Output Section 6.19
I16 FNTYPE c154_set_gpio_output(I16 CardId, I16 DoValue );
I16 FNTYPE c154_get_gpio_output(I16 CardId, I16 *DoValue );
I16 FNTYPE c154_get_gpio_input(I16 CardId, I16 *DiValue );

I16 FNTYPE c154_set_gpio_input_function(I16 CardId, I16 Channel, I16 Select, I16 Logic);
I16 FNTYPE c154_set_gpio_output_function(I16 card_id, I16 channel, I16 select);

I16 FNTYPE c154_get_gpio_input_ex(I16 CardId, U16 *Value );
I16 FNTYPE c154_set_gpio_output_ex(I16 CardId, U16 Value );
I16 FNTYPE c154_get_gpio_output_ex(I16 CardId, U16 *Value );

I16 FNTYPE c154_get_gpio_input_ex_CH(I16 CardId, I16 Channel, U16 *Value );
I16 FNTYPE c154_set_gpio_output_ex_CH(I16 CardId, I16 Channel, U16 Value );
I16 FNTYPE c154_get_gpio_output_ex_CH(I16 CardId, I16 Channel, U16 *Value );

I16 FNTYPE c154_set_DI_filter(I16 CardId, I16 Channel, U16 width, U16 enable );
I16 FNTYPE c154_get_DI_filter(I16 CardId, I16 Channel, U16 *width, U16 *enable );

I16 FNTYPE c154_get_CardType(I16 CardId, U16 *Type );

//Soft Limit 6.20
I16 FNTYPE c154_disable_soft_limit(I16 AxisNo);
I16 FNTYPE c154_enable_soft_limit(I16 AxisNo, I16 Action);
I16 FNTYPE c154_set_soft_limit(I16 AxisNo, I32 PlusLimit, I32 MinusLimit);
I16 FNTYPE c154_check_soft_limit(I16 AxisNo, I16 *PlusLimit_sts, I16 *MinusLimit_sts);

//Backlas Compensation / Vibration Suppression 6.21
I16 FNTYPE c154_backlash_comp(I16 AxisNo, I16 CompPulse, I16 Mode);
I16 FNTYPE c154_suppress_vibration(I16 AxisNo, U16 ReverseTime, U16 ForwardTime);
I16 FNTYPE c154_set_fa_speed(I16 AxisNo, F64 FA_Speed);

//Constant synthesized speed control 6.23
//I16 FNTYPE c154_set_axis_option(I16 AxisNo, I16 option);

I16 FNTYPE c154_p_change( I16 AxisNo, F64 Pos );

#ifdef __cplusplus
}
#endif

#endif