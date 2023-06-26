import json
import threading
from flask import Flask, jsonify, request, render_template
import yaml

app = Flask(__name__)
nornir_data = None  # Global variable to store Nornir data
groups_data = []  # List to store groups data
hosts_data = []  # List to store hosts data

def run_nornir_tasks():
    global nornir_data

    from nornir import InitNornir
    from nornir_utils.plugins.tasks.data import load_yaml
    from nornir_utils.plugins.functions import print_result, print_title
    from nornir_netmiko.tasks import netmiko_send_command
    from nornir.core.filter import F
    from nornir.core.exceptions import NornirExecutionError

    nr = InitNornir(config_file="config.yaml", dry_run=True)

    result = nr.run(task=netmiko_send_command, command_string="show run", enable=True)
    nornir_data = result
    print(nornir_data)

def start_nornir_tasks():
    global groups_data, hosts_data

    if not groups_data or not hosts_data:
        print("Groups or hosts data is missing. Please save the necessary data.")
        return

    thread = threading.Thread(target=run_nornir_tasks)
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_groups_yaml', methods=['POST'])
def save_groups_yaml():
    global groups_data
    groups_data.append(request.form.get('groupsData'))
    groups_dicts = [yaml.safe_load(data) for data in groups_data]
    with open('groups.yaml', 'w') as file:
        for group_dict in groups_dicts:
            yaml.dump(group_dict, file)
    start_nornir_tasks()  # Start Nornir tasks after saving groups data
    return 'Groups.yaml saved'

@app.route('/save_hosts_yaml', methods=['POST'])
def save_hosts_yaml():
    global hosts_data
    hosts_data.append(request.form.get('hostsData'))
    hosts_dicts = [yaml.safe_load(data) for data in hosts_data]
    with open('hosts.yaml', 'w') as file:
        for host_dict in hosts_dicts:
            yaml.dump(host_dict, file)
    start_nornir_tasks()  # Start Nornir tasks after saving hosts data
    return 'Hosts.yaml saved'

@app.route('/get_hosts_yaml', methods=['GET'])
def get_hosts_yaml():
    hosts_yaml = None

    with open('hosts.yaml', 'r') as file:
        hosts_yaml = file.read()

    return jsonify({'hosts_yaml': hosts_yaml})

@app.route('/get_groups_yaml', methods=['GET'])
def get_groups_yaml():
    groups_yaml = None

    with open('groups.yaml', 'r') as file:
        groups_yaml = file.read()

    return jsonify({'groups_yaml': groups_yaml})

@app.route('/get_nornir_data', methods=['GET'])
def get_nornir_data():
    global nornir_data, groups_data, hosts_data

    if nornir_data is None:
        return 'Nornir tasks are not yet executed. Please wait for the tasks to complete.'

    nornir_data_json = json.dumps(nornir_data, default=str, indent=4)
    groups_data_json = json.dumps(groups_data, default=str, indent=4)
    hosts_data_json = json.dumps(hosts_data, default=str, indent=4)

    return jsonify({'nornir_data': nornir_data_json, 'groups_data': groups_data_json, 'hosts_data': hosts_data_json})

if __name__ == '__main__':
    app.run()
