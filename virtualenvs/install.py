import os
import shutil
from copy import deepcopy

# Create dictionary of SIP versions for PyQt4 versions
SIP = {}
SIP['4.9.4'] = '4.13.3'

# Set up virtual environments for testing ipython/pyqt4/matplotlib

PYTHON_VERSIONS = ['2.6', '2.7']  # pv
MATPLOTLIB_VERSIONS = ['1.1.0', '1.1.1']  # mv                                                                                                                           
IPYTHON_VERSIONS = ['0.11', '0.12', '0.13']  # iv                                                                                                                         
PYQT4_VERSIONS = ['4.9.4']  # qtv                                                                                                                                          

def dist_name(**kwargs):
    return 'python{pv}-matplotlib{mv}-ipython{iv}-pyqt{qtv}'.format(**kwargs)

versions = []
version = {}

# Set environment variables for Scipy                                                                                                                                 
version['env'] = 'BLAS=/n/glue/CI/virtualenvs/linalg/BLAS/libfblas.a LAPACK=/n/glue/CI/virtualenvs/linalg/LAPACK/liblapack.a'

# Set up versions for fixed packages
version['nv'] = '1.6.2'
version['sv'] = '0.10.1'
version['fv'] = '3.1'

# Set up versions for variable packages
for pv in PYTHON_VERSIONS:
    version['pv'] = pv
    for mv in MATPLOTLIB_VERSIONS:
        version['mv'] = mv
        for iv in IPYTHON_VERSIONS:
            version['iv'] = iv
            for qtv in PYQT4_VERSIONS:
                version['qtv'] = qtv
                version['sipv'] = SIP[qtv]
                version['full'] = dist_name(**version)
                versions.append(deepcopy(version))

for version in versions:

    # Set up virtualenv
    os.system('$HOME/usr/python/bin/virtualenv-{pv} --python=$HOME/usr/python/bin/python{pv} --no-site-packages {full}.tmp'.format(**version))

    # Copy to resolve symbolic links
    shutil.copytree('{full}.tmp'.format(**version), '{full}'.format(**version))
    shutil.rmtree('{full}.tmp'.format(**version))

    # Set permissions back to read/write
    os.system("chmod -R u+w {full}".format(**version))

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
    os.system('{env} ../{full}/bin/python{pv} setup.py build --fcompiler=gnu95'.format(**version))
    os.system('{env} ../{full}/bin/python{pv} setup.py install'.format(**version))
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

    # Install fixed version packages
    os.system('{full}/bin/python {full}/bin/pip install -r dependencies.txt'.format(**version))


