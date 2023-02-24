import setuptools

setuptools.setup(
    name = 'btool',
    version = '0.0.1',
    author = 'RaisoLiu',
    author_email = 'raisoliu@gmail.com',
    description = 'Brain decoding & analysing toolbox',
    packages = setuptools.find_packages(),
    classifiers = [
    ],
    install_requires = [
        "os",
        "numpy",
        "tqdm",
        "h5py",
        "scipy",
        "matplotlib",
        "plotly",
    ],
    python_requires = ">=3.8",

)