// Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
// Protected under U.S. Patent Application No. 64/148,668.

using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;
using Unity.Mathematics;

namespace IdemNPC.Runtime
{
    /// <summary>
    /// Multithreaded Burst-compiled Job simulating tactical decision ticks and movement
    /// for massive crowds with strictly zero garbage collection.
    /// </summary>
    [BurstCompile(CompileSynchronously = true, FloatMode = FloatMode.Fast)]
    public struct IdemSwarmUpdateJob : IJobParallelFor
    {
        [NativeDisableParallelForRestriction]
        public NativeArray<IdemAgentState> Agents;

        [ReadOnly]
        public float3 TargetPosition;

        [ReadOnly]
        public float DeltaTime;

        [ReadOnly]
        public float MoveSpeed;

        public void Execute(int index)
        {
            IdemAgentState agent = Agents[index];

            if (!agent.IsActive || agent.Health <= 0f)
            {
                agent.IsActive = false;
                Agents[index] = agent;
                return;
            }

            // Direction towards target
            float3 toTarget = TargetPosition - agent.Position;
            float distSq = math.lengthsq(toTarget);

            if (distSq > 0.001f)
            {
                float3 dir = math.normalize(toTarget);
                agent.Position += dir * MoveSpeed * DeltaTime;
                // Higher threat when closer to target
                agent.ThreatScore = 1000.0f / (math.sqrt(distSq) + 1.0f);
            }

            Agents[index] = agent;
        }
    }
}

