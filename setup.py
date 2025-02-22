from setuptools import find_packages, setup

setup(
    name='Denso-Technologies',
    version='1.0.0',
    port='0.0.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'phonenumbers' , 'geocoder' , 'folium' , 'twilio'  , 'watchdog' , 'flask-sslify' 
    ],
)
