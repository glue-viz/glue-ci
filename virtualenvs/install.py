import os
import shutil
from copy import deepcopy

PYTHON_VERSIONS = ['2.6', '2.7']  # pv
NUMPY_VERSIONS = ['1.4.1', '1.5.1', '1.6.2']  # nv
SCIPY_VERSIONS = ['0.9.0', '0.10.1']  # sv
MATPLOTLIB_VERSIONS = ['1.1.0', '1.1.1']  # mv
IPYTHON_VERSIONS = ['0.11', '0.12', '0.13']  # iv
PYFITS_VERSIONS = ['3.0.9', '3.1']  # fv
SIP_VERSIONS = ['4.13.3']  # sipv
PYQT4_VERSIONS = ['4.9.4']  # qtv

ADDITIONAL_PIP = ['atpy', 'pygments', 'pyzmq', 'pylint', 'pytest', 'pep8', 'pytest-cov', 'aplpy', 'pywcs', 'mock']


def dist_name(**kwargs):
    return 'python{pv}-numpy{nv}-scipy{sv}-ipython{iv}-pyfits{fv}-pyqt{qtv}-sip{sipv}'.format(**kwargs)

versions = []
version = {}
for pv in PYTHON_VERSIONS:
    version['pv'] = pv
    for nv in NUMPY_VERSIONS:
        version['nv'] = nv
        for sv in SCIPY_VERSIONS:
            version['sv'] = sv
            for mv in MATPLOTLIB_VERSIONS:
                version['mv'] = mv
                for iv in IPYTHON_VERSIONS:
                    version['iv'] = iv
                    for fv in PYFITS_VERSIONS:
                        version['fv'] = fv
                        for sipv in SIP_VERSIONS:
                            version['sipv'] = sipv
                            for qtv in PYQT4_VERSIONS:
                                version['qtv'] = qtv
                                versions.append(deepcopy(version))

for version in versions:

    # Get full path for Python virtualenv
    version['full'] = dist_name(**version)

    # Set up virtualenv
    os.system('$HOME/usr/python/bin/virtualenv-{pv} --python=$HOME/usr/python/bin/python{pv} --no-site-packages {full}.tmp'.format(**version))

    # Copy to resolve symbolic links
    shutil.copytree('{full}.tmp'.format(**version), '{full}'.format(**version))
    shutil.rmtree('{full}.tmp'.format(**version))

    # Install Numpy
    os.system('tar xvf tarfiles/numpy-{nv}.tar'.format(**version))
    os.chdir('numpy-{nv}'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py build --fcompiler=gnu95'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py install'.format(**version))
    os.chdir('../')
    os.system('rm -r numpy-{nv}'.format(**version))

    # Install Scipy
    os.system('tar xvf tarfiles/scipy-{sv}.tar'.format(**version))
    os.chdir('scipy-{sv}'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py build --fcompiler=gnu95'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py install'.format(**version))
    os.chdir('../')
    os.system('rm -r scipy-{sv}'.format(**version))

    # Install IPython
    os.system('tar xvf tarfiles/ipython-{iv}.tar'.format(**version))
    os.chdir('ipython-{iv}'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py build'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py install'.format(**version))
    os.chdir('../')
    os.system('rm -r ipython-{iv}'.format(**version))

    # Install Matplotlib
    os.system('tar xvf tarfiles/matplotlib-{mv}.tar'.format(**version))
    os.chdir('matplotlib-{mv}'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py build'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py install'.format(**version))
    os.chdir('../')
    os.system('rm -r matplotlib-{mv}'.format(**version))

    # Install PyFITS
    os.system('tar xvf tarfiles/pyfits-{fv}.tar'.format(**version))
    os.chdir('pyfits-{fv}'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py build'.format(**version))
    os.system('../{full}/bin/python{pv} setup.py install'.format(**version))
    os.chdir('../')
    os.system('rm -r pyfits-{fv}'.format(**version))

    # Install sip and PyQT4
    os.system('tar xvf tarfiles/sip-{sipv}.tar'.format(**version))
    os.chdir('sip-{sipv}'.format(**version))
    os.system('../{full}/bin/python{pv} configure.py --incdir=../{full}/include/python{pv}'.format(**version))
    os.system('make')
    os.system('make install')
    os.chdir('../')
    os.system('tar xvf tarfiles/PyQt-x11-gpl-{qtv}.tar'.format(**version))
    os.chdir('PyQt-x11-gpl-{qtv}'.format(**version))
    os.system('../{full}/bin/python{pv} configure.py -q /usr/lib64/qt4/bin/qmake -g --confirm-license'.format(**version))
    os.system('make')
    os.system('make install')
    os.chdir('../')
    os.system('rm -r sip-{sipv}'.format(**version))
    os.system('rm -r PyQt-x11-gpl-{qtv}'.format(**version))

