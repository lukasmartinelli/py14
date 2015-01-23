import ast


class CLikeTranspiler(ast.NodeVisitor):
    """Provides a base for C-like programming languages"""

    def visit_Name(self, node):
        if node.id == 'True':
            return 'true'
        elif node.id == 'False':
            return 'false'
        return node.id

    def visit_Eq(self, node):
        return '=='

    def visit_NotEq(self, node):
        return '!='

    def visit_Num(self, node):
        return str(node.n)

    def visit_Pass(self, node):
        return '/*pass*/'

    def visit_Mult(self, node):
        return '*'

    def visit_Add(self, node):
        return '+'

    def visit_Sub(self, node):
        return '-'

    def visit_Div(self, node):
        return '/'

    def visit_Mod(self, node):
        return '%'

    def visit_Lt(self, node):
        return '<'

    def visit_Gt(self, node):
        return '>'

    def visit_GtE(self, node):
        return '>='

    def visit_LtE(self, node):
        return '<='

    def visit_LShift(self, node):
        return '<<'

    def visit_RShift(self, node):
        return '>>'

    def visit_BitXor(self, node):
        return '^'

    def visit_BitOr(self, node):
        return '|'

    def visit_BitAnd(self, node):
        return '&'

    def visit_Not(self, node):
        return '!'

    def visit_IsNot(self, node):
        return '!=='

    def visit_USub(self, node):
        return '-'

    def visit_And(self, node):
        return ' && '

    def visit_Or(self, node):
        return ' || '

    def visit_Str(self, node):
        return '"{0}"'.format(node.s)

    def visit_Return(self, node):
        if node.value:
            return 'return {0};'.format(self.visit(node.value))
        return 'return;'

    def visit_If(self, node):
        buffer = []
        buffer.append('if ({0}) {{'.format(self.visit(node.test)))
        buffer.extend([self.visit(child) for child in node.body])

        orelse = [self.visit(child) for child in node.orelse]
        if orelse:
            buffer.append('} else {')
            buffer.extend(orelse)
            buffer.append("}")

        return '\n'.join(buffer)

    def visit_Print(self, node):
        buffer = ["std::cout"]
        for n in node.values:
            value = self.visit(n)
            buffer.append("<<")
            buffer.append(value)
        return " ".join(buffer) + "<< std::endl;"

    def visit_While(self, node):
        buffer = []
        buffer.append("while ({0}) {{".format(self.visit(node.test)))
        buffer.extend([self.visit(c) for c in node.body])
        buffer.append("}")
        return '\n'.join(buffer)

    def visit_Compare(self, node):
        left = self.visit(node.left)
        op = self.visit(node.ops[0])
        right = self.visit(node.comparators[0])
        return "{0} {1} {2}".format(left, op, right)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return " ".join([left, op, right])

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        op = self.visit(node.op)
        val = self.visit(node.value)
        return "{0} {1}= {2};".format(target, op, val)