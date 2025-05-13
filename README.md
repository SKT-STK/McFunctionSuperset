a superset language for mcfunction,  
basically like TS for JS but for mcfunction,  
currently allows you to add nbt data to /execute summon and keep execution entity context when using /schedule,  
(/return wont work when used with /execute summon),  
(/schedule must have the timing specified, else it wont work, and also, /schedule clear works as expected),  
you can currently use it by just changing the file extension from .mcfunction to .mcfunctionx or .mcfx for the files in which you wish to use the superset features in and before running /reload running the main.py(copy it to the root of your datapack (next to pack.mcmeta)) script (run *pip install -r .\requirements.txt* first),  
also sometimes it will create its files in completly wrong place and so there is a beautiful boolean flag in the code named "IS_FUCKING_WORKING", just set it to 'True' if it doesnt and then it should (like actually tho). its got a diff way of being 'activated' as well, instead of a diff file extension it looks for ' as @s ' in the same line as the /schedule  

there is also a skt_stk.py file which implements the /schedule part of this superset and adds a fix for /execute anchored eyes. It is specificly designed to work with beet/bolt and comes last in the "pipeline", so add ["skt_stk.schedule", "skt_stk.anchored"] to it  

!!! AT THIS MOMENT VERY VERY EXPERIMENTAL AND PROB HAS A 1_000_000 EDGE-CASES WHERE IT WONT WORK !!!,
