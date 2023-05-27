import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Flask-Modals',
    version='0.5.0',
    author='Debashish Palit',
    author_email='dpalit17@outlook.com',
    description='Use forms in Bootstrap modals with Flask.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/deb17/flask-modals',
    packages=['flask_modals'],
    package_data={'flask_modals': ['templates/modals/*.html',
                                   'static/js/main.js',
                                   'static/css/progressBarStyle.css']},
    include_package_data=True,
    install_requires=['Flask', 'lxml'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
