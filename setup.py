from setuptools import setup, find_packages

setup(
    name="next-ai-kov",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas==1.5.3',
        'streamlit',
        'numpy',
        'pip>=23.1',
        'setuptools',
        'wheel',
        'google-auth-oauthlib==1.1.0',
        'google-auth-httplib2==0.1.1',
        'google-api-python-client==2.108.0',
        'oauth2client==4.1.3'
    ],
    python_requires='>=3.10.0',
)
