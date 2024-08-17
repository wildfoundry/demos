import random
import requests
import time
from datetime import datetime


while True:
    # Generate a random light reading between 0 and 1
    light_level = random.uniform(0, 1)

    measurement_time = datetime.now().strftime("%S:%M:%H %d-%m-%Y")
    
    # Send a POST request to the other script with the light reading
    response = requests.post('http://localhost:8000/record', json={'time': measurement_time, 'reading': light_level})
    
    # Check if the request was successful
    if response.status_code == 200:
        print('Light reading successfully sent')
    else:
        print('Error sending light reading:', response.text)
    
    # Wait for 1 second before sending the next reading
    time.sleep(1)
    