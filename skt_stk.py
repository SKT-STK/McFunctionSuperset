from beet import Context, Function
from uuid import uuid4
import regex

class Schedule():
  def __init__(self, ctx: Context):
    scheduled = []
    for name, func in list(ctx.data.functions.items()):
      schedules = -1
      clears = -1
      i = -1
      for line in func.lines:
        i += 1
        if ' as @s ' in line and ' schedule function ' in line:
          if line.endswith('clear'):
            continue
          
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

class Anchored():
  def __init__(self, ctx):
    for func in list(ctx.data.functions.values()):
      i = -1
      for line in func.lines:
        i += 1
        
        if (anch := ' anchored eyes ') in line and 'positioned ^' not in line.split(anch, 1)[1]:
          func.lines[i] = line.replace(anch, f'{anch}positioned ^ ^ ^ ')

class Inline():
  def __init__(self, ctx: Context):
    self.ctx = ctx
  
  def get_indent(self, string: str) -> int:
    return len(string) - len(string.lstrip())
  
  def macro(self):
    for name, func in list(self.ctx.data.functions.items()):
      macros = []
      has_parent = False
      for i, line in enumerate(func.lines):
        if line.startswith('# ') or line.replace(' ', '') == '': continue
        if not (
          (
            'function(with entity ' in line
            or 'function(with block ' in line
            or 'function(with storage ' in line
            or 'function({' in line
          )
          and line.endswith('):')
        ):
          if has_parent and self.get_indent(line) > (cur_parent := macros[-1])['parent_indent']:
            cur_parent['indent_block'].append(dict(
              line = line[cur_parent['parent_indent']:],
              index = i
            ))
          else:
            if has_parent:
              has_parent = False
          continue
        
        macros.append(dict(
          parent_index = i,
          parent_indent = self.get_indent(line),
          indent_block = [],
          macro_with = line.split('function(')[1][:-2]
        ))
        
        has_parent = True
      
      reversed_macros = macros
      reversed_macros.reverse()
      for i, macro in enumerate(reversed_macros):
        func.lines[macro['parent_index']] = func.lines[macro['parent_index']].split('function(')[0] + f'function {(macro_name := f'{name}/macro_{i}')} {macro['macro_with']}'
        
        line_indexes_reversed = [inner_macro['index'] for inner_macro in macro['indent_block']]
        line_indexes_reversed.reverse()
        for line_index in line_indexes_reversed:
          func.lines.pop(line_index)
        
        self.ctx.data[macro_name] = Function([inner_macro['line'] for inner_macro in macro['indent_block']])
  
  def schedule(self):
    for name, func in list(self.ctx.data.functions.items()):
      schedules = []
      has_parent = False
      for i, line in enumerate(func.lines):
        if line.startswith('# ') or line.replace(' ', '') == '': continue
        if not regex.match(r'^\s*function\(([1-9]\d*(?:[tsd])?)\):', line):
          if has_parent and self.get_indent(line) > (cur_parent := schedules[-1])['parent_indent']:
            cur_parent['indent_block'].append(dict(
              line = line[cur_parent['parent_indent']:],
              index = i
            ))
          else:
            if has_parent:
              has_parent = False
          continue
        
        schedules.append(dict(
          parent_index = i,
          parent_indent = self.get_indent(line),
          indent_block = [],
          schedule_time = line.split('function(')[1][:-2]
        ))
        
        has_parent = True
      
      reversed_schedules = schedules
      reversed_schedules.reverse()
      for i, schedule in enumerate(reversed_schedules):
        func.lines[schedule['parent_index']] = func.lines[schedule['parent_index']].split('function(')[0] + f'schedule function {(schedule_name := f'{name}/schedule_{i}')} {schedule['schedule_time']}'
        
        line_indexes_reversed = [inner_schedule['index'] for inner_schedule in schedule['indent_block']]
        line_indexes_reversed.reverse()
        for line_index in line_indexes_reversed:
          func.lines.pop(line_index)
        
        self.ctx.data[schedule_name] = Function([inner_schedule['line'] for inner_schedule in schedule['indent_block']])
  
  def execute_if(self):
    for name, func in list(self.ctx.data.functions.items()):
      macros = []
      has_parent = False
      for i, line in enumerate(func.lines):
        if line.startswith('# ') or line.replace(' ', '') == '': continue
        if not (
          'function()' in line
          and line.endswith('):')
        ):
          if has_parent and self.get_indent(line) > (cur_parent := macros[-1])['parent_indent']:
            cur_parent['indent_block'].append(dict(
              line = line[cur_parent['parent_indent']:],
              index = i
            ))
          else:
            if has_parent:
              has_parent = False
          continue
        
        macros.append(dict(
          parent_index = i,
          parent_indent = self.get_indent(line),
          indent_block = []
        ))
        
        has_parent = True
      
      reversed_macros = macros
      reversed_macros.reverse()
      for i, macro in enumerate(reversed_macros):
        func.lines[macro['parent_index']] = func.lines[macro['parent_index']].split('function(')[0] + f'function {(macro_name := f'{name}/execute_if_{i}')}'
        
        line_indexes_reversed = [inner_macro['index'] for inner_macro in macro['indent_block']]
        line_indexes_reversed.reverse()
        for line_index in line_indexes_reversed:
          func.lines.pop(line_index)
        
        self.ctx.data[macro_name] = Function([inner_macro['line'] for inner_macro in macro['indent_block']])
      
      continuation_lines = func.lines
      for i, line in enumerate(continuation_lines):
        if line.lstrip().startswith(';'):
          func.lines[i-1] += line.lstrip().replace(';', ' ')
          func.lines.pop(i)


def schedule(ctx: Context):
  Schedule(ctx)

def anchored(ctx: Context):
  Anchored(ctx)

def inline(ctx: Context):
  inline = Inline(ctx)
  inline.macro()
  inline.schedule()
  inline.execute_if()
