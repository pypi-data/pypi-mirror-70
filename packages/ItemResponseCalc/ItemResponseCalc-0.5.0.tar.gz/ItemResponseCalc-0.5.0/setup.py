import setuptools
import ItemResponseCalc

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ItemResponseCalc",
    version= ItemResponseCalc.__version__,
    author="Arne Leijon",
    author_email="leijon@kth.se",
    description="Statistical Analysis of Questionnaire Response Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Multimedia :: Sound/Audio"
    ),
    keywords = 'questionnaire item-response-theory Bayesian',
    install_requires=['numpy>=1.17', 'scipy', 'matplotlib', 'samppy', 'openpyxl'],
    python_requires='>=3.6'
)
