// Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
// Protected under U.S. Patent Application No. 64/148,668.

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class FIdemNPCModule : public IModuleInterface
{
public:
	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};

