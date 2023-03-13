from setuptools import setup

setup(
    name='kgraphserve',
    version='0.0.1',
    description='A Flask app for serving knowledge graphs',
    author='Eric Yates',
    author_email='eric@medleyagency.com',
    url='https://github.com/MedleyLabs/kgraphserve',
    packages=['kgraphserve'],
    install_requires=[
        'flask',
        'flask_cors',
        'owlready2',
        'pyyaml',
        'requests',
        'tqdm',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Flask',
        'Framework :: Pytest',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
    ],
)
