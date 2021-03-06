#  Copyright (c) 2016-2017 Rocky Bernstein
"""
More complex expression parsing
"""
# from __future__ import print_function
import os,sys
os.chdir(sys.path[0])



from spark_parser.ast import AST

from VeriSim_Scanner import VeriSimScanner, ENDMARKER

from spark_parser.scanner import GenericScanner, GenericToken
from spark_parser import GenericParser

DEFAULT_DEBUG = {'rules': False, 'transition': False, 'reduce' : False,
                 'errorstack': 'full', 'context': False, 'dups': False}
# class VeriSimParser(GenericASTBuilder):
class VeriSimParser(GenericParser):
    """A more complete spark example: a Python 2 Parser.

    Note: function parse() comes from GenericASTBuilder
    """

    def __init__(self, start='translation_unit', debug=DEFAULT_DEBUG):
    #    super(VeriSimParser, self).__init__(AST, start, debug=debug)
        GenericParser.__init__(self,start, debug)
        self.start = start
        self.debug = debug
        
        # Put left-recursive list non-terminals:
        # x ::= x y
        # x ::=
        self.collect = frozenset(('stmts', 'comments', 'dot_names', 'dots',
                        'comp_op_exprs', 'newline_or_stmts',
                        'comma_names', 'comma_fpdef_opt_eqtests',)
        )


    def debug_reduce(self, rule, tokens, parent, i):
        """Customized format and print for our kind of tokens
        which gets called in debugging grammar reduce rules
        """
        prefix = '           '
        if parent and tokens:
            p_token = tokens[parent]
            if hasattr(p_token, 'line'):
                prefix = 'L.%3d.%03d: ' % (p_token.line, p_token.column)
                pass
            pass
        print("%s%s ::= %s" % (prefix, rule[0], ' '.join(rule[1])))

    def nonterminal(self, nt, args):
        # nonterminal with a (reserved) single word derivation
        no_skip = ('pass_stmt', 'continue_stmt', 'break_stmt', 'return_stmt')

        has_len = hasattr(args, '__len__')

        if nt in self.collect and len(args) > 1:
            #
            #  Collect iterated thingies together.
            #
            rv = args[0]
            for arg in args[1:]:
                rv.append(arg)
        elif (has_len and len(args) == 1 and
              hasattr(args[0], '__len__') and args[0] not in no_skip and
              len(args[0]) == 1):
            # Remove singleton derivations
            rv = GenericASTBuilder.nonterminal(self, nt, args[0])
            del args[0] # save memory
        elif (has_len and len(args) == 2 and
              hasattr(args[1], '__len__') and len(args[1]) == 0):
            # Remove trailing epsilon rules, but only when there
            # are two items.
            if hasattr(args[0], '__len__') and len(args[0]) == 1:
                # Remove singleton derivation
                rv = args[0]
            else:
                rv = GenericASTBuilder.nonterminal(self, nt, args[:1])
            del args[1] # save memory
        else:
            rv = GenericASTBuilder.nonterminal(self, nt, args)
        return rv

    ##########################################################
    # Verisim grammar rules. Grammar rule functions
    # start with the name p_ and are collected automatically
    ##########################################################
    def p_main_module(self,args):
        '''
        translation_unit ::= module_declaration ENDMARKER
        '''
        return AST('TOP',[args[0]])

    def p_module_dec(self,args):
        '''
        module_declaration ::= MODULE module_identifier dor_list_of_ports_or_decla_opt_1 SEMICOLON module_items ENDMODULE
        '''
        tmp = AST('MODULE' , [args[1] ,args[2],args[4]] )  
        return tmp

    def p_module_dec_1(self,args):
        '''
        ## dor_list_of_ports_or_decla_opt_1
        dor_list_of_ports_or_decla_opt_1 ::= LPAREN dor_list_of_ports_or_decla_opt_2 RPAREN
        dor_list_of_ports_or_decla_opt_1 ::=
        '''
        if len(args)!=0 and args[1] != None :
           return AST('single', [args[1]]) 
        pass

    def p_module_dec_2(self,args):
        '''
        dor_list_of_ports_or_decla_opt_2 ::= dor_list_of_ports_or_decla
        dor_list_of_ports_or_decla_opt_2 ::=
        '''
        if len(args)!=0 and args[0] != None :
           return AST('single', [args[0]]) 
        pass

    def p_module_dec_3(self,args):
        '''
        dor_list_of_ports_or_decla ::= list_of_port_declarations
        '''
        return AST('single',[args[0]])

    def p_list_of_ports(self,args):
        '''
        ## 这里的port真的需要左右有中括号吗？ list_of_ports ::= port (COMMA [port])*
        ## new comma_port_opt_s
        list_of_ports ::= port comma_port_opt_s
        
        list_of_port_declarations ::= port_declaration comma_port_declarations
        '''
        if len(args) >1 :
            return AST('PORTs', [args[0],args[1]])
        return AST('single', [args[0]])
    
    def p_port_dec(self,args):
        '''
        port_declaration ::= input_declaration
        port_declaration ::= output_declaration
        
        '''
        if len(args) >0 :
            return AST('single',[args[0]])
        pass
        
    def p_module_dec_4(self,args):
        '''
        comma_port_opt_s ::= comma_port_opt_s COMMA port_opt 
        comma_port_opt_s ::= 
        '''
        if len(args) !=0:
            return AST('single',[args[2]] )
        pass
    
    def p_module_name(self,args):
        '''
        module_identifier ::= identifier 
        '''
        return AST('module_name',args[0])

    def p_ident_kind(self,args):
        '''
        
        port_identifier ::= identifier
        net_identifier ::= identifier 
        gate_instance_identifier ::= identifier 
        genvar_identifier ::= identifier 
        block_identifier ::= identifier 

        '''
        return AST('single' ,args[0])
        
    def p_ident(self,args):
        '''
        identifier ::= NAME
        '''
        return AST('single',[args[0]])


    def p_port_output_decla(self,args):
        '''
        output_declaration ::= OUTPUT wire_opt signed_opt range_opt list_of_port_identifiers
        output_declaration ::= OUTPUT REG signed_opt range_opt list_of_variable_port_identifiers
        output_declaration ::= OUTPUT INTEGER list_of_variable_port_identifiers
        '''
        ## this should be edit
        tmp = AST('OUTPUT',[args[3],args[4]] )
        return tmp
    
    def p_port_range_decla(self,args):
        '''
        range_opt ::= range
        range_opt ::= 
        '''
        tmp = None
        if len(args) ==0 :
            tmp = AST('WIDTH', [None] )
        else :
            tmp = AST('WIDTH', [args[0]])
        return tmp


    def p_range_decla(self,args):
        '''
        range ::= LBRACKET msb_constant_expression COLON lsb_constant_expression RBRACKET
        '''
        tmp =  AST('RANGE' , [args[1] , args[3]])
        return tmp

    def p_constant_pri_1(self,args):
        '''
        real_number ::= NUMBER
        '''
        tmp = AST('NUMBER', [args[0]])
        return tmp


    def p_port(self,args):
        '''
        port ::= port_expression
        port ::= DOT port_identifier LPAREN port_expression_opt RPAREN
        
        '''
        if len(args) == 1 :
            return AST('PORT', [args[0]])
        else :
            return AST('PORT',[None])
        
    def p_port_expression(self,args):
        '''
        port_expression ::= port_reference
        port_expression ::= LBRACE port_reference  comma_port_references RBRACE 
        '''
        if len(args) ==1 :
            return AST('single',[args[0]])
        else :
            return AST('PORT_COMBINE',[args[1],args[2]])

    def p_port_reference(self,args):
        '''
        ##  port_reference ::= port_identifier ['['constant_range_expression']']
        port_reference ::= port_identifier LBRACKET_constant_range_expression_RBRACKET_opt 
        '''
        return AST('port_reference', [args[0],args[1]] )
        
    def p_port_ref_1(self,args):
        '''
        LBRACKET_constant_range_expression_RBRACKET_opt ::= LBRACKET constant_range_expression RBRACKET
        LBRACKET_constant_range_expression_RBRACKET_opt ::=
        '''
        if len(args) >0 :
            return AST('single',[args[1]])
        pass

    def p_input_dec(self,args):
        '''
        input_declaration ::= INPUT wire_opt signed_opt range_opt list_of_port_identifiers
        '''
        if len(args) >0 :
            return AST('INPUT',[args[3],args[4]])
        pass

    def p_port_dec_more(self,args):
        '''
        comma_port_declarations ::= comma_port_declarations COMMA port_declaration
        comma_port_declarations ::= 
        '''
        if len(args) >0 :
                return AST('MORE',[args[0],args[2]])
        return AST('None',[None])
        

    def p_port_ident(self,args):
        '''
        list_of_port_identifiers ::= port_identifier COMMA_port_identifiers
        COMMA_port_identifiers ::= COMMA_port_identifiers COMMA port_identifier
        COMMA_port_identifiers ::=
        '''
        if len(args) ==2  :
            return AST('PORT_ident',[args[0]])
        elif len( args) == 3 :
            if args[0] != None :
                return AST('PORT_ident',[args[0],args[3]])
            else :
                return AST('PORT_ident',[args[3]])
        elif len(args)==1:
            return AST('single',[args[0]])
        pass

    def p_const_expr(self,args):
        '''
        ## constant_expression ::= [ unary_operator ] constant_primary constant_expression_nlrs
        constant_expression ::= unary_operator_opt constant_primary constant_expression_nlrs
        '''
        if len(args) >0 and args[2]!=None :
            return AST('single',[args[1],args[2]])
        else : 
            return AST('single',[args[1]])
        pass

    def p_generate_single(self,args):
        '''
        msb_constant_expression ::= constant_expression 
        lsb_constant_expression ::= constant_expression
        constant_primary ::= number
        number ::= real_number
        module_item ::= non_port_module_item

        non_port_module_item ::= module_or_generate_item
        non_port_module_item ::= generate_region

        module_or_generate_item ::= module_or_generate_item_declaration
        module_or_generate_item ::= continuous_assign
        module_or_generate_item ::= gate_instantiation
        module_or_generate_item ::= always_construct
        module_or_generate_item ::= loop_generate_construct
        module_or_generate_item ::= conditional_generate_construct

        module_or_generate_item_declaration ::= net_declaration
        module_or_generate_item_declaration ::= reg_declaration 
        module_or_generate_item_declaration ::= integer_declaration
        module_or_generate_item_declaration ::= genvar_declaration
        ##---- always statement

        statement ::= blocking_assignment
        statement ::= case_statement
        statement ::= conditional_statement
        statement ::= loop_statement
        statement ::= procedural_continuous_assignments SEMICOLON
        statement ::= SEMICOLON
        '''

        return AST('single',[args[0]])

    def p_port_dec_more_in_items(self,args):
        '''
        module_items ::= module_items module_item
        module_items ::= 
        '''
        if len(args) >0 :
            return AST('Module_items',[args[0],args[1]])
        else :
            return AST('No More',[])
        pass

    def p_gen_single_or_not(self,args):
        '''
        ### dim_and_exp :  数组长度
        dor_dim_and_exp_opt ::= dor_dim_and_exp?
        '''
        if args[0] !=None:
            return AST('single',[args[0]])

    
    def p_gate_type(self,args):
        '''
        ## gatetype
        n_input_gatetype ::= AND
        n_input_gatetype ::= NAND
        n_input_gatetype ::= OR
        n_input_gatetype ::= NOR
        n_input_gatetype ::= XOR
        n_input_gatetype ::= XNOR
        n_output_gatetype ::= NOT
        '''
        return AST(args[0].name ,[args[0]] )

    def p_int_dec(self,args):
        '''
        integer_declaration ::= INTEGER list_of_variable_identifiers SEMICOLON
        '''
        return AST('INT',[args[1]])

    def p_net_wire_dec(self,args):
        '''
        net_declaration ::= WIRE signed_opt range_opt list_of_net_decl_assignments_or_identifiers SEMICOLON
        '''
        return AST('WIRE',[args[2],args[3]])

    def p_net_reg_dec(self,args):
        '''
        reg_declaration ::= REG signed_opt range_opt list_of_variable_identifiers SEMICOLON
        '''
        return AST('REG',[args[2],args[3],AST('dec_reg_flag',[None])])

    def p_net_wire_1(self,args):
        '''
        ## dor dimension and expression // line 67 
        ## list_of_net_decl_assignments_or_identifiers ::= net_identifier [ dor_dim_and_exp ] (COMMA net_identifier dor_dim_and_exp )*
        list_of_net_decl_assignments_or_identifiers ::= net_identifier dor_dim_and_exp_opt  COMMA_net_identifier_dor_dim_and_exps
        
        '''

        if(args[1]!=None):
            return AST('plex',[args[0],args[1]] )
        else :
            return AST('single',[args[0]])

    def p_dim_1(self,args):
        '''
        dor_dim_and_exp ::= dimension+
        dor_dim_and_exp ::= IS_EQUAL expression
        '''

        if len(args) == 1 :
            return AST('plex',[args[0]])
        else :
            return AST('EQUAL',[args[1]] )

    def p_dim_2(self,args):
        '''
        dimension ::= LBRACKET dimension_constant_expression COLON dimension_constant_expression RBRACKET
        '''
        return AST('dim',[args[1],args[3]])
    

    def p_list_var_1(self,args):
        '''
        ###(COMMA port_identifier [IS_EQUAL constant_expression])*
        list_of_variable_identifiers ::= port_identifier IS_EQUAL_constant_expression_opt COMMA_port_identifier_IS_EQUAL_constant_expression_opt_s
        '''
        ## ignore more commas
        if args[1].kind == 'None' :
            return AST('single',[args[0]])
        else :
            return AST('plex',[args[0],args[1]] )
    
    def p_list_var_1_1(self,args):
        '''
        COMMA_port_identifier_IS_EQUAL_constant_expression_opt_s ::= COMMA_port_identifier_IS_EQUAL_constant_expression_opt_s COMMA port_identifier  IS_EQUAL_constant_expression_opt
        COMMA_port_identifier_IS_EQUAL_constant_expression_opt_s ::= 
        '''
        if len(args) >0:
            return AST('more',[args[0],args[2],args[3]] )

    def p_list_var_2(self,args):
        '''
        IS_EQUAL_constant_expression_opt ::= IS_EQUAL constant_expression
        IS_EQUAL_constant_expression_opt ::=
        '''
        if len(args)>0 :
            return AST('EQUAL',[args[1]])
        else :
            return AST('None',[None])

    def p_assign_dec(self,args):
        '''
        continuous_assign ::= ASSIGN list_of_net_assignments SEMICOLON
        '''
        return AST('ASSIGN',[args[1]] )
    
    def p_assign_dec_1(self,args):
        '''
        list_of_net_assignments ::= net_assignment COMMA_net_assignments
        COMMA_net_assignments ::= COMMA_net_assignments COMMA net_assignment
        COMMA_net_assignments ::= 
        '''
        if len(args)==0 :
            return AST('None',None)
        elif len(args)== 3 :
            if args[1] !=None:
                return AST('More',[args[0],args[2]])
            else :
                return AST('single',[args[2]] )
        else :
            if args[1] !=None:
                return AST('More',[args[0],args[1]])
            else :
                return AST('single',[args[0]])
        pass

    def p_assign_dec_2(self,args):
        '''
        net_assignment ::= net_lvalue IS_EQUAL expression
        '''
        return AST('ASSIGN_2',[args[0],AST('LEFT_OVER',[None]), args[2],AST('ASSIGN_OVER',[None])])

    def p_assign_dec_3_0(self,args):
        '''
        net_lvalue ::= hierarchical_identifier_range_const
        net_lvalue ::= LBRACE net_lvalue COMMA_net_lvalues RBRACE	
        '''
        if len(args)==1:
            return AST('NET_LEFT',[args[0]] )
        else :
            return AST('COMBINE',[args[1],args[2],AST('COMBINE_OVER',[None])])

    def p_assign_dec_3_0_2(self,args):
        '''
        COMMA_net_lvalues ::= COMMA_net_lvalues COMMA net_lvalue
        COMMA_net_lvalues ::= 
        '''
        if len(args)==0:
            return AST('None',None)
        else :
            return AST('More',[args[0],args[2]])
    

    def p_exp_content_0(self,args):
        '''
        expression ::= unary_operator_opt primary  expression_nlrs
        '''
        # 目前忽略operator
        if args[1]=='single' and args[2].kind=='None' :
            return AST('single',[args[1]])
        else :
            return AST('EXPR',[args[1],args[2]])

    def p_primary_1(self,args):
        '''
        ##  primary ::= hierarchical_identifier_range   [ LPAREN expression (COMMA expression)* RPAREN ]
        primary ::= hierarchical_identifier_range   LPAREN_expression_COMMA_expressions_RPAREN_opt 
        LPAREN_expression_COMMA_expressions_RPAREN_opt ::= LPAREN expression COMMA_expressions RPAREN
        LPAREN_expression_COMMA_expressions_RPAREN_opt ::= 
        '''
        ## ignore args[1]
        if len(args)==0:
            return AST('None',None)
        else :
            if args[1].kind == 'None' :
                return AST('single',[args[0]])
            else :
                return AST('More',[args[0],args[1]])
    
    def p_hie_ident_range_1(self,args):
        '''
        ## hierarchical_identifier_range ::= identifier ( DOT identifier [ LBRACKET range_expression RBRACKET ]  |  LBRACKET range_expression RBRACKET   )*
        hierarchical_identifier_range ::= identifier great3_opt_s 
        
        '''
        if len(args)==2:
            if args[1].kind == 'None' :
                return AST('single',[args[0]])
            else :
                return AST('More',[args[0],args[1]])

    def p_hie_ident_range_1_2(self,args):
        '''
        great3_opt_s ::= great3_opt_s great3_opt_chosen
        great3_opt_s ::= 
        '''
        ##ignore more opts
        if len(args)==0:
            return AST('None',None)
        else :
            return AST('single',[args[1]])

    def p_hie_ident_range_2(self,args):
        '''
        great3_opt_chosen ::= LBRACKET range_expression RBRACKET
        great3_opt_chosen ::= DOT identifier LBRACKET_range_expression_RBRACKET_opt
        '''
        ## ignore .ident
        if len(args)==3:
            return AST('RANGE_BIND',[args[1]])

    def p_hie_ident_range_2_2(self,args):
        '''
        range_expression ::= NUMBER COLON NUMBER
        '''
        ##dor DIY: range_expression
        return AST('plex',[args[0],args[2]])


    def p_hie_ident_range_const_1(self,args):
        '''
        hierarchical_identifier_range_const ::= identifier LBRACKET_constant_range_expression_RBRACKETs
        LBRACKET_constant_range_expression_RBRACKETs ::= LBRACKET_constant_range_expression_RBRACKETs LBRACKET constant_range_expression RBRACKET
        LBRACKET_constant_range_expression_RBRACKETs ::= 
        '''
        if len(args)==0:
            return AST('None',[])
        elif len(args)==2:
            return AST('ident_and_range',[args[0],args[1]])
        else:
            return AST('More',[args[0],args[2]])

    def p_const_range_exp(self,args):
        '''
        constant_range_expression ::= constant_expression COLON_lsb_constant_expression_opt
        '''
        return AST('RANGE',[args[0],args[1]] )


    def p_const_range_exp_1(self,args):
        '''
        COLON_lsb_constant_expression_opt ::= COLON lsb_constant_expression
        COLON_lsb_constant_expression_opt ::=
        '''
        if len(args)==0:
            return AST('None',[])
        else:
            return AST('More',[args[1]])

    def p_exp_nlr_1(self,args):
        '''
        expression_nlrs ::= expression_nlrs expression_nlr
        expression_nlrs ::= 
        '''
        if len(args)==0:
            return AST('None',[])
        else:
            return AST('More',[args[0],args[1]])
    
    def p_exp_nlr_2(self,args):
        '''
        expression_nlr ::=  binary_operator expression
        expression_nlr ::=  QUES expression COLON expression
        '''
        if len(args)==2:
            return AST('UNION',[args[0],args[1],AST('do_cal',[None])])
        else:
            return AST('Ques',[args[1],args[3]])

    def p_binary(self,args):
        '''
        binary_operator ::= BINOP
        binary_operator ::= PLUS
        binary_operator ::= MINUS
        '''
        return AST('cal_op',[args[0]])

    def p_always_top(self,args):
        '''
        always_construct ::= ALWAYS statement
        '''
        return AST('ALWAYS',[args[1]])

    def p_stmt_1(self,args):
        '''
        statement ::= procedural_timing_control_statement
        '''
        return AST('Time_control',[args[0]])

    def p_stmt_1_1(self,args):
        '''
        procedural_timing_control_statement ::= event_control statement_or_null
        '''
        return AST('Time_control_1',[args[0],args[1]])

    def p_always_top_1(self,args):
        '''
        event_control ::= AT LPAREN event_expression RPAREN

        ##dor!!! STAR must be caution
        event_control ::= AT LPAREN BINOP RPAREN
        event_control ::= AT BINOP
        '''
        if len(args)>2:
            return AST('Trigger',[args[2],AST('TriggerEnd',[None])])
        return AST('Trigger_any',[None])

    def p_m_g_items(self,args):
        '''
        module_or_generate_items ::= module_or_generate_items module_or_generate_item
        module_or_generate_items ::= 

        statements ::= statements statement
        statements ::= 
        '''
        if len(args)>0:
            return AST('More',[args[0],args[1]])

    def p_single_opt(self,args):
        '''
        statement_or_null ::= statement?
        expression_opt ::= expression?
        '''
        if len(args)>0 :
            return AST('single',[args[0]])

    def p_stmt_2(self,args):
        '''
        statement ::= seq_block
        '''
        return AST('single',[args[0]])

    def p_seq_block(self,args):
        '''
        ## [COLON block_identifier block_item_declaration* ]
        seq_block ::= BEGIN statements END
        '''
        return AST('BLOCK',[args[1]])

    def p_event_expr(self,args):
        '''
        event_expression ::= POSEDGE expression
        '''
        return AST('posedge',[args[1]])

    def p_block_assign(self,args):
        '''
        ##  great ->    [LPAREN expression (COMMA expression)*   RPAREN] ['<=' [delay_or_event_control] [expression] ] 
        blocking_assignment ::= variable_lvalue  great2_opt SEMICOLON
        '''
        if len(args)>0:
            return AST('BLOCK_ASSIGN',[args[0],AST('B_LEFT_OVER',[None]) , args[1]])

    def p_block_assign_1(self,args):
        '''
        ##dor COMP_OP MUSTbe '<=' ?
        great2_opt ::= COMP_OP  expression_opt
        great2_opt ::= IS_EQUAL  expression_opt
        great2_opt ::= 
        '''
        if len(args)>0:
            return AST('More',[args[1]])
        

    def p_if_Enable(self,args):
        '''
        conditional_statement  ::= IF LPAREN expression RPAREN statement_or_null ELSE_statement_or_null_opt
        '''
        return AST('enable',[args[2],args[4],AST('enableEnd',[None])])

    def p_var_left(self,args):
        '''
        variable_lvalue ::= hierarchical_identifier_range
        variable_lvalue ::= LBRACE variable_lvalue COMMA_variable_lvalues RBRACE
        '''
        if len(args)>1:
            return AST('More',[args[0],args[1]])
        else :
            return AST('single',[args[0]])

    
    def p_python_grammar(self, args):
        ''' 
        conditional_generate_construct ::= if_generate_construct
        conditional_generate_construct ::= case_generate_construct

        if_generate_construct ::= IF LPAREN constant_expression RPAREN  generate_block_or_null ELSE_generate_block_or_null_opt
        ELSE_generate_block_or_null_opt ::= ELSE generate_block_or_null
        ELSE_generate_block_or_null_opt ::= 
        case_generate_construct ::= CASE LPAREN constant_expression RPAREN  case_generate_item case_generate_item* ENDCASE

        case_generate_item ::= constant_expression COMMA_constant_expressions COLON generate_block_or_null
        COMMA_constant_expressions ::= COMMA_constant_expressions COMMAconstant_expression
        COMMA_constant_expressions ::= 
        case_generate_item ::= DEFAULT COLON generate_block_or_null

        COLON_generate_block_identifier_opt ::= COLON generate_block_identifier
        generate_block ::= BEGIN COLON_generate_block_identifier_opt module_or_generate_items END 

        generate_block_or_null ::= generate_block
        generate_block_or_null ::= module_or_generate_item
        generate_block_or_null ::= SEMICOLON
        
        procedural_continuous_assignments ::= ASSIGN variable_assignment
        variable_assignment ::= variable_lvalue IS_EQUAL expression
        
        COMMA_expressions ::= COMMA_expressions COMMA expression
        COMMA_expressions ::= 

        case_statement  ::= CASE LPAREN expression RPAREN case_item+ ENDCASE    

        ## case item
        case_item ::= expression COMMA_expressions  COLON statement_or_null
        COMMA_expression_s ::= COMMA_expression_s COMMA expression

        case_item ::= DEFAULT COLON? statement_or_null

        loop_statement ::= FOR LPAREN variable_assignment SEMICOLON expression SEMICOLON variable_assignment RPAREN statement   
        
        constant_expression_nlrs ::= constant_expression_nlrs binary_operator constant_expression
        constant_expression_nlrs ::=    
        
        ### constant_primary ::= string

        ##dor ident_or_sysname 
        ## constant_primary ::= dor_ident_or_sysname [ LBRACKET constant_range_expression RBRACKET ]
        constant_primary ::= dor_ident_or_sysname  LBRACKET_constant_range_expression_RBRACKET_opt 
        LBRACKET_constant_range_expression_RBRACKET_opt ::= LBRACKET constant_range_expression RBRACKET
        LBRACKET_constant_range_expression_RBRACKET_opt ::= 

        ## constant_primary ::= dor_ident_or_sysname [ LPAREN constant_expression { COMMA constant_expression } RPAREN ]
        constant_primary ::= dor_ident_or_sysname LPAREN_constant_expression_COMMA_constant_expressions_RPAREN_opt
        LPAREN_constant_expression_COMMA_constant_expressions_RPAREN_opt ::= LPAREN constant_expression COMMA_constant_expressions RPAREN
        LPAREN_constant_expression_COMMA_constant_expressions_RPAREN_opt ::=

        dor_ident_or_sysname ::=  identifier
        dor_ident_or_sysname ::=  system_name

        ## constant_primary ::= LBRACE constant_expression [ COMMA constant_expression (COMMA constant_expression )* ] RBRACE
        constant_primary ::= LBRACE constant_expression COMMA_constant_expression_COMMA_constant_expressions_opt RBRACE
        COMMA_constant_expression_COMMA_constant_expressions_opt ::= COMMA constant_expression COMMA_constant_expressions
        ## constant_primary ::= LBRACE constant_expression [ LBRACE constant_expression (COMMA constant_expression )* RBRACE ] RBRACE
        constant_primary ::= LBRACE constant_expression LBRACE_constant_expression_COMMA_constant_expressions_RBRACE_opt RBRACE
        LBRACE_constant_expression_COMMA_constant_expressions_RBRACE_opt ::= LBRACE constant_expression COMMA_constant_expressions

        COMMA_constant_expressions ::=  COMMA_constant_expressions COMMA constant_expression
        COMMA_constant_expressions ::= 

        primary ::= number
        ### primary ::= string
        ## primary ::= LBRACE expression [ COMMA expression (COMMA expression)* ] RBRACE
        primary ::= LBRACE expression COMMA_expression_COMMA_expressions_opt RBRACE
        COMMA_expression_COMMA_expressions_opt ::= COMMA expression COMMA_expressions
        COMMA_expression_COMMA_expressions_opt ::= 

        ## primary ::= LBRACE expression [ LBRACE expression (COMMA expression)* RBRACE ] RBRACE
        primary ::= LBRACE expression LBRACE_expression_COMMA_expressions_RBRACE_opt RBRACE
        LBRACE_expression_COMMA_expressions_RBRACE_opt ::= LBRACE expression COMMA_expressions RBRACE
        LBRACE_expression_COMMA_expressions_RBRACE_opt ::= 

        ## hierarchical_identifier_range_const ::= identifier (DOT identifier [ LBRACKET constant_range_expression RBRACKET ] )*
        hierarchical_identifier_range_const ::= identifier DOT_identifier_LBRACKET_constant_range_expression_RBRACKET_opt_s
        DOT_identifier_LBRACKET_constant_range_expression_RBRACKET_opt_s ::= DOT_identifier_LBRACKET_constant_range_expression_RBRACKET_opt_s DOT identifier LBRACKET_constant_range_expression_RBRACKET_opt
        DOT_identifier_LBRACKET_constant_range_expression_RBRACKET_opt_s ::= 
        LBRACKET_constant_range_expression_RBRACKET_opt ::= LBRACKET constant_range_expression RBRACKET

        
        COMMA_variable_lvalues ::= COMMA_variable_lvalues COMMA variable_lvalue
        COMMA_variable_lvalues ::= 

        variable_or_net_lvalue ::= hierarchical_identifier_range
        ## variable_or_net_lvalue ::= LBRACE variable_or_net_lvalue (COMMA variable_or_net_lvalue)* RBRACE
        variable_or_net_lvalue ::= LBRACE variable_or_net_lvalue COMMA_variable_or_net_lvalues RBRACE
        COMMA_variable_or_net_lvalues ::= COMMA_variable_or_net_lvalues COMMA variable_or_net_lvalue
        COMMA_variable_or_net_lvalues ::=

        # number ::= natural_number based_number?
        # number ::= natural_number base_format_base_value_opt
        # base_format_base_value_opt ::= base_format base_value

        ##dor: now cant resolve base_value and base_number 
        ## number ::= natural_number [base_format natural_number ]
        
        # number ::= sizedbased_number
        # number ::= based_number

        # ## number ::= base_format base_value
        # number ::= base_format natural_number

        based_number ::= NUMBER
        base_value ::= NUMBER
        ## value is 1 0 x z
        sizedbased_number ::= SIZE_NUMBER
        base_format ::= SIZE_NUMBER

        ## list_of_variable_port_identifiers ::= port_identifier [ IS_EQUAL constant_expression ]  (COMMA port_identifier [ IS_EQUAL constant_expression ])*
        list_of_variable_port_identifiers ::= port_identifier IS_EQUAL_constant_expression_opt COMMA_port_identifier_IS_EQUAL_constant_expression_opts
        IS_EQUAL_constant_expression_opt ::= IS_EQUAL constant_expression
        IS_EQUAL_constant_expression_opt ::= 
        COMMA_port_identifier_IS_EQUAL_constant_expression_opts ::= COMMA port_identifier IS_EQUAL_constant_expression_opt
        COMMA_port_identifier_IS_EQUAL_constant_expression_opts ::=

        dimension_constant_expression ::= constant_expression 
        
        unary_operator_opt ::= unary_operator
        unary_operator_opt ::= 

        generate_block_identifier ::= identifier
        unary_operator ::= PLUS
        unary_operator ::= MINUS
        unary_operator ::= QUES

        ## tmp cannot semantic -----
        ### generate
        generate_region ::= GENERATE module_or_generate_item* ENDGENERATE
        genvar_declaration ::= GENVAR list_of_genvar_identifiers SEMICOLON

        # list_of_genvar_identifiers ::= genvar_identifier (COMMA genvar_identifier)* 
        loop_generate_construct ::= FOR LPAREN genvar_initialization SEMICOLON genvar_expression SEMICOLON genvar_iteration RPAREN generate_block
        loop_generate_construct ::= FOR LPAREN genvar_initialization SEMICOLON genvar_expression SEMICOLON genvar_iteration RPAREN module_or_generate_item
        genvar_initialization ::= genvar_identifier IS_EQUAL constant_expression

        genvar_expression ::= unary_operator? genvar_primary genvar_expression_nlr

        genvar_expression_nlr ::= binary_operator genvar_expression genvar_expression_nlr
        genvar_expression_nlr ::= QUES genvar_expression COLON genvar_expression genvar_expression_nlr
        genvar_expression_nlr ::= 

        genvar_iteration ::= genvar_identifier IS_EQUAL genvar_expression
        genvar_primary ::= constant_primary

        ### gatetype
        gate_instantiation ::= n_input_gatetype n_input_gate_instance COMMA_n_input_gate_instances SEMICOLON
        COMMA_n_input_gate_instances ::= COMMA_n_input_gate_instances COMMA n_input_gate_instance
        COMMA_n_input_gate_instances ::= 

        gate_instantiation ::= n_output_gatetype n_output_gate_instance COMMA_n_output_gate_instances SEMICOLON
        COMMA_n_output_gate_instances ::= COMMA_n_output_gate_instances COMMA n_output_gate_instances
        COMMA_n_output_gate_instances ::= 

        n_input_gate_instance ::= name_of_gate_instance_opt LPAREN output_terminal COMMA input_terminal COMMA_input_terminals RPAREN
        name_of_gate_instance_opt ::= name_of_gate_instance?
        COMMA_input_terminals ::= COMMA_input_terminals COMMA input_terminal
        COMMA_input_terminals ::= 

        n_output_gate_instance ::= name_of_gate_instance_opt LPAREN input_or_output_terminal COMMA_input_or_output_terminals RPAREN
        COMMA_input_or_output_terminals ::= COMMA_input_or_output_terminals COMMA input_or_output_terminal
        COMMA_input_or_output_terminals ::= 

        input_terminal ::= expression
        #### dor :dont dnow expression_2
        ##### input_or_output_terminal ::= expression_2
        input_or_output_terminal ::= expression

        name_of_gate_instance ::= gate_instance_identifier LBRACKET range RBRACKET

        port_opt ::= port
        port_opt ::=
        port_expression_opt ::= port_expression?

        ## (COMMA port_reference)*
        comma_port_references ::= comma_port_references COMMA port_reference
        comma_port_references ::=
        wire_opt ::= WIRE?
        signed_opt ::= SIGNED?

        COMMA_net_identifier_dor_dim_and_exps ::= COMMA_net_identifier_dor_dim_and_exps COMMA net_identifier dor_dim_and_exp
        COMMA_net_identifier_dor_dim_and_exps ::= 

        ELSE_statement_or_null_opt ::= ELSE statement_or_null
        ELSE_statement_or_null_opt ::= 
    '''



