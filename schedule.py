import os
from uuid import uuid4


IS_FUCKING_BROKEN = True


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
    if file.endswith('.mcfunction'):
      file_path = os.path.join(root, file)
      
      with open(file_path) as file:
        lines = file.readlines()

        if not schedule_dir_nuked:
          schedule_func_path = root.split('function\\')[0] + f'{'\\function' if not IS_FUCKING_BROKEN else ''}\\_schedule\\'
          clean_schedule_dir(schedule_func_path)
        schedule_dir_nuked = True
        
        scheduled_names = []
        i = -1
        for line in lines:
          i += 1
          if ' schedule function ' in line and ' as @s ' in line:
            line = line.replace(' as @s', '')
            if (x := 'execute run ') in line:
              line = line.replace(x, '')
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
                f'schedule function {schedule_func_path.split('\\')[(3 if IS_FUCKING_BROKEN else 2)]}:_schedule/{schedule_uuid} {ticks}{replace_append}'
              ])
              
            with open(f'{os.path.join(schedule_func_path, schedule_uuid)}.mcfunction', 'w') as file:
              file.writelines([
                f'execute as @e[tag={tag_uuid}] run function {original_line.split()[-1]}\n',
                f'tag @e remove {tag_uuid}'
              ])
              
            new_command = original_line.split()
            new_command[-1] = f'{schedule_func_path.split('\\')[(3 if IS_FUCKING_BROKEN else 2)]}:_schedule/{func_uuid}'
            new_command = ' '.join(new_command)
            
            lines[i] = new_command + '\n'
            scheduled_names.append(dict(name = original_line.split()[-1], uuid = schedule_uuid, tag = tag_uuid))
            
          elif ' schedule clear ' in line and ' as @s ' in line:
            line = line.replace(' as @s', '')
            if (x := 'execute run ') in line:
              line = line.replace(x, '')
            if (name := line.split()[-1]) in [d['name'] for d in scheduled_names]:
              lines[i] = line.replace(name, f'{schedule_func_path.split('\\')[(3 if IS_FUCKING_BROKEN else 2)]}:_schedule/{(this_scheduled_name := ([dict(uuid = d['uuid'], tag = d['tag']) for d in scheduled_names if d['name'] == name][0]))['uuid']}')
              before_schedule = line.split(' schedule clear')[0]
              lines.insert(i + 1, before_schedule + f' tag @e remove {this_scheduled_name['tag']}\n')
          
      with open(file_path, 'w') as file:
        file.writelines(lines)
