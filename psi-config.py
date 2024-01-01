#!/usr/bin/env python3

import sys
import os
import argparse
import configparser
import json
import datetime

if __name__ == "__main__":
    # read command line arguments
    parser = argparse.ArgumentParser(description = 'psioniq configuration json script')
    parser.add_argument('-c', '--config', default='psi-config.ini', help = 'specify configuration file')
    parser.add_argument('-s', '--section', default='default', help = 'specify section of configuration file')
    parser.add_argument('-o', '--output', default='psi-config-out.json', help = 'specify output json file')
    parser.add_argument('-l', '--license', default='default', help = 'specify license file by default if not provided in ini config')
    args = parser.parse_args()

    args.license = 'licenses/' + args.license + '.txt'

    # check arguments
    if not args.config:
        print('Error: no configuration file specified')
        sys.exit(1)

    if not args.section:
        print('Error: no section specified')
        sys.exit(1)

    if not args.output:
        print('Error: no output file specified')
        sys.exit(1)

    # check files
    if os.access(args.config, os.R_OK) == False:
        print('Error: configuration file {} cannot be read'.format(args.config))
        sys.exit(1)

    if os.access(args.license, os.R_OK) == False:
        print('Error: license file {} cannot be read'.format(args.license))
        sys.exit(1)

    if os.path.exists(args.output) == True:
        if os.access(args.output, os.W_OK) == False:
            print('Error: output file {} cannot be written'.format(args.output))
            sys.exit(1)

    # read ini config file
    iniconfig = configparser.ConfigParser()
    iniconfig.read(args.config)

    sections = iniconfig.sections()
    if args.section not in sections:
        print('Error: section {} not found in {}'.format(args.section, args.config))
        sys.exit(1)

    iniconfig_dict = {}
    for section in sections:
        if section == args.section:
            options = iniconfig.options(section)
            for option in options:
                iniconfig_dict[option] = iniconfig.get(section, option)

    # post-parse ini config file and default values
    year = datetime.datetime.now().year

    holder_list = []
    year_list = []

    if 'year' in iniconfig_dict:
        year = iniconfig_dict['year']

    if 'license' in iniconfig_dict:
        args.license = 'licenses/' + iniconfig_dict['license'] + '.txt'

    for i in range(0, 8):
        holder_key = 'holder' + str(i)
        year_key = 'year' + str(i)
        if (holder_key in iniconfig_dict) and (iniconfig_dict[holder_key] != ''):
            holder_list.append(iniconfig_dict[holder_key])
            if (year_key in iniconfig_dict) and (iniconfig_dict[year_key] != ''):
                year_list.append(iniconfig_dict[year_key])
            else:
                year_list.append(year)

    max_year_len = max(len(str(year)) for year in year_list)

    for i in range(0, len(year_list)):
        year_list[i] = str(year_list[i]) + ' ' * (max_year_len - len(str(year_list[i])))

    # construct license text
    license_text = []

    for i in range(0, len(holder_list)):
        license_text.append('Copyright (c) {} {}'.format(year_list[i], holder_list[i]))

    with open(args.license, 'r', encoding='utf-8') as flicense:
        license_text.extend(flicense.readlines())

    for i in range(0, len(license_text)):
        license_text[i] = license_text[i].rstrip('\n').rstrip('\r')

    # update output json file
    if os.path.exists(args.output) == True:
        with open(args.output, 'r', encoding='utf-8') as fjson:
            json_content = json.load(fjson)
    else:
        json_content = {}

    #### json content update ####
    json_content.update({'psi-header.config' : {
        'forceToTop': True,
        'blankLinesAfter': 2,
        'license': 'Custom' 
    }})

    json_content.update({'psi-header.license-text' : license_text})

    json_content.update({'psi-header.lang-config' : [
        {
            'language': '*',
            'begin': '/**',
            'end': ' */',
            'prefix': ' * '
        }
    ]})

    json_content.update({'psi-header.templates' : [
        {
            'language': '*',
            'template': [
                '<<licensetext>>'
            ]
        }
    ]})
    ########

    with open(args.output, 'w', encoding='utf-8') as fjson:
        json.dump(json_content, fjson, indent=4)

