
from nose.tools import raises, with_setup, eq_

from cement import hooks, namespaces, handlers
from cement.core.view import render_genshi_output, render_json_output

def setup_func():
    "set up test fixtures"
    pass
    
def teardown_func():
    "tear down test fixtures"
    pass
    
@with_setup(setup_func, teardown_func)
def test_render_genshi_output():
    fake_dict = dict(foo='String', bar=100, list=[1,2,3,4,5])
    tmpl_content = """$foo$bar{% for i in list %}${i}{% end %}"""
    output = render_genshi_output(fake_dict, tmpl_content)
    eq_(output, 'String10012345')

@with_setup(setup_func, teardown_func)
def test_render_genshi_output():
    fake_dict = dict(foo='String', bar=100, list=[1,2,3,4,5])
    tmpl_content = """$foo$bar{% for i in list %}${i}{% end %}"""
    output = render_json_output(fake_dict, tmpl_content)
    eq_(output, '{"bar": 100, "foo": "String", "list": [1, 2, 3, 4, 5], "stderr": "", "stdout": ""}')