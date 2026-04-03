"""修复neuron.py中的拼写错误"""

import re

file_path = r"c:\Users\X1882\Desktop\github\skill-time\random_agent\brain_inspired\neuron.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('spiike_history', 'spike_history')
content = content.replace('spiike_queue', 'spike_queue')
content = content.replace('spiike_threshold', 'spike_threshold')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 修复完成")
