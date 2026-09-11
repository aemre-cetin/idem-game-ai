// Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
// Protected under U.S. Patent Application No. 64/148,668.

using UnrealBuildTool;

public class IdemNPC : ModuleRules
{
	public IdemNPC(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
		CppStandard = CppStandardVersion.Cpp20;

		PublicIncludePaths.AddRange(
			new string[] {
				// Module public include directory
			}
		);
				
		PrivateIncludePaths.AddRange(
			new string[] {
				// Module private include directory
			}
		);
			
		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"GameplayTasks"
			}
		);
			
		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				// Internal private dependencies
			}
		);
		
		DynamicallyLoadedModuleNames.AddRange(
			new string[]
			{
			}
		);
	}
}

