from setuptools import setup

setup(
        name='libnxctrl',
        version='0.1.0',
        url='https://github.com/Victrid/libnxctrl',
        license='GPLv3',
        author='Weihao Jiang',
        author_email='weihau.chiang@gmail.com',
        description='Python Library Emulating Nintendo Switch Controllers',
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Software Development :: Libraries",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            ],
        package_data={
            'libnxctrl.mart1no_joycontrol': [
                'joycontrol/profile/sdp_record_hid.xml',
                'LICENSE',
                'README.md'
                ],
            'libnxctrl.Poohl_joycontrol':   [
                'joycontrol/profile/sdp_record_hid.xml',
                'LICENSE',
                'README.md'
                ],
            'libnxctrl.nxbt.nxbt':          [
                'controller/sdp/switch-controller.xml',
                'LICENSE',
                'README.md'
                ]
            },
        )
