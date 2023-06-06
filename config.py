import yaml

with open("./config.yml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        jobs = data['release']['1.0.0']['jobs']
        print(jobs)
    except yaml.YAMLError as exc:
        print(exc)
