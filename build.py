import urllib
import os
import subprocess
import zipfile
import shutil
import glob
import sys

def make_dir_safe(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)

def apply_patch(p):
	patch_file, target_file = p
	subprocess.call('patch -f %s ../../patches/%s' % (target_file, patch_file))

def progress_hook(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	sys.stdout.write("\rProgress: %2d%%" % percent)
	#sys.stdout.write("\b\b\b")
	sys.stdout.flush()

def main():
	download_dir = 'downloads'
	msvcver = 12
	msvcyear = 2013
	architecture = 64
	boost_version = '1.59.0'
	boost_version_ = '1_59_0'
	force_download_boost = False
	force_unpack_boost = False
	force_download_flexbison = False
	force_unpack_flexbison = False
	flex_target_dir = 'install/bin'
	build_config = 'Debug'
	build_dir = 'build'
	build_phases = [
	(True,''), 
	(True, '-DZLIB_INCLUDE_DIR=%s -DZLIB_ROOT=%s' % (os.path.abspath('install/include'), os.path.abspath('install'))), 
	(True, ''), 
	(True, ''), 
	(True, '-DOSL_BUILD_CPP11=1 -DLLVM_FIND_QUIETLY=0 -DBUILDSTATIC=1 -DOSL_BUILD_PLUGINS=0 -Wno-dev')]

	patches = [
	[('libjpeg/CMakeLists.txt.patch', '../../phase1/libjpeg/CMakeLists.txt')],
	[('libtiff/CMakeLists.txt.patch', '../../phase2/libtiff/CMakeLists.txt')],
	[('oiio/py_deepdata.cpp.patch', '../../phase3/oiio/src/python/py_deepdata.cpp')],
	[],
	[('OpenShadingLanguage/CMakeLists.txt.patch','../../phase5/OpenShadingLanguage/CMakeLists.txt'),
	('OpenShadingLanguage/externalpackages.cmake.patch','../../phase5/OpenShadingLanguage/src/cmake/externalpackages.cmake'),
	('OpenShadingLanguage/flexbison.cmake.patch','../../phase5/OpenShadingLanguage/src/cmake/flexbison.cmake'),
	('OpenShadingLanguage/oslgram.y.patch','../../phase5/OpenShadingLanguage/src/liboslcomp/oslgram.y'),
	('OpenShadingLanguage/osllex.l.patch','../../phase5/OpenShadingLanguage/src/liboslcomp/osllex.l')]]
	devenv_path = '\"C:\\Program Files (x86)\\Microsoft Visual Studio %d.0\\Common7\\IDE\\devenv.com\"' % (msvcver)

	make_dir_safe(download_dir)
	
	# BOOST
	boost_target = download_dir + '/boost.exe'
	if force_download_boost or not os.path.exists(boost_target):
		print("Downloading boost")
		boost_url = 'http://iweb.dl.sourceforge.net/project/boost/boost-binaries/%s/boost_%s-msvc-%d.0-%d.exe' % (boost_version, boost_version_, msvcver, architecture)
		urllib.urlretrieve(boost_url, boost_target, progress_hook)
	else:
		print("Boost already downloaded, skipping")
	# Choosing random file, not sure if there is a safer way of knowing if we have a successful unpack here
	if force_unpack_boost or not os.path.exists(download_dir + '/boost/tools/index.html' ):
		print("Unpacking boost")
		res = subprocess.call('\"%s\" /dir=%s/boost /sp- /silent' % (boost_target, download_dir), shell = True)
		if not res == 0:
			print("Failed to unpack boost")
			return
	else:
		print("Boost already unpacked, skipping")
	
	#Flex/Bison
	flex_target = download_dir + '/win_flex_bison-latest.zip'
	make_dir_safe('install')
	make_dir_safe('install/bin')
	if force_download_flexbison or not os.path.exists(flex_target):
		print("Downloading flex")
		urllib.urlretrieve('http://tcpdiag.dl.sourceforge.net/project/winflexbison/win_flex_bison-latest.zip', flex_target, progress_hook)
	else:
		print("Flex already downloaded, skipping")

	# Choosing random file, not sure if there is a safer way of knowing if we have a successful unpack here
	if force_unpack_flexbison or not os.path.exists(flex_target_dir + '/win-flex.exe' ):
		flex_archive = zipfile.ZipFile(flex_target, 'r')
		print flex_archive.extractall(flex_target_dir)
		#os.rename(flex_target_dir + '/win_flex.exe', flex_target_dir + '/flex.exe')
		#os.rename(flex_target_dir + '/win_bison.exe', flex_target_dir + '/bison.exe')
		print("Unpacking flex")
	else:
		print("Flex already unpacked, skipping")

	# extend path to make open exr build
	os.environ["PATH"] += os.pathsep + os.path.abspath('install/lib')
	# Build phases
	make_dir_safe(build_dir)
	cmake_generator_string = '-G \"Visual Studio %d %d Win%d\"' % (msvcver, msvcyear, architecture)
	for i in range(len(build_phases)):
		build, cmake_params = build_phases[i]
		if build:
			phase_idx = i + 1
			print('Generating build project for phase%d' % phase_idx)
			phase_dir = '%s/phase%d' %  (build_dir, phase_idx)
			make_dir_safe(phase_dir)
			os.chdir(phase_dir)
			# apply patches
			for patch in patches[i]:
				apply_patch(patch)
			res = subprocess.call('cmake ../../phase%d %s %s' %(phase_idx, cmake_params, cmake_generator_string))
			if not res == 0:
				print('Failed to cmake phase%d' % phase_idx)
				return
			print('Building phase%d' % phase_idx)
			res = subprocess.call('%s %s /Build %s /project %s /projectconfig %s' % (devenv_path, os.path.abspath("Project.sln"), build_config, os.path.abspath("install.vcxproj"), build_config))
			if not res == 0:
				print ("Failed to build phase%d" % phase_idx)
				return
			os.chdir('../..')

	# Now copy all dll's to the bin directory so we can actually run stuff
	for f in glob.glob('install/lib/*.dll'):
		print('Copying %s' % f)
		shutil.copy(f, 'install/bin')
	for f in glob.glob('downloads/boost/lib64-msvc-%d.0/*.dll' % msvcver):
		print('Copying %s' % f)
		shutil.copy(f, 'install/bin')

if __name__ == "__main__":
    main()

