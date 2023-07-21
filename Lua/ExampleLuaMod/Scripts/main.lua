
local UEHelpers = require("UEHelpers")


function CheckPlayerController()
    PLAYER = FindFirstOf("PlayerController")
    if PLAYER:IsValid() then
        print("player is valid")
    else
        print("player is not valid")
    end
end


function CheckWorld()
    WORLD = UEHelpers.GetWorld()
    if WORLD:IsValid() then
        print("world is valid")
    else
        print("world is not valid")
    end
end


function Summon()
    local PlayerControllerTable = {}
    local AllPlayerControllers = FindAllOf("PlayerController")
    for Index, PlayerController in pairs(AllPlayerControllers) do
        if PlayerController:IsValid() and PlayerController.Player:IsValid() and not PlayerController:HasAnyInternalFlags(EInternalObjectFlags.PendingKill) then
            PlayerControllerTable[PlayerController.Player.ControllerId + 1] = PlayerController
        end
    end
	PlayerPawn = PlayerControllerTable[1].Pawn
    Location = PlayerPawn.RootComponent:K2_GetComponentLocation()
    PlayerPawnLocationRot = PlayerPawn.RootComponent:K2_GetComponentRotation()
    local Rotation = {0.0, 0.0, 0.0}
    local ThingToSpawn = StaticFindObject("/Game/Entity/Howler_BP.Howler_BP_C")

    if ThingToSpawn:IsValid() then
        print("Thing To Spawn Was Valid")
    else
        print("Thing To Spawn Was not Valid")
    end

    WORLD:SpawnActor(ThingToSpawn, Location, Rotation)
    
    SummonedThing = FindFirstOf("Howler_BP_C")
    if SummonedThing:IsValid() then
        print("Summoned Thing Was Valid")
    else
        print("Summoned Thing Was not Valid")
    end
end


RegisterKeyBind(Key.L, function()
	CheckPlayerController()
    CheckWorld()
    ExecuteInGameThread(function()
        Summon()
    end)
end)
