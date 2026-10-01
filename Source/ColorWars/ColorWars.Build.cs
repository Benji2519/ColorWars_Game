// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class ColorWars : ModuleRules
{
	public ColorWars(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"ColorWars",
			"ColorWars/Variant_Platforming",
			"ColorWars/Variant_Platforming/Animation",
			"ColorWars/Variant_Combat",
			"ColorWars/Variant_Combat/AI",
			"ColorWars/Variant_Combat/Animation",
			"ColorWars/Variant_Combat/Gameplay",
			"ColorWars/Variant_Combat/Interfaces",
			"ColorWars/Variant_Combat/UI",
			"ColorWars/Variant_SideScrolling",
			"ColorWars/Variant_SideScrolling/AI",
			"ColorWars/Variant_SideScrolling/Gameplay",
			"ColorWars/Variant_SideScrolling/Interfaces",
			"ColorWars/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
