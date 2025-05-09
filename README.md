a superset language for mcfunction,  
basically like TS for JS but for mcfunction,  
currently allows you to add nbt data to /execute summon and keep execution entity context when using /schedule,  
(/return wont work when used with /execute summon),  
(/schedule must have the timing specified, else it wont work, and also, /schedule clear works as expected),  
you can currently use it by just changing the file extension from .mcfunction to .mcfunctionx or .mcfx for the files in which you wish to use the superset features in and before running /reload running the main.py(copy it to the root of your datapack (next to pack.mcmeta)) script (run *pip install -r .\requirements.txt* first),  

there is also an schedule.py file which implements only the /schedule part of this superset and is specificly designed to work with beet/bolt and comes last in the "pipeline", coundnt be bothered to make it an actual plugin tho, so just create a makefile like: "run: beet build, xcopy schedule.py build /Y /I, cd build && python schedule.py", also, sometimes it will create its files in completly wrong place and so there is a beautiful boolean flag in the code named "IS_FUCKING_WORKING", just set it to 'True' if it doesnt and then it should (like actually tho). its got a diff way of being 'activated' as well, instead of a diff file extension it looks for ' as @s ' in the same line as the /schedule  

!!! AT THIS MOMENT VERY VERY EXPERIMENTAL AND PROB HAS A 1_000_000 EDGE-CASES WHERE IT WONT WORK !!!,
