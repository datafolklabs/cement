
from {{ label }}.main import {{ class_name}}Test

def test_{{ label }}(tmp):
    with {{ class_name }}Test() as app:
        res = app.run()
        print(res)
        raise Exception

def test_command1(tmp):
    argv = ['command1']
    with {{ class_name }}Test(argv=argv) as app:
        app.run()
