
unit C154;

interface

//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// System Section 6.3
function  c154_initial( var CardID_InBit :Word;   Manual_ID :Smallint):Smallint;stdcall;
function  c154_close():Smallint;stdcall;
function  c154_get_version(  CardId :Smallint;   var firmware_ver;  var driver_ver :Longint;  var dll_ver :Longint):Smallint;stdcall;
function  c154_set_security_key(  CardId :Smallint;   old_secu_code:Smallint;   new_secu_code:Smallint):Smallint;stdcall;
function  c154_check_security_key(  CardId :Smallint;   secu_code :Smallint):Smallint;stdcall;
function  c154_reset_security_key(  CardId :Smallint):Smallint;stdcall;
function  c154_config_from_file():Smallint;stdcall;

//Pulse Input/Output Configuration Section 6.4
function  c154_set_pls_outmode(  AxisNo:Smallint;   pls_outmode:Smallint):Smallint;stdcall;
function  c154_set_pls_iptmode(  AxisNo:Smallint;   pls_iptmode:Smallint;   pls_logic:Smallint):Smallint;stdcall;
function  c154_set_feedback_src(  AxisNo:Smallint;   Src:Smallint):Smallint;stdcall;

//Velocity mode motion Section 6.5
function  c154_tv_move(  AxisNo:Smallint;  StrVel:Double;  MaxVel:Double;  Tacc:Double):Smallint;stdcall;
function  c154_sv_move(  AxisNo:Smallint;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  SVacc:Double):Smallint;stdcall;
function  c154_sd_stop(  AxisNo:Smallint;  Tdec:Double):Smallint;stdcall;
function  c154_emg_stop(  AxisNo:Smallint):Smallint;stdcall;
function  c154_get_current_speed(  AxisNo:Smallint;  var speed:Double):Smallint;stdcall;
function  c154_speed_override(  CAxisNo:Smallint;  NewVelPercent:Double;  Time:Double):Smallint;stdcall;
function  c154_set_max_override_speed(  AxisNo:Smallint;  OvrdSpeed:Double;   Enable:Smallint):Smallint;stdcall;

