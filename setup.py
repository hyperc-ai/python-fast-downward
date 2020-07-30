import os
import sys
import platform
import subprocess
import glob
from setuptools import setup
from setuptools import find_packages
from wheel.bdist_wheel import bdist_wheel
import shutil
import stat

PACKAGE_NAME = 'downward_ch'
DOWNWARD_REPO = 'https://github.com/criticalhop/downward.git '
BRANCH = 'ch-addition'
FF_REPO = 'git@github.com:criticalhop/FF-emscripten.git'
FF_DIR = 'FF-emscripten'
PATCHES = ['downward_patch3.patch', 'total-queue-pushes_02.patch']

def get_readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r').read()


def get_umask():
    umask = os.umask(0)
    os.umask(umask)
    return umask


def chmod_plus_x(path):
    os.chmod(
        path,
        os.stat(path).st_mode |
        (
            (
                stat.S_IXUSR |
                stat.S_IXGRP |
                stat.S_IXOTH
            )
            & ~get_umask()
        )
    )

def run_proc(run_lst, dir):
    build_process = subprocess.Popen(run_lst, cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    line = build_process.stdout.readline()
    encoding = "utf-8" if sys.stdout.encoding is None else sys.stdout.encoding
    while line:
            sys.stdout.write(line.decode(encoding))
            line = build_process.stdout.readline()
    line = build_process.stderr.readline()
    while line:
            sys.stderr.write(line.decode(encoding))
            line = build_process.stderr.readline()

class BuildFastDownward(bdist_wheel):

    def get_tag(self):
        python, abi, plat = bdist_wheel.get_tag(self)
        if 'linux' == plat.split('_')[0]:
            plat = 'manylinux1_{0}'.format('_'.join(plat.split('_')[1:]))
        python, abi = 'py3', 'none'
        return python, abi, plat

    def run(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        package_dir = os.path.join(cur_dir, PACKAGE_NAME)
        #cleanup
        try:
            shutil.rmtree(os.path.join(cur_dir, "build"))
        except:
            pass
        try:
            shutil.rmtree(os.path.join(cur_dir, "dist"))
        except:
            pass            
        try:            
            shutil.rmtree(package_dir)
        except:
            pass
        #ff-hoffman
        run_proc(["git clone " + FF_REPO], cur_dir)
        
        run_proc(["make"], os.path.join(cur_dir, FF_DIR))
        #maplan
        run_proc(['git clone https://gitlab.com/danfis/maplan.git'], cur_dir)

        run_proc(["make boruvka opts protobuf nanomsg translate"], os.path.join(cur_dir, 'maplan/third-party'))
        run_proc(["make -C ./bin"], os.path.join(cur_dir, 'maplan'))
        #ipc2018-classical/team2
        #run_proc(['git clone https://bitbucket.org/ipc2018-classical/team2.git'], cur_dir)
 
        # hg clone -u 7a0a766081e6 http://hg.fast-downward.org  downward_ch
        run_proc(["git clone -b " + BRANCH + " " + DOWNWARD_REPO + " " + PACKAGE_NAME], cur_dir)

#       cd downward_ch ; patch -p1 < ../downward_patch3.patch
#        for PATCH in PATCHES:
#            patch_dir =  str(os.path.join(cur_dir, PATCH))
#            run_proc(["patch -p1 < " + patch_dir], package_dir)

        shutil.copyfile(os.path.join(cur_dir, "downward_ch.py"), os.path.join(package_dir, "downward_ch.py"))
        shutil.copyfile(os.path.join(cur_dir, "__init__.py"), os.path.join(package_dir, "__init__.py"))
        
        # Compilation
        build_command = str(os.path.join(package_dir, 'build.py'))
        print ("Building The Fast-Downward Planning System...")
        run_proc([build_command], package_dir)
    
        #Remove pyc files that break fast-downward
        fileList = glob.glob(package_dir+'/driver/portfolios/*pyc')
        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)

        # cleanup fast-downward 
        shutil.rmtree(os.path.join(package_dir, ".hg"))
        shutil.rmtree(os.path.join(package_dir, "experiments"))
        shutil.rmtree(os.path.join(package_dir, "src"))
        shutil.rmtree(os.path.join(package_dir, "builds/release/search"))
        shutil.copytree(os.path.join(cur_dir, 'maplan'), os.path.join(package_dir, 'maplan'))
        shutil.copyfile(os.path.join(cur_dir, FF_DIR + '/ff'), os.path.join(package_dir, "builds/release/bin/ff"))
        chmod_plus_x(os.path.join(package_dir, "builds/release/bin/ff"))
        shutil.rmtree(os.path.join(cur_dir, FF_DIR))

        self.root_is_pure = False
        bdist_wheel.run(self)


setup(
    name=PACKAGE_NAME,
    python_requires='>=3.6.0',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'bdist_wheel': BuildFastDownward},
    entry_points={'console_scripts': ['fast-downward=' + PACKAGE_NAME + '.downward_ch:downward_ch_main']},
    version='0.0.7',
    author='Kuznetsov Andrey A.',
    author_email='andreykyz@gmail.com',
    license='GNU General Public License Version 3',
    description=PACKAGE_NAME + ' is the Fast-Downward Planning System (www.fast-downward.org) with Critical hop patches',
    long_description=get_readme(),
    keywords='semantic planning pddl fast downward planner fast-downward domain-independent',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: C++',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering'
    ]
)
