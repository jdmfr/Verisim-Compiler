

// This file was automatically generated by Coco/R; don't modify it.
#if !defined(Coco_COCO_PARSER_H__)
#define Coco_COCO_PARSER_H__

#include <QStack>
#include <Verilog/VlSynTree.h>


#include "VlPpLexer.h"

namespace Coco {


class Errors {
public:
	int count;			// number of errors detected

	Errors();
    static void SynErr(const QString& sourcePath, int line, int col, int n, Vl::Errors* err, const char* ctx, const QString& = QString() );
	void Error(int line, int col, const char *s);
	void Warning(int line, int col, const char *s);
	void Warning(const char *s);
	void Exception(const char *s);

}; // Errors

class Parser {
private:
	enum {
		_EOF=0,
		_TPlus=1,
		_TMinus=2,
		_TBang=3,
		_TBangEq=4,
		_TBang2Eq=5,
		_TTilde=6,
		_TTildeBar=7,
		_TTildeAmp=8,
		_TTildeHat=9,
		_THat=10,
		_THatTilde=11,
		_TSlash=12,
		_TPercent=13,
		_TEq=14,
		_T2Eq=15,
		_T3Eq=16,
		_TAmp=17,
		_T2Amp=18,
		_T3Amp=19,
		_TBar=20,
		_T2Bar=21,
		_TStar=22,
		_T2Star=23,
		_TLt=24,
		_TLeq=25,
		_T2Lt=26,
		_T3Lt=27,
		_TGt=28,
		_TGeq=29,
		_T2Gt=30,
		_T3Gt=31,
		_THash=32,
		_TAt=33,
		_TQmark=34,
		_TEqGt=35,
		_TStarGt=36,
		_TMinusGt=37,
		_TLpar=38,
		_TRpar=39,
		_TLbrack=40,
		_TRbrack=41,
		_TLbrace=42,
		_TRbrace=43,
		_TLatt=44,
		_TRatt=45,
		_TLcmt=46,
		_TRcmt=47,
		_TComma=48,
		_TDot=49,
		_TSemi=50,
		_TColon=51,
		_TPlusColon=52,
		_TMinusColon=53,
		_Talways=54,
		_Tand=55,
		_Tassign=56,
		_Tautomatic=57,
		_Tbegin=58,
		_Tbuf=59,
		_Tbufif0=60,
		_Tbufif1=61,
		_Tcase=62,
		_Tcasex=63,
		_Tcasez=64,
		_Tcell=65,
		_Tcmos=66,
		_Tconfig=67,
		_Tdeassign=68,
		_Tdefault=69,
		_Tdefparam=70,
		_Tdesign=71,
		_Tdisable=72,
		_Tedge=73,
		_Telse=74,
		_Tend=75,
		_Tendcase=76,
		_Tendconfig=77,
		_Tendfunction=78,
		_Tendgenerate=79,
		_Tendmodule=80,
		_Tendprimitive=81,
		_Tendspecify=82,
		_Tendtable=83,
		_Tendtask=84,
		_Tevent=85,
		_Tfor=86,
		_Tforce=87,
		_Tforever=88,
		_Tfork=89,
		_Tfunction=90,
		_Tgenerate=91,
		_Tgenvar=92,
		_Thighz0=93,
		_Thighz1=94,
		_Tif=95,
		_Tifnone=96,
		_Tincdir=97,
		_Tinclude=98,
		_Tinitial=99,
		_Tinout=100,
		_Tinput=101,
		_Tinstance=102,
		_Tinteger=103,
		_Tjoin=104,
		_Tlarge=105,
		_Tliblist=106,
		_Tlibrary=107,
		_Tlocalparam=108,
		_Tmacromodule=109,
		_Tmedium=110,
		_Tmodule=111,
		_Tnand=112,
		_Tnegedge=113,
		_Tnmos=114,
		_Tnor=115,
		_Tnoshowcancelled=116,
		_Tnot=117,
		_Tnotif0=118,
		_Tnotif1=119,
		_Tor=120,
		_Toutput=121,
		_Tparameter=122,
		_Tpmos=123,
		_Tposedge=124,
		_Tprimitive=125,
		_Tpull0=126,
		_Tpull1=127,
		_Tpulldown=128,
		_Tpullup=129,
		_Tpulsestyle_onevent=130,
		_Tpulsestyle_ondetect=131,
		_Trcmos=132,
		_Treal=133,
		_Trealtime=134,
		_Treg=135,
		_Trelease=136,
		_Trepeat=137,
		_Trnmos=138,
		_Trpmos=139,
		_Trtran=140,
		_Trtranif0=141,
		_Trtranif1=142,
		_Tscalared=143,
		_Tshowcancelled=144,
		_Tsigned=145,
		_Tsmall=146,
		_Tspecify=147,
		_Tspecparam=148,
		_Tstrong0=149,
		_Tstrong1=150,
		_Tsupply0=151,
		_Tsupply1=152,
		_Ttable=153,
		_Ttask=154,
		_Ttime=155,
		_Ttran=156,
		_Ttranif0=157,
		_Ttranif1=158,
		_Ttri=159,
		_Ttri0=160,
		_Ttri1=161,
		_Ttriand=162,
		_Ttrior=163,
		_Ttrireg=164,
		_Tunsigned=165,
		_Tuse=166,
		_Tuwire=167,
		_Tvectored=168,
		_Twait=169,
		_Twand=170,
		_Tweak0=171,
		_Tweak1=172,
		_Twhile=173,
		_Twire=174,
		_Twor=175,
		_Txnor=176,
		_Txor=177,
		_TmaxKeyword=178,
		_TPathPulse=179,
		_TSetup=180,
		_THold=181,
		_TSetupHold=182,
		_TRecovery=183,
		_TRemoval=184,
		_TRecrem=185,
		_TSkew=186,
		_TTimeSkew=187,
		_TFullSkew=188,
		_TPeriod=189,
		_TWidth=190,
		_TNoChange=191,
		_TmaxSystemName=192,
		_TString=193,
		_TIdent=194,
		_TSysName=195,
		_TCoDi=196,
		_TRealnum=197,
		_TNatural=198,
		_TSizedBased=199,
		_TBasedInt=200,
		_TBaseFormat=201,
		_TBaseValue=202,
		_TAttribute=203,
		_TMacroUsage=204
	};
	int maxT;

