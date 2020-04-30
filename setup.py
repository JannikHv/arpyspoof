import os
import shutil

from setuptools import setup


shutil.copyfile('arpyspoof.py', 'arpyspoof')

setup(
    name='arpyspoof',
    version='0.0.1',
    description='Performs an ARP-spoofing attack',
    long_description='Performs an ARP-spoofing attack',
    url='https://github.com/JannikHv/arpyspoof',
    author='Jannik Hauptvogel',
    author_email='JannikHv@gmail.com',
    maintainer='Jannik Hauptvogel',
    maintainer_email='JannikHv@gmail.com',
    license='GPLv2',
    packages= [],
    scripts=['arpyspoof'],
    install_requires=['scapy', 'netifaces', 'ipaddress']
)

os.remove('arpyspoof')
