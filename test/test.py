import random

css_rules = []

for i in range(1, 151):
    left = random.randint(0, 100)
    animation_duration = random.randint(4, 10)
    animation_delay = random.randint(0, 5)
    css_rules.append(f".rain:nth-child({i}) {{ top: -50%; left: {left}%; animation-duration: {animation_duration}s; animation-delay: {animation_delay}s; }}")

css_output = "\n".join(css_rules)

# Save the output to a .txt file at the root directory
with open('e:/My_GitHub_Repos/playground-2.0/test/output.txt', 'w') as file:
    file.write(css_output)
