import urllib
import os
import subprocess


def make_dir_safe(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)


def main():
	download_dir = 'downloads'
	msvcver = 12
	msvcyear = 2013
	architecture = 64
	boost_version = '1.59.0'
	boost_version_ = '1_59_0'
	force_download_boost = False
	force_unpack_boost = False

	build_config = 'Debug'
	build_dir = 'build'
	build_phases = [True, False, False, False, False]
	devenv_path = '\"C:\\Program Files (x86)\\Microsoft Visual Studio %d.0\\Common7\\IDE\\devenv.exe\"' % (msvcver)

	make_dir_safe(download_dir)
	
	# BOOST
	boost_target = download_dir + '/boost.exe'
	if force_download_boost or not os.path.exists(boost_target):
		print("Downloading boost")
		boost_url = 'http://iweb.dl.sourceforge.net/project/boost/boost-binaries/%s/boost_%s-msvc-%d.0-%d.exe' % (boost_version, boost_version_, msvcver, architecture)
		urllib.urlretrieve(boost_url, boost_target)
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
	
	# Build phases
	make_dir_safe(build_dir)
	cmake_generator_string = '-G \"Visual Studio %d %d Win%d\"' % (msvcver, msvcyear, architecture)
	for i in range(len(build_phases)):
		if build_phases[i]:
			phase_idx = i + 1
			phase_dir = '%s/phase%d' %  (build_dir, phase_idx)
			make_dir_safe(phase_dir)
			os.chdir(phase_dir)
			res = subprocess.call('cmake ../../phase%d %s' %(phase_idx, cmake_generator_string))
			if not res == 0:
				print('Failed to cmake phase%d' % phase_idx)
				return
			res = subprocess.call('%s %s /Build %s /project %s /projectconfig %s' % (devenv_path, os.path.abspath("Project.sln"), build_config, os.path.abspath("install.vcxproj"), build_config))
			print('Building phase%d' % phase_idx)
			if not res == 0:
				print ("Failed to build phase%d" % phase_idx)
				return
			os.chdir('../..')



if __name__ == "__main__":
    main()

