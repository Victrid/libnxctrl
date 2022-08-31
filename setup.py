from setuptools import setup

setup(
        name='libnxctrl',
        version='0.1.1',
        url='https://github.com/Victrid/libnxctrl',
        license='GPLv3',
        author='Weihao Jiang',
        author_email='weihau.chiang@gmail.com',
        description='Python Library Emulating Nintendo Switch Controllers',
        readme='README.md',
        readme_type='text/markdown',
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Software Development :: Libraries",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            ],
        install_requires=[
            # NXBT requirements
            "dbus-python~=1.2.16",
            "Flask~=1.1.2",
            "Flask-SocketIO~=5.0.1",
            "eventlet~=0.31.0",
            "blessed~=1.17.10",
            "pynput~=1.7.1",
            "psutil~=5.6.6",
            "cryptography~=3.3.2",
            # JoyControl requirements
            'hid~=1.0.5',
            'aioconsole~=0.5.1'
            ],
        packages=['libnxctrl',
                  'libnxctrl.nxbt',
                  'libnxctrl.mart1no_joycontrol.joycontrol',
                  'libnxctrl.Poohl_joycontrol.joycontrol'],
        package_dir={
            'libnxctrl':                               'src/libnxctrl',
            'libnxctrl.nxbt':                          'src/libnxctrl/nxbt',
            'libnxctrl.mart1no_joycontrol.joycontrol': 'src/libnxctrl/mart1no_joycontrol/joycontrol',
            'libnxctrl.Poohl_joycontrol.joycontrol':   'src/libnxctrl/Poohl_joycontrol/joycontrol'
            },
        package_data={
            'libnxctrl.mart1no_joycontrol.joycontrol': [
                'profile/sdp_record_hid.xml',
                '../LICENSE',
                '../README.md'
                ],
            'libnxctrl.Poohl_joycontrol.joycontrol':   [
                'profile/sdp_record_hid.xml',
                '../LICENSE',
                '../README.md'
                ],
            'libnxctrl.nxbt':                          [
                'nxbt/controller/sdp/switch-controller.xml'
                '../LICENSE',
                '../README.md'
                ],
            'libnxctrl.nxbt.nxbt.controller':          [

                ]
            },
        )
