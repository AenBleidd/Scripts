import os
import sys
import zipfile

from pathlib import Path

def get_vcpkg_archives_list(vcpkg_path):
    for path, _, files in os.walk(vcpkg_path):
        for file in files:
            if file.endswith(".zip"):
                file_path = os.path.join(path, file)
                yield file_path

def read_control(control):
    package = ''
    version = '0'
    port_version = '0'
    architecture = ''
    lines = control.split('\n')
    for line in lines:
        if (line != ''):
            pair = line.split(': ')
            if (pair[0] == 'Package'):
                package = pair[1]
            elif (pair[0] == 'Version'):
                version = pair[1]
            elif (pair[0] == 'Port-Version'):
                port_version = pair[1]
            elif (pair[0] == 'Architecture'):
                architecture = pair[1]
    return package, version + '-' + port_version, architecture

def get_packages(archives):
    packages = {}
    for archive in archives:
        zip_file = zipfile.ZipFile(archive, 'r')
        control = zip_file.read('CONTROL')
        package, version, architecture = read_control(control.decode('utf-8'))
        if (architecture not in packages.keys()):
            packages[architecture] = {}
        if (package not in packages[architecture].keys()):
            packages[architecture][package] = {}
        if (version not in packages[architecture][package].keys()):
            packages[architecture][package][version] = []
        if (archive not in packages[architecture][package][version]):
            packages[architecture][package][version].append(archive)
    return packages

def print_packages(packages):
    for architecture in packages:
        print(architecture)
        for package in packages[architecture]:
            print('\t', package)
            for version in packages[architecture][package]:
                print('\t\t', version)
                for archive in packages[architecture][package][version]:
                    print('\t\t\t', archive)

def mark_outdated_packages(packages):
    outdated = []
    for architecture in packages:
        for package in packages[architecture]:
            archives_with_same_version = {}
            max_version = sorted(packages[architecture][package].keys(), reverse=True)[0]
            for version in packages[architecture][package]:
                if (version != max_version):
                    for archive in packages[architecture][package][version]:
                        outdated.append(archive)
                else:
                    if (len(packages[architecture][package][version]) == 1):
                        continue
                    for archive in packages[architecture][package][version]:
                        archives_with_same_version[os.path.getmtime(archive)] = archive
                    max_date = sorted(archives_with_same_version.keys(), reverse=True)[0]
                    for archive in packages[architecture][package][version]:
                        if (archive != archives_with_same_version[max_date]):
                            outdated.append(archive)
    return outdated

def get_hash_from_name(name):
    return Path(name).stem

def get_hash_list(packages):
    hash_list = []
    for architecture in packages:
        for package in packages[architecture]:
            for version in packages[architecture][package]:
                for archive in packages[architecture][package][version]:
                  hash_list.append(get_hash_from_name(os.path.basename(archive)))
    return hash_list

def remove_outdated_from_hash_list(hash_list, outdated):
    for package in outdated:
        package_hash = get_hash_from_name(os.path.basename(package))
        if (package_hash in hash_list):
            hash_list.remove(package_hash)

def read_vcpkg_abi_info_content(content, packages):
    dependencies = []
    lines = content.split('\n')
    for line in lines:
        if line:
            pair = line.split(' ')
            if (pair[0] in packages):
                dependencies.append(pair[1])
    return dependencies

def read_vcpkg_abi_info(archive, package, packages):
    zip_file = zipfile.ZipFile(archive, 'r')
    if (package == 'gtest'):
        package = 'GTest'
    file_name = 'share/'+package+'/vcpkg_abi_info.txt'
    try:
        info_file = zip_file.read(file_name)
        return read_vcpkg_abi_info_content(info_file.decode('utf-8'), packages)
    except Exception as ex:
        print('Failed to read the file', file_name, 'from', archive, ':', ex)
        return ''

def mark_duplicate_packages(packages, outdated):
    hash_list = get_hash_list(packages)
    remove_outdated_from_hash_list(hash_list, outdated)

    for architecture in packages:
        dependencies_list = {}
        for package in packages[architecture]:
            for version in packages[architecture][package]:
                for archive in packages[architecture][package][version]:
                    dependencies = read_vcpkg_abi_info(archive, package, packages[architecture].keys())
                    if (len(dependencies) != 0):
                        dependencies_list[get_hash_from_name(os.path.basename(archive))] = dependencies
        process_dependencies_list(dependencies_list, packages, outdated, hash_list, architecture)

def add_package_to_outdated_by_hash(packages, outdated, package_hash, architecture):
    for package in packages[architecture]:
        for version in packages[architecture][package]:
            for archive in packages[architecture][package][version]:
                if (get_hash_from_name(os.path.basename(archive)) == package_hash and archive not in outdated):
                    outdated.append(archive)
                    return

def process_package_dependencies(package_hash, dependencies, packages, outdated, hash_list, architecture):
    is_valid = True
    if (package_hash not in hash_list):
        add_package_to_outdated_by_hash(packages, outdated, package_hash, architecture)
        is_valid = False
    if (package_hash not in dependencies):
        return is_valid
    package_dependencies = dependencies[package_hash]
    for dependency_hash in package_dependencies:
        is_valid = is_valid and process_package_dependencies(dependency_hash, dependencies, packages, outdated, hash_list, architecture)
    if (not is_valid):
        add_package_to_outdated_by_hash(packages, outdated, package_hash, architecture)
        if (package_hash in hash_list):
            hash_list.remove(package_hash)
        return False
    return is_valid

def process_dependencies_list(dependencies, packages, outdated, hash_list, architecture):
    for package_hash in dependencies:
        process_package_dependencies(package_hash, dependencies, packages, outdated, hash_list, architecture)

def print_outdated(outdated, packages):
    for architecture in packages:
        for package in packages[architecture]:
            for version in packages[architecture][package]:
                for archive in packages[architecture][package][version]:
                    if (archive in outdated):
                        print(architecture, package, version, archive, sep=' -> ')

def remove_outdated(outdated):
    for archive in outdated:
        os.remove(archive)

def help():
    print('Usage: python CleanVcpkgArchive.py <vcpkg_archive_path>')

if(len(sys.argv) != 2):
    help()
    exit(1)

vcpkg_path = sys.argv[1]

vcpkg_archives_list = get_vcpkg_archives_list(vcpkg_path)
vcpkg_packages = get_packages(vcpkg_archives_list)
print_packages(vcpkg_packages)
outdated = mark_outdated_packages(vcpkg_packages)
mark_duplicate_packages(vcpkg_packages, outdated)
print('Outdated packages:')
print_outdated(outdated, vcpkg_packages)
remove_outdated(outdated)
