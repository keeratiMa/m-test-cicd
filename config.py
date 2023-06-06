import argparse
import sys

import yaml


def get_job_config(config, job):
    return config['config'][job]


def build_cmd(job_config):
    jar_prefix = "nest-stream-flink-"
    cmd = f"sh deploy.sh -n {job_config['name']} -ns {job_config['namespace']} -e {job_config['env']} -jar {jar_prefix}{job_config['version']}.jar --config={job_config['config']}"

    return cmd


def main(param):
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-e", help="env", required=True)

    args = argParser.parse_args()
    print("-----args=%s" % args)

    # process default args
    env = args.env
    with open("./config.yml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            jobs = data['release']['1.0.0']['jobs']
            for job in jobs:
                job_config = get_job_config(data, job)
                job_config['env'] = env
                cmd = build_cmd(job_config)
                print(cmd)

        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    print("Python version")
    print(sys.version)
    print("Version info.")
    print(sys.version_info)

    main(sys.argv[1:])
