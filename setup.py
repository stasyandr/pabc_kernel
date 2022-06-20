from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='pabc_kernel',
    version='1.1',
    packages=['pabc_kernel'],
    description='PABC.NET kernel for Jupyter',
    long_description=readme,
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
