set cook_output_dir="C:\Users\Mythical\Downloads\Output"
set uproject="C:\Users\Mythical\Documents\GitHub\Interpose\KevinSpel.uproject"
set engine_dir="C:\unreal_engine_installs\UE_4.22"

cd %engine_dir%
Engine\Build\BatchFiles\RunUAT.bat BuildCookRun -project=%uproject% -noP4 -platform=Win64 -clientconfig=Development -serverconfig=Development -cook -allmaps -stage -archive -archivedirectory=%cook_output_dir%