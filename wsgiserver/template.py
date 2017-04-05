"""
This is a tiny template system, authored by mozillazg (@https://github.com/mozillazg).

Sample code:
>>> from wsgiserver.template import Template

>>> template = Template('<html>{% if test %}<h1>{{ varvalue }}</h1>{% endif %}</html>')
>>> print template.render({'test': True, 'varvalue': 'Hello'})
'<html><h1>Hello</h1></html>'

"""

import os
import re

__author__ = "mozillazg"


class CodeBuilder:
    INDENT_STEP = 4

    def __init__(self, indent=0):
        self.indent = indent
        self.lines = []

    def forward(self):
        self.indent += self.INDENT_STEP

    def backward(self):
        self.indent -= self.INDENT_STEP

    def add(self, code):
        self.lines.append(code)

    def add_line(self, code):
        self.lines.append(' ' * self.indent + code)

    def __str__(self):
        return '\n'.join(map(str, self.lines))

    def __repr__(self):
        return str(self)


class Template:

    def __init__(self, raw_text, indent=0, default_context=None,
                 func_name='__func_name', result_var='__result',
                 template_dir='', encoding='utf-8'):
        self.raw_text = raw_text
        self.default_context = default_context or {}
        self.func_name = func_name
        self.result_var = result_var
        self.template_dir = template_dir
        self.encoding = encoding
        self.code_builder = code_builder = CodeBuilder(indent=indent)
        self.buffered = []

        self.re_variable = re.compile(r'\{\{ .*? \}\}')
        self.re_comment = re.compile(r'\{# .*? #\}')
        self.re_tag = re.compile(r'\{% .*? %\}')
        self.re_tokens = re.compile(r'''(
            (?:\{\{ .*? \}\})
            |(?:\{\# .*? \#\})
            |(?:\{% .*? %\})
        )''', re.VERBOSE)

        # extends
        self.re_extends = re.compile(r'\{% extends (?P<name>.*?) %\}')
        # blocks
        self.re_blocks = re.compile(
            r'\{% block (?P<name>\w+) %\}'
            r'(?P<code>.*?)'
            r'\{% endblock \1 %\}', re.DOTALL)
        # block.super
        self.re_block_super = re.compile(r'\{\{ block\.super \}\}')

        code_builder.add_line('def {}():'.format(self.func_name))
        code_builder.forward()
        code_builder.add_line('{} = []'.format(self.result_var))
        self._parse_text()

        self.flush_buffer()
        code_builder.add_line('return "".join({})'.format(self.result_var))
        code_builder.backward()

    def _parse_text(self):
        # extends
        self._handle_extends()

        tokens = self.re_tokens.split(self.raw_text)
        handlers = (
            (self.re_variable.match, self._handle_variable),
            (self.re_tag.match, self._handle_tag),
            (self.re_comment.match, self._handle_comment),
        )
        default_handler = self._handle_string

        for token in tokens:
            for match, handler in handlers:
                if match(token):
                    handler(token)
                    break
            else:
                default_handler(token)

    def _handle_variable(self, token):
        variable = token.strip('{} ')
        self.buffered.append('str(globals().get("{}", ""))'.format(variable))

    def _handle_comment(self, token):
        pass

    def _handle_string(self, token):
        self.buffered.append('{}'.format(repr(token)))

    def _handle_tag(self, token):
        self.flush_buffer()
        tag = token.strip('{%} ')
        tag_name = tag.split()[0]
        if tag_name == 'include':
            self._handle_include(tag)
        else:
            self._handle_statement(tag)

    def _handle_statement(self, tag):
        tag_name = tag.split()[0]
        if tag_name in ('if', 'elif', 'else', 'for'):
            if tag_name in ('elif', 'else'):
                self.code_builder.backward()
            self.code_builder.add_line('{}:'.format(tag))
            self.code_builder.forward()
        elif tag_name in ('break',):
            self.code_builder.add_line(tag)
        elif tag_name in ('endif', 'endfor'):
            self.code_builder.backward()

    def _handle_include(self, tag):
        filename = tag.split()[1].strip('"\'')
        included_template = self._parse_another_template_file(filename)
        self.code_builder.add(included_template.code_builder)
        self.code_builder.add_line(
            '{0}.append({1}())'.format(
                self.result_var, included_template.func_name
            )
        )

    def _parse_another_template_file(self, filename):
        template_path = os.path.realpath(
            os.path.join(self.template_dir, filename)
        )
        name_suffix = str(hash(template_path)).replace('-', '_')
        func_name = '{}_{}'.format(self.func_name, name_suffix)
        result_var = '{}_{}'.format(self.result_var, name_suffix)
        with open(template_path, encoding=self.encoding) as fp:
            template = self.__class__(
                fp.read(), indent=self.code_builder.indent,
                default_context=self.default_context,
                func_name=func_name, result_var=result_var,
                template_dir=self.template_dir
            )
        return template

    def _handle_extends(self):
        match_extends = self.re_extends.match(self.raw_text)
        if match_extends is None:
            return

        parent_template_name = match_extends.group('name').strip('"\' ')
        parent_template_path = os.path.join(
            self.template_dir, parent_template_name
        )
        child_blocks = self._get_all_blocks(self.raw_text)
        with open(parent_template_path, encoding=self.encoding) as fp:
            parent_text = fp.read()
        new_parent_text = self._replace_parent_blocks(
            parent_text, child_blocks
        )
        self.raw_text = new_parent_text

    def _replace_parent_blocks(self, parent_text, child_blocks):
        def replace(match):
            name = match.group('name')
            parent_code = match.group('code')
            child_code = child_blocks.get(name, '')
            child_code = self.re_block_super.sub(parent_code, child_code)
            new_code = child_code or parent_code
            return new_code
        return self.re_blocks.sub(replace, parent_text)

    def _get_all_blocks(self, text):
        return {
            name: code
            for name, code in self.re_blocks.findall(text)
        }

    def flush_buffer(self):
        line = '{0}.extend([{1}])'.format(
            self.result_var, ','.join(self.buffered)
        )
        self.code_builder.add_line(line)
        self.buffered = []

    def render(self, context=None):
        namespace = {}
        namespace.update(self.default_context)
        namespace.update(context or {})
        exec str(self.code_builder) in namespace
        return namespace[self.func_name]()
