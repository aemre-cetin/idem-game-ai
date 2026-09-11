"""
Unit Tests for IdemNPC 3D Arena Simulator & In-Situ Swarm Compactor.
Verifies:
1. Massive swarm scaling (1,000 to 10,000 NPCs).
2. Steering dynamics & arena boundary confinement.
3. In-situ involution compaction after mass AoE kill.
4. Mathematical idempotence of the living/dead partition.
"""

import math
import numpy as np
from idempotent_game_ai.arena_simulator import ArenaSimulator


def test_arena_initialization_and_scale():
    for count in [500, 2000, 5000, 10000]:
        sim = ArenaSimulator(num_npcs=count)
        assert sim.active_count == count
        assert sim.positions.shape[0] == 10000
        assert np.all(sim.health[:count] == 100.0)


def test_arena_steering_and_boundaries():
    sim = ArenaSimulator(num_npcs=1000, arena_radius=40.0)
    for _ in range(50):
        res = sim.step(dt=0.016)
        assert res["step"] > 0
        assert res["active_npcs"] == 1000
        # All living entities must stay confined within arena radius
        dist = np.sqrt(sim.positions[:sim.active_count, 0]**2 + sim.positions[:sim.active_count, 2]**2)
        assert np.all(dist <= sim.arena_radius + 0.1)


def test_aoe_kill_and_idempotent_compaction():
    sim = ArenaSimulator(num_npcs=3000, arena_radius=45.0)
    
    # Detonate large AoE blast at center
    blast_res = sim.trigger_aoe_blast(0.0, 0.0, radius=22.0)
    killed = blast_res["killed"]
    assert killed > 0
    assert blast_res["active"] == 3000 - killed
    assert sim.active_count == 3000 - killed
    
    # Verify strict compaction:
    # 1. All entities in [0 .. active_count-1] MUST have health > 0 (strictly living)
    assert np.all(sim.health[:sim.active_count] > 0.0), "Dead entity found in compacted living segment!"
    
    # 2. All entities in [active_count .. 2999] MUST have health == 0 (strictly dead)
    assert np.all(sim.health[sim.active_count:3000] == 0.0), "Living entity found in dead suffix!"
    
    # 3. Mathematical idempotence: second compaction must do 0 swaps
    # If we run compaction again on the already compacted array:
    left = 0
    right = 3000 - 1
    swaps_performed = 0
    new_active = sim.active_count
    while left < new_active and right >= new_active:
        while left < new_active and sim.health[left] > 0:
            left += 1
        while right >= new_active and sim.health[right] <= 0:
            right -= 1
        if left < new_active and right >= new_active:
            swaps_performed += 1
            left += 1
            right -= 1
            
    assert swaps_performed == 0, "Idempotence violated: second compaction performed non-zero swaps!"


def test_behavior_modes_and_engine_presets():
    sim = ArenaSimulator(num_npcs=1000)
    for b in ["swarm", "chase", "battle"]:
        sim.set_behavior(b)
        assert sim.behavior_mode == b
        sim.step(0.016)
        
    for e in ["roblox_luau", "unity_dots", "ue5_mass"]:
        sim.set_engine_preset(e)
        assert sim.engine_mode == e


def test_spatial_modes_and_volume_preservation():
    sim = ArenaSimulator(num_npcs=1500)
    
    # 1. Test IdemSpatial O(N) mode
    sim.set_spatial_mode("idem_spatial")
    assert sim.spatial_mode == "idem_spatial"
    for _ in range(30):
        res = sim.step(0.016)
    assert res["spatial_comparisons"] == 1500 * 3
    assert res["swarm_diameter_m"] > 10.0, "IdemSpatial must maintain physical swarm volume!"

    # 2. Test Traditional N^2 mode
    sim.set_spatial_mode("traditional_n2")
    assert sim.spatial_mode == "traditional_n2"
    res = sim.step(0.016)
    assert res["spatial_comparisons"] == (1500 * 1499) // 2

    # 3. Test Off mode (singularity)
    sim.set_spatial_mode("off")
    assert sim.spatial_mode == "off"
    res = sim.step(0.016)
    assert res["spatial_comparisons"] == 0


if __name__ == "__main__":
    test_arena_initialization_and_scale()
    print("PASS: test_arena_initialization_and_scale")
    test_arena_steering_and_boundaries()
    print("PASS: test_arena_steering_and_boundaries")
    test_aoe_kill_and_idempotent_compaction()
    print("PASS: test_aoe_kill_and_idempotent_compaction")
    test_behavior_modes_and_engine_presets()
    print("PASS: test_behavior_modes_and_engine_presets")
    test_spatial_modes_and_volume_preservation()
    print("PASS: test_spatial_modes_and_volume_preservation")
    print("ALL ARENA TESTS PASSED!")
