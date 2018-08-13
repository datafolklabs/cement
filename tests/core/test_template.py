
import os
from cement.utils.test import TestApp, raises
from cement.core.template import TemplateInterface, TemplateHandler


# module tests

class TestTemplateInterface(object):
    def test_interface(self):
        assert TemplateInterface.Meta.interface == 'template'


class TestTemplateHandler(object):
    def test_subclassing(self):
        class MyTemplateHandler(TemplateHandler):
            class Meta:
                label = 'my_template_handler'

            def render(self, *args, **kw):
                pass

            def copy(self, *args, **kw):
                pass

            def load(self, *args, **kw):
                pass

        h = MyTemplateHandler()
        assert h._meta.interface == 'template'
        assert h._meta.label == 'my_template_handler'


# app functionality and coverage tests

def test_exclude_and_ignore_are_none():

    class MyHandler(TemplateHandler):
        class Meta:
            label = 'test'
            ignore = None
            exclude = None

    res = MyHandler()
    assert isinstance(res._meta.ignore, list)
    assert isinstance(res._meta.exclude, list)


def test_copy(tmp, rando):
    with TestApp(extensions=['jinja2'], template_handler='jinja2') as app:
        # create a template src
        os.makedirs(os.path.join(tmp.dir, 'src'))
        with open(os.path.join(tmp.dir, 'src', 'take-me'), 'w') as f:
            f.write('{{ rando }}')

        with open(os.path.join(tmp.dir, 'src', 'ignore-me'), 'w') as f:
            f.write('{{ rando }}')

        with open(os.path.join(tmp.dir, 'src', 'exclude-me'), 'w') as f:
            f.write('{{ rando }}')

        # copy to dest

        app.template.copy(os.path.join(tmp.dir, 'src'),
                          os.path.join(tmp.dir, 'dest'),
                          {'rando': rando},
                          exclude=['.*exclude-me.*'],
                          ignore=['.*ignore-me.*'])

        # assert variables are interpolated

        print(os.listdir(tmp.dir))
        print(os.listdir(os.path.join(tmp.dir, 'src')))
        print(os.listdir(os.path.join(tmp.dir, 'dest')))
        with open(os.path.join(tmp.dir, 'dest', 'take-me'), 'r') as f:
            assert f.read() == rando

        # assert files are ignored/excluded

        with open(os.path.join(tmp.dir, 'dest', 'exclude-me'), 'r') as f:
            assert f.read() == '{{ rando }}'

        assert not os.path.exists(os.path.join(tmp.dir, 'dest', 'ignore-me'))

        # copy again with and without force

        with raises(AssertionError, match='Destination file already exists:'):
            app.template.copy(os.path.join(tmp.dir, 'src'),
                              os.path.join(tmp.dir, 'dest'),
                              {'rando': rando},
                              exclude=['.*exclude-me.*'],
                              ignore=['.*ignore-me.*'])

        app.template.copy(os.path.join(tmp.dir, 'src'),
                          os.path.join(tmp.dir, 'dest'),
                          {'rando': rando},
                          exclude=['.*exclude-me.*'],
                          ignore=['.*ignore-me.*'],
                          force=True)

        # again with explicit none ignore/exclude for coverage

        app.template.copy(os.path.join(tmp.dir, 'src'),
                          os.path.join(tmp.dir, 'dest'),
                          {'rando': rando},
                          exclude=None,
                          ignore=None,
                          force=True)


def test_load_template_from_file_does_not_exist(tmp):
    class ThisApp(TestApp):
        class Meta:
            template_dirs = [tmp.dir]

    with ThisApp() as app:
        app.run()
        res = app.template._load_template_from_file('bogus')
        assert res == (None, None)
