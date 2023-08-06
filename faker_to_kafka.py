import json
import time
from tqdm.notebook import tqdm
from kafka import KafkaProducer
from faker import Faker
fake = Faker()

# Please, create topic before producing

bootstrap_servers = ['localhost:9092']
topicname = 'registered_profile'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)

n = 5000
for _ in tqdm(range(n)):
     # gen data
     profile = fake.profile()

     # pre-process
     loc = profile['current_location']
     profile['current_location'] = (float(loc[0]), float(loc[1]))
     profile['birthdate'] = str(profile['birthdate'])

     # produce
     value = json.dumps(profile).encode('utf-8')
     key = str(profile['ssn']).encode('utf-8')
     ack = producer.send(topicname, value, key=key)

     time.sleep(0.1)