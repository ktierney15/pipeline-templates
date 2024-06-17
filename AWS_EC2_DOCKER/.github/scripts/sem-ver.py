"""
File: versioning.py
Author: Kevin Tierney
Description: This script performs sematic versioning

To use this script, you just need to pass in the version type (major, minor, or patch) and the current version.
examples: 
    python3 sem-ver.py 'patch' 'v1.2.1' -> output: 'v1.2.2'
    python3 sem-ver.py 'minor' 'v1.2.1' -> output: 'v1.3.0'
    python3 sem-ver.py 'major' 'v1.2.1' -> output: 'v2.0.0'
    
"""



import argparse

def create_new_version(version_type: str, current_version: str) -> str:
    contains_v = False
    if current_version[0].lower() == 'v':
        contains_v = True
        current_version = current_version[1:]

    version_split = current_version.split(".")

    if version_type == 'major':
        version_split[0] = str(int(version_split[0]) + 1)
        version_split[1] = "0"
        version_split[2] = "0"
    elif version_type == 'minor':
        version_split[1] = str(int(version_split[1]) + 1)
        version_split[2] = "0"
    elif version_type == 'patch':
        version_split[2] = str(int(version_split[2]) + 1) 

    rejoined_version = '.'.join(version_split)

    if contains_v:
        rejoined_version = "v" + rejoined_version
    
    return rejoined_version

def main():
    parser = argparse.ArgumentParser(description='Arguments needed to version your application')
    parser.add_argument('version_type', choices=['major', 'minor', 'patch'], help='Version type to create: Major, Minor, or Patch')
    parser.add_argument('current_version', type=str, help='First operand')
    args = parser.parse_args()

    print(create_new_version(args.version_type, args.current_version))

    return create_new_version(args.version_type, args.current_version)

if __name__ == "__main__":
    main()