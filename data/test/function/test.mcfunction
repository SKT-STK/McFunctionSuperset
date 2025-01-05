execute as @p at @s positioned ^ ^2 ^5 run summon armor_stand ~ ~ ~ {Tags:["945cee03-9821-46d3-9df9-7973895af41f","yes"],ArmorItems:[{},{},{},{id:dirt}]}
execute as @e[tag=945cee03-9821-46d3-9df9-7973895af41f] at @s anchored eyes run particle totem_of_undying ~ ~ ~ 1 1 1 0.01 100 normal @a
tag @e[tag=945cee03-9821-46d3-9df9-7973895af41f] remove 945cee03-9821-46d3-9df9-7973895af41f

# tp @s ~ ~5 ~
say lol xd

execute as @p at @s run summon armor_stand ~ ~ ~ {Tags:["5379e4e9-ce2d-410f-8892-7656c48bf616"],ArmorItems:[{},{},{},{id:dirt}]}
execute as @e[tag=5379e4e9-ce2d-410f-8892-7656c48bf616] at @s run setblock ~ ~ ~ diamond_block
tag @e[tag=5379e4e9-ce2d-410f-8892-7656c48bf616] remove 5379e4e9-ce2d-410f-8892-7656c48bf616

execute as @e run function test:_schedule/0c38a194-b4a4-4f2e-8285-6b1ea5bb86cd
# function test:_schedule/f913ea2e-97ad-4b0d-87db-892590b105ee
