// Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
// Protected under U.S. Patent Application No. 64/148,668.

using System;
using Unity.Burst;
using Unity.Collections;
using Unity.Mathematics;

namespace IdemNPC.Runtime
{
    /// <summary>
    /// Blittable agent data structure optimized for Unity Burst compiler and SIMD vectorization.
    /// </summary>
    public struct IdemAgentState
    {
        public int EntityId;
        public float3 Position;
        public float Health;
        public float ThreatScore;
        public bool IsActive;
        public int CustomState;
    }

    /// <summary>
    /// Zero-Allocation In-Place Compaction Engine for Unity.
    /// Operates directly on native memory with strictly 0 GC allocations.
    /// </summary>
    [BurstCompile]
    public static class IdemNPC
    {
        /// <summary>
        /// Consolidates all active agents to the front of the array [0, ActiveCount - 1]
        /// using 2-cycle involution transpositions (pi(pi(x)) == x).
        /// Allocates 0 Bytes of managed heap memory.
        /// </summary>
        /// <param name="agents">NativeArray containing agent states to compact in-place.</param>
        /// <returns>Number of active agents preserved in prefix.</returns>
        [BurstCompile]
        public static int CompactActiveInPlace(ref NativeArray<IdemAgentState> agents)
        {
            int total = agents.Length;
            if (total <= 1)
            {
                return (total == 1 && agents[0].IsActive && agents[0].Health > 0f) ? 1 : 0;
            }

            // Count active entities
            int activeCount = 0;
            for (int i = 0; i < total; ++i)
            {
                if (agents[i].IsActive && agents[i].Health > 0f)
                {
                    activeCount++;
                }
            }

            if (activeCount == 0 || activeCount == total)
            {
                return activeCount;
            }

            // In-place 2-cycle involution
            int left = 0;
            int right = activeCount;

            while (left < activeCount && right < total)
            {
                while (left < activeCount && agents[left].IsActive && agents[left].Health > 0f)
                {
                    left++;
                }

                while (right < total && (!agents[right].IsActive || agents[right].Health <= 0f))
                {
                    right++;
                }

                if (left < activeCount && right < total)
                {
                    // In-place swap
                    IdemAgentState temp = agents[left];
                    agents[left] = agents[right];
                    agents[right] = temp;
                    left++;
                    right++;
                }
            }

            return activeCount;
        }

        /// <summary>
        /// Partitions the Top-K highest threat score entities in-place into prefix [0, K - 1]
        /// without allocating temporary sort buffers or GC memory.
        /// </summary>
        [BurstCompile]
        public static int SelectTopKThreatsInPlace(ref NativeArray<IdemAgentState> agents, int k)
        {
            int total = agents.Length;
            if (total == 0) return 0;

            k = math.clamp(k, 1, total);
            if (k == total) return total;

            int low = 0;
            int high = total - 1;
            int targetIdx = k - 1;

            while (low < high)
            {
                float pivot = agents[high].ThreatScore;
                int i = low;

                for (int j = low; j < high; ++j)
                {
                    if (agents[j].ThreatScore >= pivot)
                    {
                        IdemAgentState temp = agents[i];
                        agents[i] = agents[j];
                        agents[j] = temp;
                        i++;
                    }
                }

                IdemAgentState pivotTemp = agents[i];
                agents[i] = agents[high];
                agents[high] = pivotTemp;

                if (i == targetIdx)
                {
                    break;
                }
                else if (i < targetIdx)
                {
                    low = i + 1;
                }
                else
                {
                    high = i - 1;
                }
            }

            return k;
        }
    }
}

