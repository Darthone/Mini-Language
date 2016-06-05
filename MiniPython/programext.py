#!/usr/bin/python
#
# exp.py - Classes to represent underlying data structures for the grammar
#    below, for the mini-compiler.
#
# Kurt Schmidt
# 8/07
#
# DESCRIPTION:
#       Just a translation of the C++ implementation by Jeremy Johnson (see
#       programext.cpp)
#
# EDITOR: cols=80, tabstop=2
#
# NOTES
#   environment:
#       a dict
#
#       Procedure calls get their own environment, can not modify enclosing env
#
#   Grammar:
#       program: stmt_list 
#       stmt_list:  stmt ';' stmt_list 
#           |   stmt  
#       stmt:  assign_stmt 
#           |  define_stmt 
#           |  if_stmt 
#           |  for_stmt 
#           |  class_stmt 
#           |  class_inherit_stmt 
#           |  while_stmt 
#       assign_stmt: IDENT ASSIGNOP expr
#       define_stmt: DEFINE IDENT PROC '(' param_list ')' stmt_list END
#       if_stmt: IF expr THEN stmt_list ELSE stmt_list FI
#       for_stmt: FOR assign_stmt ';' expr  ';' assign_stmt DO stmt_list OD
#       class_stmt: CLASS IDENT '(' param_list ')' stmt_list END
#       class_inherit_stmt: CLASS IDENT '(' param_list ')' ':' IDENT stmt_list END
#       while_stmt: WHILE expr DO stmt_list OD
#       param_list: IDENT ',' param_list 
#           |      IDENT 
#       expr: expr '+' term   
#           | expr '-' term   
#           | term            
#       term: term '*' factor   
#           | term '^' factor   
#           | factor            
#       factor:     '(' expr ')'  
#           |       NUMBER 
#           |       IDENT 
#           |       funcall 
#       funcall:  IDENT '(' expr_list ')'
#       expr_list: expr ',' expr_list 
#           |      expr 
#

import sys

####  CONSTANTS   ################

    # the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

######   CLASSES   ##################

class Expr :
    '''Virtual base class for expressions in the language'''

    def __init__( self ) :
        raise NotImplementedError(
            'Expr: pure virtual base class.  Do not instantiate' )

    def eval( self, nt, ft, ct ) :
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Expr.eval: virtual method.  Must be overridden.' )

    def display( self, nt, ft, ct, depth=0 ) :
        'For debugging.'
        raise NotImplementedError(
            'Expr.display: virtual method.  Must be overridden.' )

class Number( Expr ) :
    '''Just integers'''

    def __init__( self, v=0 ) :
        self.value = v
    
    def eval( self, nt, ft, ct ) :
        return self.value

    def display( self, nt, ft, ct, depth=0 ) :
        print "%s%i" % (tabstop*depth, self.value)

class Ident( Expr ) :
    '''Stores the symbol'''

    def __init__( self, name ) :
        self.name = name
    
    def eval( self, nt, ft, ct ) :
        return nt[ self.name ]

    def display( self, nt, ft, ct, depth=0 ) :
        print "%s%s" % (tabstop*depth, self.name)


class LessThan( Expr ) :
    '''expression for binary less than'''
    def __init__ ( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, ct ) :
        if self.lhs.eval( nt, ft, ct ) < self.rhs.eval( nt, ft, ct) :
            return 1
        else :
            return 0

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sLESSTHAN" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )

class GreaterThan( Expr ) :
    '''expression for binary greater than'''
    def __init__ ( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, ct ) :
        if self.lhs.eval( nt, ft, ct ) > self.rhs.eval( nt, ft, ct) :
            return 1
        else :
            return 0

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sGREATERTHAN" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )


class LessEqual( Expr ) :
    '''expression for binary less than or equal'''
    def __init__ ( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, ct ) :
        if self.lhs.eval( nt, ft, ct ) <= self.rhs.eval( nt, ft, ct) :
            return 1
        else :
            return 0

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sLESSEQUAL" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )

class GreaterEqual( Expr ) :
    '''expression for binary greater than or equal'''
    def __init__ ( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, ct ) :
        if self.lhs.eval( nt, ft, ct ) >= self.rhs.eval( nt, ft, ct) :
            return 1
        else :
            return 0

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sGREATEREQUAL" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )

class Equal( Expr ) :
    '''expression for binary equal'''
    def __init__ ( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, ct ) :
        if self.lhs.eval( nt, ft, ct ) == self.rhs.eval( nt, ft, ct) :
            return 1
        else :
            return 0

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sEQUAL" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )

class NotEqual( Expr ) :
    '''expression for binary greater not equal'''
    def __init__ ( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        self.lhs = lhs
        self.rhs = rhs

    def eval( self, nt, ft, ct ) :
        if self.lhs.eval( nt, ft, ct ) != self.rhs.eval( nt, ft, ct) :
            return 1
        else :
            return 0

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sGREATERTHAN" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )

class Times( Expr ) :
    '''expression for binary multiplication'''

    def __init__( self, lhs, rhs ) :
        '''lhs, rhs are Expr's, the operands'''

        # test type here?
        # if type( lhs ) == type( Expr ) :
        self.lhs = lhs
        self.rhs = rhs
    
    def eval( self, nt, ft, ct ) :
        return self.lhs.eval( nt, ft, ct ) * self.rhs.eval( nt, ft, ct )

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sMULT" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )
        #print "%s= %i" % (tabstop*depth, self.eval( nt, ft, ct ))


class Plus( Expr ) :
    '''expression for binary addition'''

    def __init__( self, lhs, rhs ) :
        self.lhs = lhs
        self.rhs = rhs
    
    def eval( self, nt, ft, ct ) :
        return self.lhs.eval( nt, ft, ct ) + self.rhs.eval( nt, ft, ct )

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sADD" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )
        #print "%s= %i" % (tabstop*depth, self.eval( nt, ft, ct ))


class Minus( Expr ) :
    '''expression for binary subtraction'''

    def __init__( self, lhs, rhs ) :
        self.lhs = lhs
        self.rhs = rhs
    
    def eval( self, nt, ft, ct ) :
        return self.lhs.eval( nt, ft, ct ) - self.rhs.eval( nt, ft, ct )

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sSUB" % (tabstop*depth)
        self.lhs.display( nt, ft, ct, depth+1 )
        self.rhs.display( nt, ft, ct, depth+1 )
        #print "%s= %i" % (tabstop*depth, self.eval( nt, ft, ct ))


class FunCall( Expr ) :
    '''stores a function call:
      - its name, and arguments'''
    
    def __init__( self, name, argList ) :
        self.name = name
        self.argList = argList
    
    def eval( self, nt, ft, ct ) :
        return ft[ self.name ].apply( nt, ft, ct, self.argList )

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sFunction Call: %s, args:" % (tabstop*depth, self.name)
        for e in self.argList :
            e.display( nt, ft, ct, depth+1 )

#------------------------------------------------------

class List :
    '''Virtual base class for lists in the language'''

    def __init__( self, cont ) :
        raise NotImplementedError(
                'List: pure virtual base class.  Do not instantiate' )

    def eval( self, nt, ft, ct ) :
        return NotImplementedError(
                'List: pure virtual base class.  Must be overwritten' )

class ListStuff() :
    def __init__( self, cont ) :
        self.cont = cont
    def eval(self, nt, ft, ct ) :
        A =[]
        for x in self.cont:
            A.append( x.eval(nt,ft) )
        return A
class NonEmptyList() :
    '''expression to return non-empty list'''
    def __init__( self, cont ) :
        self.cont = cont

    def eval( self, nt, ft, ct ) :
        return self.cont

class EmptyList() :
    '''expression to return empty list'''
    def __init__( self ) :
        self.cont = []
    def eval( self, nt, ft, ct ) :
        return self.cont

class Car( List ) :
    '''expression for car'''
    def __init__( self, cont ) :
        self.cont = cont

    def eval( self, nt, ft, ct ) :
        A = self.cont.eval(nt,ft)
        return A[0]

class Cdr( List ) :
    '''expression for cdr'''
    def __init__( self, cont ) :
        self.cont = cont

    def eval( self, nt, ft, ct ) :
        A = self.cont.eval(nt, ft, ct)
        return A[1:]

class Cons( Expr, List ) :
    '''expression for cons'''
    def __init__( self, v, cont ) :
        self.val = v
        self.cont = cont

    def eval( self, nt, ft, ct ) :
        A = self.cont.eval(nt, ft, ct)
        B = self.val.eval(nt, ft, ct)
        return A.insert(0, B)

class Null ( List ) :
    '''expression for null'''
    def __init__( self, cont ) :
        self.cont = cont

    def eval( self, nt, ft, ct ) :
        A = self.cont.eval(nt, ft, ct)
        if not A :
            return 1
        else :
            return 0


#-------------------------------------------------------

class Stmt :
    '''Virtual base class for statements in the language'''

    def __init__( self ) :
        raise NotImplementedError(
            'Stmt: pure virtual base class.  Do not instantiate' )

    def eval( self, nt, ft, ct ) :
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Stmt.eval: virtual method.  Must be overridden.' )

    def display( self, nt, ft, ct, depth=0 ) :
        'For debugging.'
        raise NotImplementedError(
            'Stmt.display: virtual method.  Must be overridden.' )


class AssignStmt( Stmt ) :
    '''adds/modifies symbol in the current context'''

    def __init__( self, name, rhs ) :
        '''stores the symbol for the l-val, and the expressions which is the
        rhs'''
        self.name = name
        self.rhs = rhs
    
    def eval( self, nt, ft, ct ) :
        nt[ self.name ] = self.rhs.eval( nt, ft, ct )

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sAssign: %s :=" % (tabstop*depth, self.name)
        self.rhs.display( nt, ft, ct, depth+1 )


class DefineStmt( Stmt ) :
    '''Binds a proc object to a name'''

    def __init__( self, name, proc ) :
        self.name = name
        self.proc = proc

    def eval( self, nt, ft, ct ) :
        ft[ self.name ] = self.proc

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sDEFINE %s :" % (tabstop*depth, self.name)
        self.proc.display( nt, ft, ct, depth+1 )


class IfStmt( Stmt ) :

    def __init__( self, cond, tBody, fBody ) :
        '''expects:
        cond - expression (integer)
        tBody - StmtList
        fBody - StmtList'''
        
        self.cond = cond
        self.tBody = tBody
        self.fBody = fBody

    def eval( self, nt, ft, ct ) :
        if self.cond.eval( nt, ft, ct ) > 0 :
            self.tBody.eval( nt, ft, ct )
        else :
            self.fBody.eval( nt, ft, ct )

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sIF" % (tabstop*depth)
        self.cond.display( nt, ft, ct, depth+1 )
        print "%sTHEN" % (tabstop*depth)
        self.tBody.display( nt, ft, ct, depth+1 )
        print "%sELSE" % (tabstop*depth)
        self.fBody.display( nt, ft, ct, depth+1 )

class Elifstmt( Stmt ) :
	
	def __init__( self, cond, tBody, fBody) :
		self.cond = cond
		self.tBody = tBody
		self.fBody = fBody

	def eval( self, nt, ft ) :
		if self.cond.eval( nt, ft ) > 0 :
			self.tBody.eval( nt, ft )
		else:
			self.fBody.eval( nt, ft)
	def display( self, nt, ft, depth=0 ) :
		print "%sELIF" % (tabstop*depth)
		self.cond.display( nt, ft, depth+1) 
		print "%sTHEN" % (tabstop*depth)
		self.tBody.display( nt, ft, depth+1 )
		self.fBody.display( nt, ft, depth+1 )


class WhileStmt( Stmt ) :

    def __init__( self, cond, body ) :
        self.cond = cond
        self.body = body

    def eval( self, nt, ft, ct ) :
        while self.cond.eval( nt, ft, ct ) > 0 :
            self.body.eval( nt, ft, ct )

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sWHILE" % (tabstop*depth)
        self.cond.display( nt, ft, ct, depth+1 )
        print "%sDO" % (tabstop*depth)
        self.body.display( nt, ft, ct, depth+1 )

class ForStmt( Stmt ) :

    def __init__( self, assign, cond, inc, body ) :
        self.assing = assign
        self.cond = cond
        self.inc = inc
        self.body = body

    def eval( self, nt, ft, ct ) :
        self.assing.eval(nt, ft, ct)
        while self.cond.eval( nt, ft, ct ) > 0 :
            self.body.eval( nt, ft, ct )
            self.inc.eval(nt, ft, ct)

    def display( self, nt, ft, ct, depth=0 ) :
        print "%sFOR" % (tabstop*depth)
        self.assing.display(nt, ft, ct, depth+1)
        self.cond.display( nt, ft, ct, depth+1 )
        self.inc.display( nt, ft, ct, depth+1 )
        print "%sDO" % (tabstop*depth)
        self.body.display( nt, ft, ct, depth+1 )

#-------------------------------------------------------
class ClassStmt( Stmt ):
    def __init__(self, ident, paramList, body):
        self.name = ident
        self.paramList = paramList
        self.body = body

    def eval( self, nt, ft, ct ) :
        ct[ self.name ] = self.body

    def display(self, nt, ft, ct):
        pass


class StmtList :
    '''builds/stores a list of Stmts'''

    def __init__( self ) :
        self.sl = []
    
    def insert( self, stmt ) :
        self.sl.insert( 0, stmt )
    
    def eval( self, nt, ft, ct ) :
        for s in self.sl :
            s.eval( nt, ft, ct )
    
    def display( self, nt, ft, ct, depth=0 ) :
        print "%sSTMT LIST" % (tabstop*depth)
        for s in self.sl :
            s.display( nt, ft, ct, depth+1 )


class Proc :
    '''stores a procedure (formal params, and the body)

    Note that, while each function gets its own environment, we decided not to
    allow side-effects, so, no access to any outer contexts.  Thus, nesting
    functions is legal, but no different than defining them all in the global
    environment.  Further, all calls are handled the same way, regardless of
    the calling environment (after the actual args are evaluated); the proc
    doesn't need/want/get an outside environment.'''

    def __init__( self, paramList, body ) :
        '''expects a list of formal parameters (variables, as strings), and a
        StmtList'''

        self.parList = paramList
        self.body = body

    def apply( self, nt, ft, ct, args ) :
        newContext = {}

        # sanity check, # of args
        if len( args ) is not len( self.parList ) :
            print "Param count does not match:"
            sys.exit( 1 )

        # bind parameters in new name table (the only things there right now)
            # use zip, bastard
        for i in range( len( args )) :
            newContext[ self.parList[i] ] = args[i].eval( nt, ft, ct )

        # evaluate the function body using the new name table and the old (only)
        # function table.  Note that the proc's return value is stored as
        # 'return in its nametable

        self.body.eval( newContext, ft )
        if newContext.has_key( returnSymbol ) :
            return newContext[ returnSymbol ]
        else :
            print "Error:  no return value"
            sys.exit( 2 )
    
    def display( self, nt, ft, ct, depth=0 ) :
        print "%sPROC %s :" % (tabstop*depth, str(self.parList))
        self.body.display( nt, ft, ct, depth+1 )


class Program :
    
    def __init__( self, stmtList ) :
        self.stmtList = stmtList
        self.nameTable = {}
        self.funcTable = {}
        self.classTable = {}
    
    def eval( self ) :
        self.stmtList.eval( self.nameTable, self.funcTable, self.classTable )
    
    def dump( self ) :
        print "Dump of Symbol Table"
        print "Name Table"
        for k in self.nameTable :
            print "  %s -> %s " % ( str(k), str(self.nameTable[k]) )
        print "Function Table"
        for k in self.funcTable :
            print "  %s" % str(k)

    def display( self, depth=0 ) :
        print "%sPROGRAM :" % (tabstop*depth)
        self.stmtList.display( self.nameTable, self.funcTable, self.classTable )


n = Plus( Number(17), Number(25) )
l = [ n ]
nt = {}
ft = {}
ct = {}
result = [ i.eval( nt, ft, ct ) for i in l ]
print result

