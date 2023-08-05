from lark import Lark, Transformer
import _ast
from pathlib import Path
import astor
import sys


class TythonTransformer(Transformer):
    def start(self, items):
        return _ast.Module(body=items)
    
    def stmts(self, items):
        (items,) = items
        return items
    
    def class_structure(self, items):
        (name,body) = items
        
        return _ast.ClassDef(name=name, body=body, decorator_list=[], bases=[])
    
    def class_body(self, items):
        return items

    def field(self, items):
        (identifier,_type) = items[0]
        return _ast.AnnAssign(target=_ast.Name(id=identifier), annotation=_ast.Name(id=_type), value=None, simple=True)

    def class_declarations(self, items):
        (items,) = items
        return items
    
    def constructor_method(self, items):
        (args,body) = items
        
        method_args = [_ast.arg(arg='self', annotation=None)]
        method_args.extend(args)
        
        return _ast.FunctionDef(name='__init__', args=_ast.arguments(args=method_args, defaults=[], vararg=None, kwarg=None), body=body, decorator_list=[])
    
    def function(self, items):
        (name,args,body) = items
        return _ast.FunctionDef(name=name, args=_ast.arguments(args=args, defaults=[], vararg=None, kwarg=None), body=body, decorator_list=[])

    def constructor_args(self, items):
        return items
    
    def func_args(self, items):
        return self.constructor_args(items)

    def public_arg(self, items):
        # TODO: sort out public later
        (items,) = items
        return items
    
    def func_arg(self, items):
        (items,) = items
        identifier = items[0]
        if len(items) == 2:
            type_ = items[1]
        else:
            type_ = None
        
        return _ast.arg(arg=identifier, annotation=type_)
    
    def func_body(self, items):
        return items
    
    def func_stmts(self, items):
        (items,) = items
        return items
    
    def reassign(self, items):
        (attrs,val,_) = items
        
        return _ast.Assign(targets=[attrs], value=val)
    
    def this_dotted_access(self, items):
        (items,) = items
        return _ast.Attribute(value=_ast.Name(id='self'), attr=items)

    def ret_expr(self, items):
        (items,) = items
        return items

    def return_expr(self, items):
        (items,) = items
        return _ast.Return(value=items)
    
    def expr(self, items):
        (items,) = items
        return items
    
    def add(self, items):
        (left,right) = items
        return _ast.BinOp(left=left, op=_ast.Add(), right=right)

    def access(self, items):
        (items,) = items
        return _ast.Name(id=items)
    
    def dotted_access(self, items):
        attr = None
        for item in items:
            if attr is None:
                attr = item
                continue
            attr = _ast.Attribute(value=attr, attr=item.id)
        return attr
    
    def types_repr(self, items):
        (items,) = items
        return items
    
    def str(self, items):
        (items,) = items
        items = items[1:-1]
        return _ast.Constant(value=items)

    def explicit_type(self, items):
        (identifier, _type) = items
        return identifier, _type

    def string(self, items):
        return _ast.Name(id='str')
    
    def object(self, items):
        (items,) = items
        return _ast.Name(id=items)

    def identifier(self, items):
        (identifier,) = items
        return str(identifier)

    def var(self, items):
        (_,identifier,expr,_) = items
        return _ast.Assign(targets=[_ast.Name(identifier)], value=expr)
    
    def new_class(self, items):
        (identifier,args) = items
        return _ast.Call(func=_ast.Name(id=identifier), args=args, keywords=[])
    
    def function_call(self, items):
        return self.new_class(items)
    
    def call_args(self, items):
        return items
    
    def call_arg(self, items):
        (items,) = items
        return items
    
    def terminator(self, items):
        return

    def interface(self, items):
        return self.class_structure(items)
    
    def interface_body(self, items):
        return self.class_body(items)
    
    def interface_declarations(self, items):
        return self.class_declarations(items)
    
    def interface_declaration(self, items):
        return self.field(items)

grammar = Path(__file__).parent.joinpath('grammar.lark')
parser = Lark.open(grammar)

if len(sys.argv) > 1:
    feed_in = sys.argv[1]
    tree = parser.parse(open(feed_in).read())

    program = TythonTransformer().transform(tree)
    code = astor.to_source(program)
    print(code)