	int errDist;
	int minErrDist;

	void SynErr(int n, const char* ctx = 0);
	void Get();
	void Expect(int n, const char* ctx = 0);
	bool StartOf(int s);
	void ExpectWeak(int n, int follow);
	bool WeakSeparator(int n, int syFol, int repFol);

public:
	Vl::PpLexer *scanner;
	Vl::Errors  *errors;

	Vl::Token d_cur;
	Vl::Token d_next;
	struct TokDummy
	{
		int kind;
	};
	TokDummy d_dummy;
	TokDummy *la;			// lookahead token
	QList<Vl::Token> d_sections;
	
	int peek( quint8 la = 1 );

    void RunParser()
    {
        d_stack.push(&d_root);
        Parse();
        d_stack.pop();
    }
  
	Vl::SynTree d_root;
	QStack<Vl::SynTree*> d_stack;
	void addTerminal() {
		Vl::SynTree* n = new Vl::SynTree( d_cur ); d_stack.top()->d_children.append(n);
	}



	Parser(Vl::PpLexer *scanner,Vl::Errors*);
	~Parser();
	void SemErr(const char* msg);

	void Verilog05();
	void translation_unit();
	void identifier();
	void system_name();
	void real_number();
	void natural_number();
	void sizedbased_number();
	void based_number();
	void base_format();
	void base_value();
	void string();
	void unary_operator();
	void binary_operator();
	void unary_module_path_operator();
	void binary_module_path_operator();
	void module_declaration();
	void udp_declaration();
	void config_declaration();
	void library_declaration();
	void include_statement();
	void library_identifier();
	void file_path_spec();
	void module_keyword();
	void module_identifier();
	void module_parameter_port_list();
	void list_of_ports();
	void list_of_port_declarations();
	void module_item();
	void parameter_declaration();
	void port();
	void port_declaration();
	void port_expression();
	void port_identifier();
	void port_reference();
	void constant_range_expression();
	void inout_declaration();
	void input_declaration();
	void output_declaration();
	void non_port_module_item();
	void module_or_generate_item();
	void module_or_generate_item_declaration();
	void local_parameter_declaration();
	void parameter_override();
	void continuous_assign();
	void gate_instantiation();
	void module_or_udp_instantiation();
	void initial_construct();
	void always_construct();
	void loop_generate_construct();
	void conditional_generate_construct();
	void net_declaration();
	void reg_declaration();
	void integer_declaration();
	void real_declaration();
	void time_declaration();
	void realtime_declaration();
	void event_declaration();
	void genvar_declaration();
	void task_declaration();
	void function_declaration();
	void generate_region();
	void specify_block();
	void specparam_declaration();
	void list_of_defparam_assignments();
	void config_identifier();
	void design_statement();
	void config_rule_statement();
	void cell_identifier();
	void default_clause();
	void inst_clause();
	void cell_clause();
	void liblist_clause();
	void use_clause();
	void inst_name();
	void topmodule_identifier();
	void instance_identifier();
	void range();
	void parameter_type();
	void list_of_param_assignments();
	void list_of_specparam_assignments();
	void net_type();
	void list_of_port_identifiers();
	void list_of_variable_port_identifiers();
	void output_variable_type();
	void list_of_event_identifiers();
	void list_of_variable_identifiers();
	void list_of_net_decl_assignments_or_identifiers();
	void net_identifier();
	void dimension();
	void expression();
	void drive_strength();
	void charge_strength();
	void delay3();
	void list_of_real_identifiers();
	void real_type();
	void real_identifier();
	void constant_expression();
	void variable_type();
	void variable_identifier();
	void strength0();
	void strength1();
	void delay();
	void delay_value();
	void mintypmax_expression();
	void expression_nlr();
	void delay2();
	void unsigned_or_real_number();
	void defparam_assignment();
	void event_identifier();
	void param_assignment();
	void specparam_assignment();
	void hierarchical_parameter_identifier();
	void constant_mintypmax_expression();
	void parameter_identifier();
	void specparam_identifier();
	void pulse_control_specparam();
	void reject_limit_value();
	void error_limit_value();
	void limit_value();
	void dimension_constant_expression();
	void msb_constant_expression();
	void lsb_constant_expression();
	void function_range_or_type();
	void function_identifier();
	void function_port_list();
	void function_item_declaration();
	void function_statement();
	void block_item_declaration();
	void tf_input_declaration();
	void task_identifier();
	void task_port_list();
	void task_item_declaration();
	void statement_or_null();
	void tf_output_declaration();
	void tf_inout_declaration();
	void task_port_item();
	void task_port_type();
	void block_reg_declaration();
	void block_integer_declaration();
	void block_time_declaration();
	void block_real_declaration();
	void block_realtime_declaration();
	void list_of_block_variable_identifiers();
	void list_of_block_real_identifiers();
	void block_variable_type();
	void block_real_type();
	void cmos_switchtype();
	void cmos_switch_instance();
	void enable_gatetype();
	void enable_gate_instance();
	void mos_switchtype();
	void mos_switch_instance();
	void n_input_gatetype();
	void n_input_gate_instance();
	void n_output_gatetype();
	void n_output_gate_instance();
	void pass_en_switchtype();
	void pass_enable_switch_instance();
	void pass_switchtype();
	void pass_switch_instance();
	void pulldown_strength();
	void pull_gate_instance();
	void pullup_strength();
	void name_of_gate_instance();
	void output_terminal();
	void input_terminal();
	void ncontrol_terminal();
	void pcontrol_terminal();
	void enable_terminal();
	void input_or_output_terminal();
	void expression_2();
	void inout_terminal();
	void gate_instance_identifier();
	void net_lvalue();
	void named_parameter_assignment();
	void list_of_genvar_identifiers();
	void genvar_identifier();
	void genvar_initialization();
	void genvar_expression();
	void genvar_iteration();
	void generate_block();
	void genvar_primary();
	void genvar_expression_nlr();
	void constant_primary();
	void if_generate_construct();
	void case_generate_construct();
	void generate_block_or_null();
	void case_generate_item();
	void generate_block_identifier();
	void udp_identifier();
	void udp_port_list();
	void udp_declaration_port_list();
	void udp_port_declaration();
	void udp_body();
	void output_port_identifier();
	void input_port_identifier();
	void udp_output_declaration();
	void udp_input_declaration();
	void udp_reg_declaration();
	void udp_initial_statement();
	void sequential_or_combinatorial_entry();
	void init_val();
	void level_or_edge_symbol();
	void level_symbol();
	void number();
	void edge_descriptor();
	void scalar_constant();
	void list_of_net_assignments();
	void net_assignment();
	void statement();
	void procedural_continuous_assignments();
	void variable_assignment();
	void variable_lvalue();
	void variable_or_net_lvalue();
	void par_block();
	void block_identifier();
	void seq_block();
	void blocking_or_nonblocking_assignment_or_task_enable();
	void delay_or_event_control();
	void case_statement();
	void conditional_statement();
	void disable_statement();
	void event_trigger();
	void loop_statement();
	void procedural_timing_control_statement();
	void system_task_enable();
	void wait_statement();
	void delay_control();
	void event_control();
	void hierarchical_task_or_block_identifier();
	void hierarchical_identifier();
	void event_expression();
	void hierarchical_event_identifier();
	void hierarchical_identifier_range();
	void event_expression_nlr();
	void procedural_timing_control();
	void case_item();
	void system_task_identifier();
	void specify_item();
	void pulsestyle_declaration();
	void showcancelled_declaration();
	void path_declaration();
	void system_timing_check();
	void list_of_path_outputs();
	void simple_or_edge_sensitive_path_declaration();
	void state_dependent_path_declaration();
	void parallel_or_full_path_description();
	void list_of_path_inputs();
	void polarity_operator();
	void specify_output_terminal_descriptor();
	void simple_path_declaration();
	void path_delay_value();
	void specify_input_terminal_descriptor();
	void input_identifier();
	void output_identifier();
	void input_or_inout_port_identifier();
	void output_or_inout_port_identifier();
	void list_of_path_delay_expressions();
	void path_delay_expression();
	void edge_identifier();
	void data_source_expression();
	void simple_or_edge_sensitive_path_description();
	void module_path_expression();
	void dlr_setup_timing_check();
	void dlr_hold_timing_check();
	void dlr_setuphold_timing_check();
	void dlr_recovery_timing_check();
	void dlr_removal_timing_check();
	void dlr_recrem_timing_check();
	void dlr_skew_timing_check();
	void dlr_timeskew_timing_check();
	void dlr_fullskew_timing_check();
	void dlr_period_timing_check();
	void dlr_width_timing_check();
	void dlr_nochange_timing_check();
	void data_event();
	void reference_event();
	void timing_check_limit();
	void notifier();
	void stamptime_condition();
	void checktime_condition();
	void delayed_reference();
	void delayed_data();
	void event_based_flag();
	void remain_active_flag();
	void controlled_reference_event();
	void threshold();
	void start_edge_offset();
	void end_edge_offset();
	void controlled_timing_check_event();
	void timing_check_event();
	void terminal_identifier();
	void timing_check_event_control();
	void specify_terminal_descriptor();
	void timing_check_condition();
	void edge_control_specifier();
	void specify_input_or_output_terminal_descriptor();
	void scalar_timing_check_condition();
	void constant_expression_nlr();
	void width_constant_expression();
	void primary();
	void module_path_primary();
	void module_path_expression_nlr();
	void module_path_mintypmax_expression();
	void range_expression();
	void system_function_identifier();
	void hierarchical_identifier_range_const();
	void parameter_value_assignment_or_delay2();
	void module_or_udp_instance();
	void port_connection_or_output_terminal();
	void primary_2();

	void Parse();

}; // end Parser

} // namespace


#endif
