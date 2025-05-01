from setuptools import setup
from setuptools import find_packages
from distutils.extension import Extension


def get_build_ext():
    try:
        from Cython.Distutils import build_ext
        return build_ext
    except ImportError:
        from setuptools.command.build_ext import build_ext
        return build_ext


def get_numpy_include():
    try:
        import numpy
        return numpy.get_include()
    except ImportError:
        return None


# Define extensions without numpy dependency
peaks = Extension("clipper.src.peaks", sources=['clipper/src/peaksmodule.cc'])

# Define readsToWiggle with numpy include if available
numpy_include = get_numpy_include()
if numpy_include:
    readsToWiggle = Extension("clipper.src.readsToWiggle",
                              ['clipper/src/readsToWiggle.pyx'],
                              include_dirs=[numpy_include])
else:
    readsToWiggle = Extension("clipper.src.readsToWiggle",
                              ['clipper/src/readsToWiggle.pyx'])

long_description = "CLIPPER - clip peak enrichment"
setup(
    name="clipper",
    long_description=long_description,
    version="2.1.2",
    packages=find_packages(),
    cmdclass={'build_ext': get_build_ext()},
    ext_modules=[readsToWiggle, peaks],

    package_data={
        'clipper': ['data/*', 'data/regions/*', 'test/data/*']
    },

    install_requires=['setuptools',
                      'pysam >= 0.15.3',
                      'numpy >= 1.18.5',
                      'scipy >= 1.5.0',
                      'matplotlib >= 3.2.2',
                      'pybedtools >= 0.8.1',
                      'scikit-learn >= 0.23.1',
                      'HTSeq >= 0.11.3'
                      ],

    setup_requires=["setuptools_git >= 0.3",
                    "numpy >= 1.18.5",
                    "Cython >= 0.29.0"],

    entry_points={
        'console_scripts': [
            'clipper = clipper.src.main:call_main',
        ],
    },

    # metadata for upload to PyPI
    author="Michael Lovci and Gabriel Pratt",
    author_email="mlovci@ucsd.edu",
    description="A set of scripts for calling peaks on CLIP-seq data",
    license="GPL2",
    keywords="CLIP-seq, peaks, bioinformatics",
    url="https://github.com/YeoLab/clipper",
)
