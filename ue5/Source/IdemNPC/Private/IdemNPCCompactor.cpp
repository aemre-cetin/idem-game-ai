// Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
// Protected under U.S. Patent Application No. 64/148,668.

#include "IdemNPCCompactor.h"

int32 UIdemNPCBlueprintLibrary::CompactActiveNPCsInPlace(TArray<FIdemEntityState>& Entities)
{
	return CompactGenericInPlace(Entities, [](const FIdemEntityState& Entity) {
		return Entity.bIsActive && Entity.Health > 0.0f;
	});
}

int32 UIdemNPCBlueprintLibrary::SelectTopKThreatsInPlace(TArray<FIdemEntityState>& Entities, int32 K)
{
	const int32 Total = Entities.Num();
	if (Total == 0)
	{
		return 0;
	}

	K = FMath::Clamp(K, 1, Total);
	if (K == Total)
	{
		return Total;
	}

	// In-place quickselect / Hoare partition on ThreatScore without allocating auxiliary arrays
	int32 Low = 0;
	int32 High = Total - 1;
	const int32 TargetIdx = K - 1;

	while (Low < High)
	{
		const float Pivot = Entities[High].ThreatScore;
		int32 i = Low;

		for (int32 j = Low; j < High; ++j)
		{
			// Descending order (largest threat scores to the front)
			if (Entities[j].ThreatScore >= Pivot)
			{
				Entities.SwapMemory(i, j);
				i++;
			}
		}
		Entities.SwapMemory(i, High);

		if (i == TargetIdx)
		{
			break;
		}
		else if (i < TargetIdx)
		{
			Low = i + 1;
		}
		else
		{
			High = i - 1;
		}
	}

	return K;
}

