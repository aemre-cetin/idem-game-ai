--!strict
-- Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
-- Protected under U.S. Patent Application No. 64/148,668.
-- IdemSwarm: 5,000+ Entity Zero-GC Swarm & Horde Engine for Roblox

local IdemNPC = require(script.Parent.IdemNPC)

local IdemSwarm = {}
IdemSwarm.__index = IdemSwarm

export type SwarmConfig = {
	maxEntities: number,
	moveSpeed: number,
	targetX: number,
	targetY: number,
	targetZ: number,
}

export type SwarmInstance = {
	config: SwarmConfig,
	entities: { IdemNPC.EntityState },
	activeCount: number,
	step: (self: SwarmInstance, dt: number) -> number,
	damageRandom: (self: SwarmInstance, ratio: number) -> (),
}

function IdemSwarm.new(config: SwarmConfig): SwarmInstance
	local entities: { IdemNPC.EntityState } = table.create(config.maxEntities)

	for i = 1, config.maxEntities do
		entities[i] = {
			id = i,
			x = (math.random() - 0.5) * 200,
			y = 0,
			z = (math.random() - 0.5) * 200,
			health = 100,
			threat = 0,
			active = true,
			state = 1,
		}
	end

	local self = {
		config = config,
		entities = entities,
		activeCount = config.maxEntities,
	}

	--[=[
		Executes 1 swarm tick:
		1. Updates active entity positions towards target.
		2. Recomputes threat score based on distance.
		3. In-place compacts active entities (0 GC allocation).
	]=]
	function self:step(dt: number): number
		local tx = self.config.targetX
		local tz = self.config.targetZ
		local speed = self.config.moveSpeed * dt

		local count = self.activeCount
		for i = 1, count do
			local e = self.entities[i]
			if e.active and e.health > 0 then
				local dx = tx - e.x
				local dz = tz - e.z
				local distSq = dx * dx + dz * dz
				if distSq > 0.01 then
					local invDist = 1.0 / math.sqrt(distSq)
					e.x += dx * invDist * speed
					e.z += dz * invDist * speed
					e.threat = 1000.0 / (math.sqrt(distSq) + 1.0)
				end
			else
				e.active = false
			end
		end

		-- In-place idempotent compaction: exactly 0.00 Bytes GC allocated
		self.activeCount = IdemNPC.compactActiveInPlace(self.entities, function(e)
			return e.active and e.health > 0
		end)

		return self.activeCount
	end

	-- Simulates combat damage or death across swarm
	function self:damageRandom(ratio: number)
		for i = 1, self.activeCount do
			if math.random() < ratio then
				self.entities[i].health = 0
				self.entities[i].active = false
			end
		end
	end

	return (self :: any) :: SwarmInstance
end

return IdemSwarm