//Single Axis Position Mode Section 6.6
function  c154_start_tr_move(  AxisNo:Smallint;  Dist:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_ta_move(  AxisNo:Smallint;  Pos:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_sr_move(  AxisNo:Smallint;  Dist:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;
function  c154_start_sa_move(  AxisNo:Smallint;  Pos:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;
function  c154_set_move_ratio(  AxisNo:Smallint;  move_ratio:Double):Smallint;stdcall;


//Linear Interpolated Motion Section 6.7
  // Two Axes Linear Interpolation function
function  c154_start_tr_move_xy(  CardId:Smallint;  DistX:Double;  DistY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_tr_move_zu(  CardId:Smallint;  DistX:Double;  DistY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;

function  c154_start_ta_move_xy(  CardId:Smallint;  PosX:Double;  PosY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_ta_move_zu(  CardId:Smallint;  PosX:Double;  PosY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;

function  c154_start_sr_move_xy(  CardId:Smallint;  DistX:Double;  DistY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;
function  c154_start_sr_move_zu(  CardId:Smallint;  DistX:Double;  DistY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;

function  c154_start_sa_move_xy(  CardId:Smallint;  PosX:Double;  PosY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;
function  c154_start_sa_move_zu(  CardId:Smallint;  PosX:Double;  PosY:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;

//Any 2 of former or later 4 axes linear interpolation function
function  c154_start_tr_line2(  var AxisArray:Smallint;  var DistArray:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_ta_line2(  var AxisArray:Smallint;  var PosArray:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_sr_line2(  var AxisArray:Smallint;  var DistArray:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;
function  c154_start_sa_line2(  var AxisArray:Smallint;  var PosArray:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;

//Any 3 of former or later 4 axes linear interpolation function
function  c154_start_tr_line3(  var AxisArray:Smallint;  var DistArray:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_ta_line3(  var AxisArray:Smallint;  var PosArray:Double;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_sr_line3(  var AxisArray:Smallint;  var DistArray:Double;  StrVel:Double;  MaxVelv:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;
function  c154_start_sa_line3(  var AxisArray:Smallint;  var PosArray;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;

//Former or later 4 Axes linear interpolation function
function  c154_start_tr_line4(  var AxisArray:Smallint;  var DistArray;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_ta_line4(  var AxisArray:Smallint;  var PosArray;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double):Smallint;stdcall;
function  c154_start_sr_line4(  var AxisArray:Smallint;  var DistArray;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;
function  c154_start_sa_line4(  var AxisArray:Smallint;  var PosArray;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  Tdec:Double;  SVacc:Double;  SVdec:Double):Smallint;stdcall;

//Circular Interpolation Motion Section 6.8
  // Two Axes Arc Interpolation function 
function  c154_start_tr_arc_xy(  CardId:Smallint;  OffsetCx:Double;  OffsetCy:Double;  OffsetEx:Double;  OffsetEy:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double):Smallint;stdcall;
function  c154_start_ta_arc_xy(  CardId:Smallint;  Cx:Double;  Cy:Double;  Ex:Double;  Ey:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double):Smallint;stdcall;
function  c154_start_sr_arc_xy(  CardId:Smallint;  OffsetCx:Double;  OffsetCy:Double;  OffsetEx:Double;  OffsetEy:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double; SVacc:Double; SVdec:Double):Smallint;stdcall;
function  c154_start_sa_arc_xy(  CardId:Smallint;  Cx:Double;  Cy:Double;  Ex:Double;  Ey:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double; SVacc:Double; SVdec:Double):Smallint;stdcall;

function  c154_start_tr_arc_zu(  CardId:Smallint;  OffsetCx:Double;  OffsetCy:Double;  OffsetEx:Double;  OffsetEy:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double):Smallint;stdcall;
function  c154_start_ta_arc_zu(  CardId:Smallint;  Cx:Double;  Cy:Double;  Ex:Double;  Ey:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double):Smallint;stdcall;
function  c154_start_sr_arc_zu(  CardId:Smallint;  OffsetCx:Double;  OffsetCy:Double;  OffsetEx:Double;  OffsetEy:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double; SVacc:Double; SVdec:Double):Smallint;stdcall;
function  c154_start_sa_arc_zu(  CardId:Smallint;  Cx:Double;  Cy:Double;  Ex:Double;  Ey:Double;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double; SVacc:Double; SVdec:Double):Smallint;stdcall;

function  c154_start_tr_arc2(  var AxisArray:Smallint;  var OffsetCenter:Double;  var OffsetEnd;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double):Smallint;stdcall;
function  c154_start_ta_arc2(  var AxisArray:Smallint;  var CenterPos:Double;  var EndPos;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double):Smallint;stdcall;
function  c154_start_sr_arc2(  var AxisArray:Smallint;  var OffsetCenter:Double;  var OffsetEnd;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double;  SVacc:Double; SVdec:Double):Smallint;stdcall;
function  c154_start_sa_arc2(  var AxisArray:Smallint;  var CenterPos:Double;  var EndPos;   CW_CCW:Smallint;  StrVel:Double; MaxVel:Double; Tacc:Double; Tdec:Double;  SVacc:Double; SVdec:Double):Smallint;stdcall;

//Home Return Mode Section 6.10
function  c154_set_home_config(  AxisNo:Smallint;   home_mode:Smallint;   org_logic:Smallint;   ez_logi:Smallint;   ez_count:Smallint;   erc_out:Smallint):Smallint;stdcall;
function  c154_home_move(  AxisNo:Smallint;  StrVel:Double;  MaxVel:Double;  Tacc:Double):Smallint;stdcall;
function  c154_home_search(  AxisNo:Smallint;  StrVel:Double;  MaxVel:Double;  Tacc:Double;  ORGOffset:Double):Smallint;stdcall;

//Manual Pulser Motion Section 6.11
function  c154_set_pulser_iptmode(  AxisNo:Smallint;   InputMode:Smallint;   Inverse:Smallint):Smallint;stdcall;
function  c154_disable_pulser_input(  AxisNo:Smallint;  Disable:Word ):Smallint;stdcall;
function  c154_pulser_vmove(  AxisNo:Smallint;  SpeedLimit:Double):Smallint;stdcall;
function  c154_pulser_pmove(  AxisNo:Smallint;  Dist:Double;  SpeedLimit:Double):Smallint;stdcall;
function  c154_set_pulser_ratio(  AxisNo:Smallint;   DivF:Smallint;   MultiF:Smallint):Smallint;stdcall;

//Motion Status Section 6.12
function  c154_motion_done(  AxisNo:Smallint):Smallint;stdcall;

//Motion Interface I/O Section 6.13
function  c154_set_servo(  AxisNo:Smallint;   on_off:Smallint):Smallint;stdcall;
function  c154_set_clr_mode(  AxisNo:Smallint;   clr_mode:Smallint;   targetCounterInBit:Smallint):Smallint;stdcall;
function  c154_set_inp(  AxisNo:Smallint;   inp_enable:Smallint;   inp_logic:Smallint):Smallint;stdcall;
function  c154_set_alm(  AxisNo:Smallint;   alm_logic:Smallint;   alm_mode:Smallint):Smallint;stdcall;
function  c154_set_erc(  AxisNo:Smallint;   erc_logic:Smallint;   erc_pulse_width:Smallint;   erc_mode:Smallint):Smallint;stdcall;
function  c154_set_erc_out(  AxisNo:Smallint):Smallint;stdcall;
function  c154_clr_erc(  AxisNo:Smallint):Smallint;stdcall; 
function  c154_set_sd(  AxisNo:Smallint;   sd_logic:Smallint;   sd_latch:Smallint;   sd_mode:Smallint):Smallint;stdcall;
function  c154_enable_sd(  AxisNo:Smallint;   enable:Smallint):Smallint;stdcall;
function  c154_set_limit_logic(  AxisNo:Smallint;   Logic:Smallint ):Smallint;stdcall;
function  c154_set_limit_mode(  AxisNo:Smallint;   limit_mode:Smallint):Smallint;stdcall;
function  c154_get_io_status(  AxisNo:Smallint;  var io_sts:Word ):Smallint;stdcall;

//Interrupt Control Section 6.14
function  c154_int_control(  CardId:Smallint;   intFlag:Smallint):Smallint;stdcall;
function  c154_wait_error_interrupt(  AxisNo:Smallint;  TimeOut_ms :Longint):Smallint;stdcall;
function  c154_wait_motion_interrupt(  AxisNo:Smallint;   IntFactorBitNo:Smallint;  TimeOut_ms:Longint ):Smallint;stdcall;
function  c154_set_motion_int_factor(  AxisNo:Smallint; int_factor:Longword ):Smallint;stdcall;

//Position Control and Counters Section 6.15
function  c154_get_position(  AxisNo:Smallint;  var Pos:Double):Smallint;stdcall;
function  c154_set_position(  AxisNo:Smallint;  Pos:Double):Smallint;stdcall;
function  c154_get_command(  AxisNo:Smallint;  var Cmd:Longint):Smallint;stdcall;
function  c154_set_command(  AxisNo:Smallint;  Cmd:Longint):Smallint;stdcall;
function  c154_get_error_counter(  AxisNo:Smallint;   var error):Smallint;stdcall;
function  c154_reset_error_counter(  AxisNo:Smallint):Smallint;stdcall;
function  c154_set_general_counter(  AxisNo:Smallint;   CntSrc:Smallint;  CntValue:Double):Smallint;stdcall;
function  c154_get_general_counter(  AxisNo:Smallint;  var CntValue:Double):Smallint;stdcall;

//Continuous Motion Section 6.17
function  c154_set_continuous_move(  AxisNo:Smallint;   Enable:Smallint):Smallint;stdcall;
function  c154_check_continuous_buffer(  AxisNo:Smallint):Smallint;stdcall;
function  c154_dwell_move(  AxisNo:Smallint;  milliSecond:Double):Smallint;stdcall;

//Multiple Axes Simultaneous Operation Section 6.18
function  c154_set_tr_move_all(  TotalAxes:Smallint;   var AxisArray:Smallint;  var DistA:Double;  var StrVelA:Double;  var MaxVelA:Double;  var TaccA:Double;  var TdecA:Double):Smallint;stdcall;
function  c154_set_sa_move_all(  TotalAx:Smallint;   var AxisArray:Smallint;  var PosA:Double;  var StrVelA:Double;  var MaxVelA:Double;  var TaccA:Double;  var TdecA:Double;  var SVaccA:Double;  var SVdecA:Double):Smallint;stdcall;
function  c154_set_ta_move_all(  TotalAx:Smallint;   var AxisArray:Smallint;  var PosA:Double;  var StrVelA:Double;  var MaxVelA:Double;  var TaccA:Double;  var TdecA:Double):Smallint;stdcall;
function  c154_set_sr_move_all(  TotalAx:Smallint;   var AxisArray:Smallint;  var DistA:Double;  var StrVelA:Double;  var MaxVelA:Double;  var TaccA:Double;  var TdecA:Double;  var SVaccA:Double;  var SVdecA:Double):Smallint;stdcall;
function  c154_start_move_all(  FirstAxisNo:Smallint):Smallint;stdcall;
function  c154_stop_move_all(  FirstAxisNo:Smallint):Smallint;stdcall;


function c154_set_sync_stop_mode( AxisNo:Smallint; stop_mode:Smallint):Smallint;stdcall;
function c154_set_sync_option(AxisNo:Smallint;sync_stop_on:Smallint;cstop_output_on:Smallint;sync_option1:Smallint;sync_option2:Smallint):Smallint;stdcall;
function c154_set_sync_signal_source(AxisNo:Smallint;sync_axis:Smallint):Smallint;stdcall;
function c154_set_sync_signal_mode(AxisNo:Smallint; mode:Smallint):Smallint;stdcall;


//General-purposed Input/Output Section 6.19
function  c154_set_gpio_output(  CardId:Smallint;   DoValue :Smallint):Smallint;stdcall;
function  c154_get_gpio_output(  CardId:Smallint;   var DoValue:Smallint ):Smallint;stdcall;
function  c154_get_gpio_input(  CardId:Smallint;   var DiValue:Smallint ):Smallint;stdcall;
function  c154_set_gpio_input_function(  CardId:Smallint;   Channel:Smallint;   Select:Smallint;   Logic:Smallint):Smallint;stdcall;

//Soft Limit 6.20
function  c154_disable_soft_limit(  AxisNo:Smallint):Smallint;stdcall;
function  c154_enable_soft_limit(  AxisNo:Smallint;   Action:Smallint):Smallint;stdcall;
function  c154_set_soft_limit(  AxisNo:Smallint;  PlusLimit:Longint;  MinusLimit:Longint):Smallint;stdcall;

//Backlas Compensation / Vibration Suppression 6.21
function  c154_backlash_comp(  AxisNo:Smallint;   CompPulse:Double;   Mode:Smallint):Smallint;stdcall;
function  c154_suppress_vibration(  AxisNo:Smallint;  ReverseTime:Word;  ForwardTime:Word):Smallint;stdcall;
function  c154_set_fa_speed(  AxisNo:Smallint;  FA_Speed:Double):Smallint;stdcall;

//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
implementation

// System Section 6.3
function  c154_initial; external 'C154.dll';
function  c154_close; external 'C154.dll';
function  c154_get_version; external 'C154.dll';
function  c154_set_security_key; external 'C154.dll';
function  c154_check_security_key; external 'C154.dll';
function  c154_reset_security_key; external 'C154.dll';
function  c154_config_from_file; external 'C154.dll';

//Pulse Input/Output Configuration Section 6.4
function  c154_set_pls_outmode; external 'C154.dll';
function  c154_set_pls_iptmode; external 'C154.dll';
function  c154_set_feedback_src; external 'C154.dll';

//Velocity mode motion Section 6.5
function  c154_tv_move; external 'C154.dll';
function  c154_sv_move; external 'C154.dll';
function  c154_sd_stop; external 'C154.dll';
function  c154_emg_stop; external 'C154.dll';
function  c154_get_current_speed; external 'C154.dll';
function  c154_speed_override; external 'C154.dll';
function  c154_set_max_override_speed; external 'C154.dll';

//Single Axis Position Mode Section 6.6
function  c154_start_tr_move; external 'C154.dll';
function  c154_start_ta_move; external 'C154.dll';
function  c154_start_sr_move; external 'C154.dll';
function  c154_start_sa_move; external 'C154.dll';
function  c154_set_move_ratio; external 'C154.dll';

//Linear Interpolated Motion Section 6.7
  // Two Axes Linear Interpolation function
function  c154_start_tr_move_xy; external 'C154.dll';
function  c154_start_tr_move_zu; external 'C154.dll';

function  c154_start_ta_move_xy; external 'C154.dll';
function  c154_start_ta_move_zu; external 'C154.dll';

function  c154_start_sr_move_xy; external 'C154.dll';
function  c154_start_sr_move_zu; external 'C154.dll';

function  c154_start_sa_move_xy; external 'C154.dll';
function  c154_start_sa_move_zu; external 'C154.dll';

//Any 2 of former or later 4 axes linear interpolation function
function  c154_start_tr_line2; external 'C154.dll';
function  c154_start_ta_line2; external 'C154.dll';
function  c154_start_sr_line2; external 'C154.dll';
function  c154_start_sa_line2; external 'C154.dll';

//Any 3 of former or later 4 axes linear interpolation function
function  c154_start_tr_line3; external 'C154.dll';
function  c154_start_ta_line3; external 'C154.dll';
function  c154_start_sr_line3; external 'C154.dll';
function  c154_start_sa_line3; external 'C154.dll';

//Former or later 4 Axes linear interpolation function
function  c154_start_tr_line4; external 'C154.dll';
function  c154_start_ta_line4; external 'C154.dll';
function  c154_start_sr_line4; external 'C154.dll';
function  c154_start_sa_line4; external 'C154.dll';

//Circular Interpolation Motion Section 6.8
  // Two Axes Arc Interpolation function 
function  c154_start_tr_arc_xy; external 'C154.dll';
function  c154_start_ta_arc_xy; external 'C154.dll';
function  c154_start_sr_arc_xy; external 'C154.dll';
function  c154_start_sa_arc_xy; external 'C154.dll';

function  c154_start_tr_arc_zu; external 'C154.dll';
function  c154_start_ta_arc_zu; external 'C154.dll';
function  c154_start_sr_arc_zu; external 'C154.dll';
function  c154_start_sa_arc_zu; external 'C154.dll';

function  c154_start_tr_arc2; external 'C154.dll';
function  c154_start_ta_arc2; external 'C154.dll';
function  c154_start_sr_arc2; external 'C154.dll';
function  c154_start_sa_arc2; external 'C154.dll';


//Home Return Mode Section 6.10
function  c154_set_home_config; external 'C154.dll';
function  c154_home_move; external 'C154.dll';
function  c154_home_search; external 'C154.dll';

//Manual Pulser Motion Section 6.11
function  c154_set_pulser_iptmode; external 'C154.dll';
function  c154_disable_pulser_input; external 'C154.dll';
function  c154_pulser_vmove; external 'C154.dll';
function  c154_pulser_pmove; external 'C154.dll';
function  c154_set_pulser_ratio; external 'C154.dll';

//Motion Status Section 6.12
function  c154_motion_done; external 'C154.dll';

//Motion Interface I/O Section 6.13
function  c154_set_servo; external 'C154.dll';
function  c154_set_clr_mode; external 'C154.dll';
function  c154_set_inp; external 'C154.dll';
function  c154_set_alm; external 'C154.dll';
function  c154_set_erc; external 'C154.dll';
function  c154_set_erc_out; external 'C154.dll';
function  c154_clr_erc; external 'C154.dll';
function  c154_set_sd; external 'C154.dll';
function  c154_enable_sd; external 'C154.dll';
function  c154_set_limit_logic; external 'C154.dll';
function  c154_set_limit_mode; external 'C154.dll';
function  c154_get_io_status; external 'C154.dll';

//Interrupt Control Section 6.14
function  c154_int_control; external 'C154.dll';
function  c154_wait_error_interrupt; external 'C154.dll';
function  c154_wait_motion_interrupt; external 'C154.dll';
function  c154_set_motion_int_factor; external 'C154.dll';

//Position Control and Counters Section 6.15
function  c154_get_position; external 'C154.dll';
function  c154_set_position; external 'C154.dll';
function  c154_get_command; external 'C154.dll';
function  c154_set_command; external 'C154.dll';
function  c154_get_error_counter; external 'C154.dll';
function  c154_reset_error_counter; external 'C154.dll';
function  c154_set_general_counter; external 'C154.dll';
function  c154_get_general_counter; external 'C154.dll';

//Continuous Motion Section 6.17
function  c154_set_continuous_move; external 'C154.dll';
function  c154_check_continuous_buffer; external 'C154.dll';
function  c154_dwell_move; external 'C154.dll';

//Multiple Axes Simultaneous Operation Section 6.18
function  c154_set_tr_move_all; external 'C154.dll';
function  c154_set_sa_move_all; external 'C154.dll';
function  c154_set_ta_move_all; external 'C154.dll';
function  c154_set_sr_move_all; external 'C154.dll';
function  c154_start_move_all; external 'C154.dll';
function  c154_stop_move_all; external 'C154.dll';

//General-purposed Input/Output Section 6.19
function  c154_set_gpio_output; external 'C154.dll';
function  c154_get_gpio_output; external 'C154.dll';
function  c154_get_gpio_input; external 'C154.dll';
function  c154_set_gpio_input_function; external 'C154.dll';

//Soft Limit 6.20
function  c154_disable_soft_limit; external 'C154.dll';
function  c154_enable_soft_limit; external 'C154.dll';
function  c154_set_soft_limit; external 'C154.dll';

//Backlas Compensation / Vibration Suppression 6.21
function  c154_backlash_comp; external 'C154.dll';
function  c154_suppress_vibration; external 'C154.dll';
function  c154_set_fa_speed; external 'C154.dll';

//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
end.
