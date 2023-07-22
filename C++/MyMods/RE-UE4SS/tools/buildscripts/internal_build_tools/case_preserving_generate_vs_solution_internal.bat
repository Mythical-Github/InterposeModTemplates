set BuildMode=%1

IF NOT DEFINED %BuildMode (
set BuildMode=Release
)

cd ../../../VS_Solution
cmake -DCMAKE_BUILD_TYPE=%BuildMode% -DUE4SS_WITH_CASE_PRESERVING_NAME=ON -DRC_FORCE_ALL_STATIC_LIBS= -G"Visual Studio 17 2022" ..
