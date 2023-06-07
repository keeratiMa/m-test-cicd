import argparse
import subprocess
import sys

import yaml


def get_job_config(config, job):
    return config['config'][job]


def build_cmd(job_config):
    jar_prefix = "nest-stream-flink-"
    cmd = f"sh deploy.sh -n {job_config['name']} -ns {job_config['namespace']} -e {job_config['env']} -jar {jar_prefix}{job_config['version']}.jar --config={job_config['config']}"

    return cmd

def run_os_command(cmd):
    print("===== cmd: ", cmd)
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("===== output: ", output)
    output = output.stdout
    print("===== output stdout: ", output)
    return output

def main(param):
    branch_env_map = {
        "refs/heads/main": ["green", "red"]
    }
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-b", "--branch", help="branch", required=True)
    argParser.add_argument("-jv", "--jar_version", help="jar_version", required=True)

    args = argParser.parse_args()
    print("-----args=%s" % args)

    # process default args
    envs = branch_env_map[args.branch]
    jar_version = args.jar_version
    with open("./release.yml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            no_snapshot_version = jar_version.replace("-SNAPSHOT", "")
            print("no_snapshot_version=" + no_snapshot_version)
            jobs = data['release'][no_snapshot_version]['jobs']
            for job in jobs:
                for env in envs:
                    job_config = get_job_config(data, job)
                    job_config['env'] = env
                    job_config['version'] = jar_version
                    cmd = build_cmd(job_config)

                    run_os_command(cmd)


        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    print("Python version")
    print(sys.version)
    print("Version info.")
    print(sys.version_info)

    main(sys.argv[1:])
