import json
import random

def generate_data():
    directions = ['Front', 'Right', 'Left', 'Rear']
    terrains = ['clear space', 'clear space', 'low rocks', 'crater', 'dust clouds', 'high rocks']
    base_directions = ['front', 'front-right', 'right', 'rear-right', 'rear', 'rear-left', 'left', 'front-left']
    container_statuses = ['full', 'empty']

    data = []
    for direction in directions:
        terrain = random.choice(terrains)
        # 1/7 chance to have mineral, except for dust clouds
        if random.randint(1, 7) == 1 and terrain != 'dust clouds':
            terrain += ', mineral'
        data.append(f"{direction}: {terrain}")
    data.append(f"container: {random.choice(container_statuses)}")
    data.append(f"base: {random.choice(base_directions)}")

    return json.dumps({"input": ', '.join(data)})

print('\n'.join(generate_data() for _ in range(10)))
