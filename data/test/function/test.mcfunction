execute as @p at @s positioned ^ ^2 ^5 run summon armor_stand ~ ~ ~ {Tags:["a6d14492-4211-47b6-8246-0b4d9a8fdc73","yes"],ArmorItems:[{},{},{},{id:dirt}]}
execute as @e[tag=a6d14492-4211-47b6-8246-0b4d9a8fdc73] at @s anchored eyes run particle totem_of_undying ~ ~ ~ 1 1 1 0.01 100 normal @a
tag @e[tag=a6d14492-4211-47b6-8246-0b4d9a8fdc73] remove a6d14492-4211-47b6-8246-0b4d9a8fdc73

# tp @s ~ ~5 ~
say lol xd

execute as @p at @s run summon armor_stand ~ ~ ~ {Tags:["a2abe5d2-e73c-425e-a328-b0db87e68594"],ArmorItems:[{},{},{},{id:dirt}]}
execute as @e[tag=a2abe5d2-e73c-425e-a328-b0db87e68594] at @s run setblock ~ ~ ~ diamond_block
tag @e[tag=a2abe5d2-e73c-425e-a328-b0db87e68594] remove a2abe5d2-e73c-425e-a328-b0db87e68594

execute as @e run function test:_schedule/4ddbedfd-fa00-4569-90d8-d4708f0e895b
# function test:_schedule/b700a5d9-9166-4fae-9df3-ebced8fa86c7
