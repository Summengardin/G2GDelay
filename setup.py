from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        return [line for line in lines if line and not line.startswith('#')]

setup(
    name='G2GDelay',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'G2GDelay=G2GDelay.G2GDelay:main',
            'G2GDelay-analyze=G2GDelay.analyze_results:main',
        ],
    },
    author='Martin Simengård',
    author_email='martin.simengard@seaonics.com',
    description='A tool for measuring glass-to-glass delay.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Summengardin/G2GDelay',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)