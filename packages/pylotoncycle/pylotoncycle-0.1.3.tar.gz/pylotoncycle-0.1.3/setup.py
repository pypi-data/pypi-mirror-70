import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pylotoncycle',
    version='0.1.3',
    description='Module to access your peloton workout data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/justmedude/pylotoncycle',
    author='Vikram Adukia',
    author_email='github@fireitup.net',
    license='MIT',
    packages=['pylotoncycle'],
    install_requires=['requests'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3'
    ]
)
