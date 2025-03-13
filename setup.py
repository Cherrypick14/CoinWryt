from setuptools import find_packages, setup

setup(
    name='CoinWryt',
    version='1.0.0',
    port='0.0.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'web3', 'flask-sslify' , 'flask-cors' , 'flask' , 'twilio'  , 'watchdog' ,  
    ],
)