def parse_VeriSim(VeriSim_tokens, start='translation_unit',
                  show_tokens=False, parser_debug=DEFAULT_DEBUG, check=False):
    assert isinstance(VeriSim_tokens, list)
    if show_tokens:
        for t in VeriSim_tokens:
            print(t)

    # For heavy grammar debugging:
    # parser_debug = {'rules': True, 'transition': True, 'reduce': True,
    #               'errorstack': 'full', 'context': True, 'dups': True}
    # Normal debugging:
    # parser_debug = {'rules': False, 'transition': False, 'reduce': True,
    #                'errorstack': 'full', 'context': True, 'dups': True}
    parser = VeriSimParser(start=start, debug=parser_debug)
    if check:
        parser.check_grammar()
    return parser.parse(VeriSim_tokens)


if __name__ == '__main__':
    # if len(sys.argv) == 1:
    #     for python2_stmts in (
    #             """return f()""",
    #             ):
    #         print(python2_stmts)y
    #         print('-' * 30)
    #         ast = parse_VeriSim(python2_stmts + ENDMARKER,
    #                             start='translation_unit', show_tokens=False, check=True)
    #         print(ast)
    #         print(IS_EQUAL * 30)
    # else:
    #     python2_stmts = " ".join(sys.argv[1:])
    #     parse_VeriSim(python2_stmts, show_tokens=False, check=True)
    src = open('adder.v')
    scan = VeriSimScanner()
    tokens = scan.tokenize(src.read() + ENDMARKER)
    ast = parse_VeriSim(tokens, start='translation_unit', show_tokens=False, check=False)
    print(ast)
    print("DORMOUSE+==========parse +end")
