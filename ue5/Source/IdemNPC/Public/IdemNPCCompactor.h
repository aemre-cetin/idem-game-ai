// Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
// Protected under U.S. Patent Application No. 64/148,668.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "IdemNPCCompactor.generated.h"

/**
 * Lightweight entity state representation for massive crowd / NPC simulation in UE5.
 */
USTRUCT(BlueprintType)
struct IDEMNPC_API FIdemEntityState
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IdemNPC")
	int32 EntityId = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IdemNPC")
	FVector Position = FVector::ZeroVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IdemNPC")
	float Health = 100.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IdemNPC")
	float ThreatScore = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IdemNPC")
	bool bIsActive = true;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IdemNPC")
	int32 CustomState = 0;
};

/**
 * In-place Idempotent Permutations Blueprint Library for Unreal Engine 5.
 * Eliminates memory reallocations, TArray::RemoveAt shifting, and frame stutters.
 */
UCLASS()
class IDEMNPC_API UIdemNPCBlueprintLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/**
	 * Consolidates all active NPCs in-place to the front of the array [0, ActiveCount-1]
	 * using 2-cycle involution transpositions (pi(pi(x)) == x).
	 * Preserves TArray memory buffer, auxiliary memory allocation = 0 Bytes.
	 *
	 * @param Entities In-out array of entity states to compact in-place.
	 * @return The number of active entities consolidated in the prefix.
	 */
	UFUNCTION(BlueprintCallable, Category = "IdemNPC|Compaction")
	static int32 CompactActiveNPCsInPlace(UPARAM(ref) TArray<FIdemEntityState>& Entities);

	/**
	 * Partitions the Top-K highest threat score entities in-place into prefix [0, K-1]
	 * without allocating temporary sort buffers.
	 *
	 * @param Entities In-out array of entities.
	 * @param K The number of top threat entities to retain.
	 * @return Clamped value of K.
	 */
	UFUNCTION(BlueprintCallable, Category = "IdemNPC|Compaction")
	static int32 SelectTopKThreatsInPlace(UPARAM(ref) TArray<FIdemEntityState>& Entities, int32 K);

	/**
	 * C++ Template: Zero-allocation in-place compaction for generic TArray elements.
	 */
	template <typename T, typename PredicateType>
	static int32 CompactGenericInPlace(TArray<T>& Array, PredicateType IsActivePredicate)
	{
		const int32 Total = Array.Num();
		if (Total <= 1)
		{
			return (Total == 1 && IsActivePredicate(Array[0])) ? 1 : 0;
		}

		// Count active entities (K)
		int32 ActiveCount = 0;
		for (int32 i = 0; i < Total; ++i)
		{
			if (IsActivePredicate(Array[i]))
			{
				ActiveCount++;
			}
		}

		if (ActiveCount == 0 || ActiveCount == Total)
		{
			return ActiveCount;
		}

		// In-place 2-cycle involution: swap inactive in [0, ActiveCount-1] with active in [ActiveCount, Total-1]
		int32 Left = 0;
		int32 Right = ActiveCount;

		while (Left < ActiveCount && Right < Total)
		{
			while (Left < ActiveCount && IsActivePredicate(Array[Left]))
			{
				Left++;
			}

			while (Right < Total && !IsActivePredicate(Array[Right]))
			{
				Right++;
			}

			if (Left < ActiveCount && Right < Total)
			{
				// In-place transposition
				Array.SwapMemory(Left, Right);
				Left++;
				Right++;
			}
		}

		return ActiveCount;
	}
};

