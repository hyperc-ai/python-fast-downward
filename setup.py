import os
import sys
import platform
import subprocess
import glob
from setuptools import setup
from setuptools import find_packages
from wheel.bdist_wheel import bdist_wheel

PACKAGE_NAME = 'downward_ch'
DOWNWARD_REPO = 'http://hg.fast-downward.org '
REV = '7a0a766081e6'
PATCH = 'downward_patch3.patch'

def get_readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r').read()


class BuildFastDownward(bdist_wheel):

    def run(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))

        # hg clone -u 7a0a766081e6 http://hg.fast-downward.org  downward_ch
        build_process = subprocess.Popen(["hg clone -u " + REV + "http://hg.fast-downward.org " + PACKAGE_NAME], cwd=cur_dir,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        line = build_process.stdout.readline()
        encoding = "utf-8" if sys.stdout.encoding is None else sys.stdout.encoding
        while line:
              sys.stdout.write(line.decode(encoding))
              line = build_process.stdout.readline()
        line = build_process.stderr.readline()
        while line:
              sys.stderr.write(line.decode(encoding))
              line = build_process.stderr.readline()

#        patch -p1 < ../downward_patch3.patch
        package_dir = os.path.join(cur_dir, PACKAGE_NAME)
        patch_dir =  str(os.path.join(cur_dir, PATCH))
        build_process = subprocess.Popen(["patch -p1 < " + patch_dir], cwd=package_dir,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        line = build_process.stdout.readline()
        encoding = "utf-8" if sys.stdout.encoding is None else sys.stdout.encoding
        while line:
              sys.stdout.write(line.decode(encoding))
              line = build_process.stdout.readline()
        line = build_process.stderr.readline()
        while line:
              sys.stderr.write(line.decode(encoding))
              line = build_process.stderr.readline()
        return
        # Compilation
        package_dir = os.path.join(cur_dir, PACKAGE_NAME)
        build_command = str(os.path.join(package_dir, 'build.py'))
        print ("Building The Fast-Downward Planning System...")
        build_process = subprocess.Popen([build_command], cwd=package_dir,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        line = build_process.stdout.readline()
        encoding = "utf-8" if sys.stdout.encoding is None else sys.stdout.encoding
        while line:
              sys.stdout.write(line.decode(encoding))
              line = build_process.stdout.readline()
 
        line = build_process.stderr.readline()
        while line:
              sys.stderr.write(line.decode(encoding))
              line = build_process.stderr.readline()
    
        fileList = glob.glob(package_dir+'/driver/portfolios/*pyc')
        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)

        bdist_wheel.run(self)


setup(
    name=PACKAGE_NAME,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'bdist_wheel': BuildFastDownward},
    entry_points={'console_scripts': ['downward-ch=' + PACKAGE_NAME + '.downward_ch:downward_ch_main']},
    version='19.06.0',
    author='Kuznetsov Andrey A.',
    author_email='andreykyz@gmail.com',
    license='GNU General Public License Version 3',
    description=PACKAGE_NAME + ' is a fork of the Fast-Downward Planning System (www.fast-downward.org) with Critical hop patches by Andrey Gryaznov',
    long_description=get_readme(),
    keywords='semantic planning pddl fast downward planner fast-downward domain-independent',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: C++',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering'
    ]
)
