import regex
import re
import os
from uuid import uuid4
from copy import deepcopy

def extract_outer_braces(s, b):
  if b == '{}':
    pattern = r'{(?:[^{}]+|(?R))*}'
  elif b == '[]':
    pattern = r'{(?:[^[]]+|(?R))*}'
  else:
    return ''
  return regex.search(pattern, s).group(0)

def remove_between_strings(original_string, substring1, substring2, keep_the_second_substr):
    pattern = rf'{re.escape(substring1)}(.*?){re.escape(substring2)}'
    return re.sub(pattern, substring2 if keep_the_second_substr else '', original_string)
  
  
def clean_schedule_dir(schedule_func_path):
  try:
    if len(filenames := os.listdir(schedule_func_path)) != 0:
      for filename in filenames:
        os.remove(os.path.join(schedule_func_path, filename))
  except FileNotFoundError:
    os.makedirs(schedule_func_path)


schedule_func_path = ''
schedule_dir_nuked = False
for root, _dirs, files in os.walk('.'):
  for file in files:
    if file.endswith('.mcfx') or file.endswith('.mcfunctionx'):
      file_path = os.path.join(root, file)
      
      with open(file_path) as file:
        lines = file.readlines()
        
        i = -1
        for line in lines:
          i += 1
          if line.startswith('#'):
            continue          
          if not (' summon' in line and not line.startswith('summon') and 'run summon' not in line):
            continue
          
          new_commands = ['', '', '']
          nbt = extract_outer_braces(line.split(' summon ', 1)[1], '{}')
          entity = line.split(' summon ', 1)[1].split('{')[0]
          old_command = line.split(' run ', 1)[1]
          uuid = str(uuid4())
          if 'Tags:["' not in nbt:
            new_commands[0] = remove_between_strings(line.replace(old_command, f'summon {entity} ~ ~ ~ {{Tags:["{uuid}"],{nbt.split('{', 1)[1]}'), f' summon {entity}{nbt}', ' run', True)
          else:
            new_nbt_1, new_nbt_2 = nbt.split('Tags:[', 1)
            new_commands[0] = remove_between_strings(line.replace(old_command, f'summon {entity} ~ ~ ~ {new_nbt_1}Tags:["{uuid}",{new_nbt_2}'), f' summon {entity}{nbt}', ' run', True)
          new_commands[1] = f'execute as @e[tag={uuid}]{line.split(f' summon {entity}{nbt}', 1)[1]}'
          new_commands[2] = f'tag @e[tag={uuid}] remove {uuid}'
          
          lines[i] = new_commands[0] + '\n'
          lines.insert(i + 1, new_commands[1])
          lines.insert(i + 2, new_commands[2] + '\n')
        
        
        if not schedule_dir_nuked:
          schedule_func_path = root.split('function\\')[0] + '\\_schedule\\'
          clean_schedule_dir(schedule_func_path)
        schedule_dir_nuked = True
        i = -1
        for line in lines:
          i += 1
          if 'schedule function ' not in line:
            continue
            
          tag_uuid = str(uuid4())
          func_uuid = str(uuid4())
          schedule_uuid = str(uuid4())
          ticks = line.split('schedule ', 1)[1].split()[-2 if line.endswith('replace\n') or line.endswith('append\n') else -1]
          replace_append = ' replace' if line.endswith('replace\n') else ' append' if line.endswith('append\n') else ''
          original_line = line.replace('schedule ', '', 1).replace(' append', '').replace(' replace', '').split()
          original_line.remove(original_line[-1])
          original_line = ' '.join(original_line)
          
          with open(f'{os.path.join(schedule_func_path, func_uuid)}.mcfunction', 'w') as file:
            file.writelines([
              f'tag @s add {tag_uuid}\n',
              f'schedule function {schedule_func_path.split('\\')[2]}:_schedule/{schedule_uuid} {ticks}{replace_append}'
            ])
            
          with open(f'{os.path.join(schedule_func_path, schedule_uuid)}.mcfunction', 'w') as file:
            file.writelines([
              f'execute as @e[tag={tag_uuid}] run function {original_line.split()[-1]}\n',
              f'tag @e[tag={tag_uuid}] remove {tag_uuid}'
            ])
            
          new_command = original_line.split()
          new_command[-1] = f'{schedule_func_path.split('\\')[2]}:_schedule/{func_uuid}'
          new_command = ' '.join(new_command)
          
          lines[i] = new_command + '\n'
          
      with open(file_path.replace('.mcfx', '.mcfunction'), 'w') as file:
        file.writelines(lines)
