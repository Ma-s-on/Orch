import docker, yaml, logging
from time import sleep

logging.basicConfig(filename='logs/orchestrator.log', level=logging.INFO)
client = docker.from_env()

def load_services(path='config/services.yml'):
    with open(path) as f:
        return yaml.safe_load(f)

def monitor(services):
    while True:
        for svc in services:
            try:
                c = client.containers.get(svc['name'])
                if c.status != 'running':
                    logging.info(f"Restarting {svc['name']}")
                    c.restart()
            except Exception as e:
                logging.error(f"{svc['name']} issue: {e}")
        sleep(30)

if __name__ == '__main__':
    monitor(load_services())
