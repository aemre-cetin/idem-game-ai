// Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
// Protected under U.S. Patent Application No. 64/148,668.

#include "IdemNPCModule.h"

#define LOCTEXT_NAMESPACE "FIdemNPCModule"

void FIdemNPCModule::StartupModule()
{
	UE_LOG(LogTemp, Log, TEXT("IdemNPC: In-Situ Zero-VRAM Game AI Module Loaded. (U.S. Patent App. 64/148,668)"));
}

void FIdemNPCModule::ShutdownModule()
{
	UE_LOG(LogTemp, Log, TEXT("IdemNPC: Module Shutdown."));
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FIdemNPCModule, IdemNPC)

