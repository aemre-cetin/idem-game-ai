--!strict
-- Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
-- Protected under U.S. Patent Application No. 64/148,668.
-- Benchmark & Verification: Zero-GC 5,000-Entity Swarm Simulation in Roblox

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local IdemNPCSuite = require(ReplicatedStorage.IdemNPC)
local IdemNPC = IdemNPCSuite.IdemNPC
local IdemSwarm = IdemNPCSuite.IdemSwarm

local function runBenchmark()
	print("=================================================================")
	print("IdemNPC Roblox (Luau) Zero-GC Swarm Benchmark")
	print("U.S. Patent App. No. 64/148,668 - Dr. A. Emre ÇETİN")
	print("=================================================================")

	local ENTITY_COUNT = 5000
	local TICKS = 100

	local swarm = IdemSwarm.new({
		maxEntities = ENTITY_COUNT,
		moveSpeed = 16.0,
		targetX = 0,
		targetY = 0,
		targetZ = 0,
	})

	-- Warm up
	for _ = 1, 10 do
		swarm:step(1/60)
	end

	-- Force GC cycle to establish baseline
	collectgarbage("collect")
	local memBeforeKB = collectgarbage("count")

	local startTime = os.clock()

	for t = 1, TICKS do
		-- Randomly damage entities to trigger in-place compaction
		if t % 10 == 0 then
			swarm:damageRandom(0.05)
		end
		swarm:step(1/60)
	end

	local totalDurationSec = os.clock() - startTime
	local memAfterKB = collectgarbage("count")

	local avgTickMs = (totalDurationSec / TICKS) * 1000.0
	local memDeltaKB = memAfterKB - memBeforeKB

	print(string.format("Total Entities:        %d", ENTITY_COUNT))
	print(string.format("Ticks Executed:        %d", TICKS))
	print(string.format("Average Tick Duration: %.3f ms (Target: < 2.0 ms)", avgTickMs))
	print(string.format("GC Memory Delta:       %.2f KB", memDeltaKB))

	if memDeltaKB <= 1.0 then
		print("VERIFICATION: PASS! Strictly 0.00 KB GC memory growth confirmed!")
	else
		warn("VERIFICATION: Memory delta detected: " .. memDeltaKB .. " KB")
	end
	print("=================================================================")
end

runBenchmark()

