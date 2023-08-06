import datetime
import yaml
from os.path import join, abspath



init_directory = abspath(__file__).split("configs.py")[0]  # "/".join(abspath(__file__).split("/")[:-1]) + "/"


def get_directory(path):
    import ad_execute
    try:
        directory = join(ad_execute.recent_directory, folder_name)
        web = ad_execute.web_port
    except Exception as e:
        directory = path
        web = 7070
    #with open(join(path, "instance.yaml")) as file:
    #    instances = yaml.full_load(file)
    #active_ins = []
    #for ins in instances['instances']:
    #    if ins['active'] is True:
    #        active_ins.append(ins)
    #if len(active_ins) == 0:
    #    directory = init_directory
    #if len(active_ins) == 1:
    #    directory = active_ins[0]['directory']
    #if len(active_ins) > 1:
    #    now = datetime.datetime.now()
    #    directories = list(map(lambda x: ((now - parse(x['date'])).total_seconds(), x['directory']), active_ins))
    #    directory = sorted(directories)[0][1]
    with open(join(directory, "docs", "configs.yaml")) as file:
        config = yaml.full_load(file)
    return config, directory, web

    #with open(join(path, "docs", "configs.yaml")) as file:
    #    config = yaml.full_load(file)
    #if config['directory'] is None:
    #    config['directory'] = init_directory
    #else:
    #    with open(join(config['directory'], "", "docs", "configs.yaml")) as file:
    #        config = yaml.full_load(file)
    #return config, config['directory']


def conf(var):
    config, directory, web = get_directory(init_directory)
    return {
             'data_main_path': join(directory, "", config['data_main_path']),
             'model_main_path': join(directory, "", config['model_main_path']),
             'log_main_path': join(directory, "", config['log_main_path']),
             'docs_main_path': join(directory, "",  config['docs_main_path']),
             'parameters': config['hyper_parameters']['lstm'],
             'parameter_3': config['hyper_parameters']['prophet'],
             'parameters_2': config['hyper_parameters']['iso_f'],
             'parameter_tuning': config['parameter_tuning'],
             'result_file': config['output_file_name'],
             'merged_results': join(directory, "", config['data_main_path'],  config['output_file_name'] + "_" + "".join(str(datetime.datetime.now())[0:10].split("-")) + ".csv"),
             'folder_name': folder_name,
             'available_ports': list(range(int(config['port_ranges'].split("*")[0]),
                                           int(config['port_ranges'].split("*")[1]))),
             'has_param_tuning_first_run': config['has_param_tuning_first_run'],
             'directory': directory,
             'web_port': web,
             'config': {c: config[c] for c in config
                        if c not in
                        ['data_main_path', 'model_main_path', 'log_main_path', 'docs_main_path', 'folder_name']}
    }[var]



alpha = 0.01
iteration = 30
boostrap_ratio = 0.5
treshold = {'lower_bound': 50, 'upper_bound': 2000}
cores = 4
min_weeks = 4
accepted_weeks_after_store_open = 5
accepted_null_ratio = 0.4
year_seconds = 366 * 24 * 60 * 60
time_dimensions = ['year', 'quarter', 'month', 'week', 'week_part', 'week_day', 'hour', 'min', 'second']
weekdays = ['Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays', 'Sundays']
folder_name = 'anomaly_detection_framework'
web_port_default = 7002
