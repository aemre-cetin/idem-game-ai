--!strict
-- Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
-- Protected under U.S. Patent Application No. 64/148,668.
-- IdemNPC: Zero-GC In-Place AI Compactor for Roblox (Luau)

local IdemNPC = {}
IdemNPC.__index = IdemNPC

export type EntityState = {
	id: number,
	x: number,
	y: number,
	z: number,
	health: number,
	threat: number,
	active: boolean,
	state: number,
}

--[=[
	Consolidates all active entities in-place into the prefix [1, activeCount]
	using 2-cycle involution transpositions (pi(pi(x)) == x).
	
	Guarantees:
	- Exactly 0.00 Bytes of Luau table / GC allocation.
	- Eliminates table.remove() O(N) array-shifting penalties.
	- Preserves original table reference.
]=]
function IdemNPC.compactActiveInPlace<T>(array: { T }, isActivePredicate: (T) -> boolean): number
	local total = #array
	if total <= 1 then
		if total == 1 and isActivePredicate(array[1]) then
			return 1
		end
		return 0
	end

	-- Count active entities
	local activeCount = 0
	for i = 1, total do
		if isActivePredicate(array[i]) then
			activeCount += 1
		end
	end

	if activeCount == 0 or activeCount == total then
		return activeCount
	end

	-- In-place 2-cycle involution: swap inactive in [1, activeCount] with active in [activeCount + 1, total]
	local left = 1
	local right = activeCount + 1

	while left <= activeCount and right <= total do
		while left <= activeCount and isActivePredicate(array[left]) do
			left += 1
		end

		while right <= total and not isActivePredicate(array[right]) do
			right += 1
		end

		if left <= activeCount and right <= total then
			-- In-place 2-cycle swap: strictly O(1) scalar register assignment
			local temp = array[left]
			array[left] = array[right]
			array[right] = temp
			left += 1
			right += 1
		end
	end

	return activeCount
end

--[=[
	Partitions the Top-K highest scoring entities in-place into prefix [1, K]
	without allocating auxiliary sort tables or triggering GC sweeps.
]=]
function IdemNPC.selectTopKInPlace<T>(array: { T }, getScore: (T) -> number, k: number): number
	local total = #array
	if total == 0 then
		return 0
	end

	if k > total then
		k = total
	elseif k < 1 then
		k = 1
	end

	if k == total then
		return total
	end

	-- In-place Hoare partition (QuickSelect) descending order
	local low = 1
	local high = total
	local targetIdx = k

	while low < high do
		local pivot = getScore(array[high])
		local i = low

		for j = low, high - 1 do
			if getScore(array[j]) >= pivot then
				local temp = array[i]
				array[i] = array[j]
				array[j] = temp
				i += 1
			end
		end

		local pivotTemp = array[i]
		array[i] = array[high]
		array[high] = pivotTemp

		if i == targetIdx then
			break
		elseif i < targetIdx then
			low = i + 1
		else
			high = i - 1
		end
	end

	return k
end

--[=[
	Modern Luau Raw Buffer Memory Pool for 10,000+ entities.
	Uses Luau's native `buffer` type for true C-like flat memory byte arrays.
	Entity layout (24 bytes):
	  [0..3]   id (u32)
	  [4..7]   x (f32)
	  [8..11]  y (f32)
	  [12..15] z (f32)
	  [16..19] health (f32)
	  [20..23] threat (f32)
]=]
function IdemNPC.createBufferPool(capacity: number)
	local BYTES_PER_ENTITY = 24
	local rawBuffer = buffer.create(capacity * BYTES_PER_ENTITY)

	local pool = {
		buffer = rawBuffer,
		capacity = capacity,
		bytesPerEntity = BYTES_PER_ENTITY,
	}

	function pool:writeEntity(index: number, id: number, x: number, y: number, z: number, health: number, threat: number)
		local offset = (index - 1) * BYTES_PER_ENTITY
		buffer.writeu32(rawBuffer, offset + 0, id)
		buffer.writef32(rawBuffer, offset + 4, x)
		buffer.writef32(rawBuffer, offset + 8, y)
		buffer.writef32(rawBuffer, offset + 12, z)
		buffer.writef32(rawBuffer, offset + 16, health)
		buffer.writef32(rawBuffer, offset + 20, threat)
	end

	function pool:swapEntities(idxA: number, idxB: number)
		if idxA == idxB then return end
		local offA = (idxA - 1) * BYTES_PER_ENTITY
		local offB = (idxB - 1) * BYTES_PER_ENTITY
		for b = 0, BYTES_PER_ENTITY - 1, 4 do
			local valA = buffer.readu32(rawBuffer, offA + b)
			local valB = buffer.readu32(rawBuffer, offB + b)
			buffer.writeu32(rawBuffer, offA + b, valB)
			buffer.writeu32(rawBuffer, offB + b, valA)
		end
	end

	function pool:isAlive(index: number): boolean
		local offset = (index - 1) * BYTES_PER_ENTITY
		return buffer.readf32(rawBuffer, offset + 16) > 0.0
	end

	function pool:compactActiveInPlace(): number
		local total = capacity
		local activeCount = 0
		for i = 1, total do
			if pool:isAlive(i) then
				activeCount += 1
			end
		end

		local left = 1
		local right = activeCount + 1

		while left <= activeCount and right <= total do
			while left <= activeCount and pool:isAlive(left) do
				left += 1
			end
			while right <= total and not pool:isAlive(right) do
				right += 1
			end
			if left <= activeCount and right <= total then
				pool:swapEntities(left, right)
				left += 1
				right += 1
			end
		end

		return activeCount
	end

	return pool
end

return IdemNPC

