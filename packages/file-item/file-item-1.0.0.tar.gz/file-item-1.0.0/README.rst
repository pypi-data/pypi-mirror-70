file-item
=========

Documentation: https://file-item.readthedocs.io/en/latest/

Installation
------------

::

    pip install file_item

Examples:
---------

::

    from file_item import File

    basedir = File.basedir(__file__)

    file_1 = basedir.joinpath('test1.csv')
    file_2 = File('/home/user/test2.csv')
    file_3 = File.from_strings('/home/user/', 'test3.csv')

    print(repr(file_1))
    # PosixPath('test1.csv')

    print(file_2)
    # /home/user/test2.csv

    print(file_1 == file_2)
    # False

    print(file_3.name)
    # test3.csv

    file_1.create_folder()

    print(File.get_file_name('test*.csv'))
    # test-.csv

