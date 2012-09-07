import os
import shutil

for version in ['2.6.8', '2.7.3', '3.1.5', '3.2.3']:

    short_version = version[:3]

    if os.path.exists('Python-{0:s}'.format(version)):
        shutil.rmtree('Python-{0:s}'.format(version))

    os.system('tar xvzf Python-{0:s}.tgz'.format(version))

    os.chdir('Python-{0:s}'.format(version))
    os.system('./configure --prefix=$HOME/usr/python ; make ; make install')
    os.chdir('..')

    shutil.rmtree('Python-{0:s}'.format(version))

    if os.path.exists('distribute-0.6.28'):
        shutil.rmtree('distribute-0.6.28')
    os.system('tar xvzf distribute-0.6.28.tar.gz')
    os.chdir('distribute-0.6.28')
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('distribute-0.6.28')

    if os.path.exists('pip-1.2.1'):
        shutil.rmtree('pip-1.2.1')

    os.system('tar xvzf pip-1.2.1.tar.gz')
    os.chdir('pip-1.2.1')
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('pip-1.2.1')

    os.system('$HOME/usr/python/bin/pip-{0:s} install virtualenv'.format(short_version))

