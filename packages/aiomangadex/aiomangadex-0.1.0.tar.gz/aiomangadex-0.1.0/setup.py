from distutils.core import setup
setup(
  name = 'aiomangadex',         # How you named your package folder (MyLib)
  packages = ['aiomangadex'],   # Chose the same as "name"
  version = '0.1.0',      # Start with a small number and increase it with every change you make
  license='Apache License 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple asynchronous API wrapper for mangadex.org.',   # Give a short description about your library
  author = 'lukesaltweather',                   # Type in your name
  author_email = 'lukesaltweather@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/lukesaltweather/aiomangadex',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/lukesaltweather/aiomangadex/archive/0.1.0.tar.gz',    # I explain this later on
  keywords = ['Manga', 'API'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'aiohttp',
          'ujson',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)