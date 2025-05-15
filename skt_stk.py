from beet import Context, Function
from uuid import uuid4

scheduled = []

def schedule(ctx: Context):
  global scheduled
  for name, func in list(ctx.data.functions.items()):
    schedules = -1
    clears = -1
    i = -1
    for line in func.lines:
      i += 1
      if ' as @s ' in line and ' schedule function ' in line:
        if line.endswith('clear'):
          return
        
        schedules += 1
        
        line = line.replace(' as @s', '')
        if (exec_run := 'execute run ') in line:
          line = line.replace(exec_run, '')
        if line.endswith(' replace'):
          line = ' '.join(line.split()[:-1])

        time = line.split()[-1]
        call_name = line.split()[-2]
        
        player_uuid = str(uuid4())
        
        schedule_1 = f'{name}/schedule_function_{schedules}1'
        schedule_2 = f'{name}/schedule_function_{schedules}2'
        ctx.data[schedule_1] = Function([
          f'tag @s add {player_uuid}',
          f'schedule function {schedule_2} {time}'
        ])
        
        schedule_2_line = f'{''.join(line.split('run ')[:-1])}run function {call_name}'
        if schedule_2_line.startswith('execute '):
          schedule_2_line = schedule_2_line.replace('execute ', f'execute as @e[tag={player_uuid}] ', 1)
        else:
          schedule_2_line = f'execute as @e[tag={player_uuid}] ' + schedule_2_line
        ctx.data[schedule_2] = Function([
          schedule_2_line,
          f'tag @e remove {player_uuid}'
        ])
        
        func.lines[i] = ' '.join(line.replace('schedule ', '').split()[:-2]) + f' {schedule_1}'
        
        scheduled.append(dict(
          original_name = call_name,
          name = schedule_2,
          uuid = player_uuid
        ))
        
      elif ' as @s ' in line and ' schedule clear ' in line:
        clears += 1
        
        line = line.replace(' as @s', '')
        if (exec_run := 'execute run ') in line:
          line = line.replace(exec_run, '')
          
        this_dict = next((d for d in scheduled if d['original_name'] == line.split()[-1]))
        clear_1 = f'{name}/schedule_clear_{schedules}'
        ctx.data[clear_1] = Function([
          f'schedule clear {this_dict['name']}',
          f'tag @e remove {this_dict['uuid']}'
        ])
        
        func.lines[i] = ' '.join(line.replace('schedule clear ', 'function ').split()[:-1]) + f' {clear_1}'

def anchored(ctx: Context):
  for func in list(ctx.data.functions.values()):
    i = -1
    for line in func.lines:
      i += 1
      
      if (anch := ' anchored eyes ') in line and 'positioned ^' not in line.split(anch, 1)[1]:
        func.lines[i] = line.replace(anch, f'{anch}positioned ^ ^ ^ ')
