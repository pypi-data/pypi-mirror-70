from distutils.core import setup
setup(
    # How you named your package folder (MyLib)
    name='bitcoin_price_alert_app',
    packages=['bitcoin_price_alert_app'],   # Chose the same as "name"
    version='0.5',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='A python app that fetches the current price of bitcoins and sends notifications via Telegram, IFTTT, Email, twitter, and SMS',
    author='Atanu Paul',                   # Type in your name
    author_email='atanu.paul.rims@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/Atanu-Paul-au6/bitcoin_price_alert_app',
    # I explain this later on
    download_url='https://github.com/Atanu-Paul-au6/bitcoin_price_alert_app/archive/v0.5.tar.gz',
    # Keywords that define your package best
    keywords=['PYTHON', 'BITCOIN', 'TELEGRAM', 'IFTTT', 'EMAIL','Twitter','Android-SMS'],
    install_requires=[            # I get to this in a second
        'requests'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
