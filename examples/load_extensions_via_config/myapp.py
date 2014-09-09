
from cement.core.foundation import CementApp

class MyApp(CementApp):
    class Meta:
        label = 'myapp'

        config_files = [
            './myapp.conf',
            ]

    def validate_config(self):
        if 'extensions' in self.config.keys('myapp'):
            exts = self.config.get('myapp', 'extensions')

            # convert a comma-separated string to a list
            if type(exts) is str:
                ext_list = exts.split(',')

                # clean up extra space if they had it inbetween commas
                ext_list = (x.strip() for x in ext_list)

                # set the new extensions value in the config
                self.config.set('myapp', 'extensions', ext_list)

            # otherwise, if it's a list (ConfigObj?)
            elif type(exts) is list:
                ext_list = exts

            for ext in ext_list:
                # load the extension
                self.ext.load_extension(ext)

                # add to meta data
                self._meta.extensions.append(ext)

def main():
    app = MyApp()
    try:
        app.setup()
        app.run()
    finally:
        app.close()

if __name__ == '__main__':
    main()
