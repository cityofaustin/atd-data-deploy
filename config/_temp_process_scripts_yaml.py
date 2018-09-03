# convert the old python-docker-cron config dict into yaml and
# upgrade it to new version
# and merge with public config

import yaml
import os
import pdb

from pdc_joey import * # SCRIPT 

#  lookup ref to source/destination based on filename
source_dest_lookup = {
    'pgrest_data_pub.py' : {
        'source' : 'postgrest',
        'destination' : 'socrata'
    },
    'sig_stat_pub.py' : {
        'source' : 'kits',
        'destination' : 'socrata'
    },
    'esb_xml_gen.py' : {
        'source' : 'knack',
        'destination' : 'xml'
    },
    'esb_xml_send.py' : {
        'source' : 'knack',
        'destination' : 'ESB'
    },
    'traffic_reports.py' : {
        'source' : 'rss',
        'destination' : 'postgrest'
    },
    'kits_cctv_push.py' : {
        'source' : 'knack',
        'destination' : 'kits'
    },
    'backup.py' : {
        'source' : 'knack',
        'destination' : 'csv'
    },
    'knack_data_pub.py' : {
        'source' : 'knack',
        'destination' : '#UNKNOWN'
    },
    'bcycle_kiosk_pub.py' : {
        'source' : 'dropbox',
        'destination' : 'agol'
    },
    'bcycle_trip_pub.py' : {
        'source' : 'dropbox',
        'destination' : 'socrata'
    },
    'detection_status_signals.py' : {
        'source' : 'knack',
        'destination' : 'knack'
    },
    'device_status.py' : {
        'source' : 'knack',
        'destination' : 'knack'
    },
    'device_status_log.py' : {
        'source' : 'knack',
        'destination' : 'knack'
    }

}


def extract_filename(arg_list):
    #  extract filename from args
    for arg in arg_list:
        if '.py' in arg:
            filename = arg
            arg_list.remove(arg)

    return arg_list, filename


def extract_from_args(arg_list):
    for arg in arg_list:
        if '-d' in arg:
            return arg.replace('-d', '').strip()
    return None

def get_source_dest(filename, lookup, attrib):
    if lookup.get(filename):
        return lookup[filename].get(attrib)
    else:
        return '#NOTFOUND'


redux = {}

for script in SCRIPTS:
    # set name value as key
    name = script.pop('name')

    # copy script entry to modify as needed
    redux[name] = dict(script)

    redux[name]['init_func'] = 'main' # new param
    redux[name]['job'] = True # new param

    #  rename 'workdir' and make relative to launcher
    redux[name]['path'] = redux[name].pop('workdir')
    redux[name]['path'] = os.path.join('../', redux[name]['path'])

    #  extract filename from args and set as key/value
    if redux[name].get('args'):
        redux[name]['args'], filename = extract_filename(redux[name]['args'])
        redux[name]['filename'] = filename

    #  remove empty arg entries after handling
    if 'args' in redux[name] and not redux[name]['args']:
        redux[name].pop('args')
    
    #  extract destination value from args
    if redux[name].get('args'):
        destination = extract_from_args(redux[name]['args'])
        if destination:
            redux[name]['destination'] = destination
    
    # try to lookup source/destination
    if not redux[name].get('destination'):
        redux[name]['destination'] = get_source_dest(redux[name]['filename'], source_dest_lookup, 'destination')

    redux[name]['source'] = get_source_dest(redux[name]['filename'], source_dest_lookup, 'source')



with open('processed.yml', 'w') as fout:
    yaml.dump(redux, fout, default_flow_style=False)









