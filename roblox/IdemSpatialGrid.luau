--!strict
-- Copyright (c) 2026 Dr. A. Emre ÇETİN. All Rights Reserved.
-- Protected under U.S. Patent Application No. 64/148,668.
-- IdemSpatialGrid: Zero-Allocation Spatial Hash Grid for Roblox

local IdemSpatialGrid = {}
IdemSpatialGrid.__index = IdemSpatialGrid

export type SpatialGrid = {
	cellSize: number,
	gridWidth: number,
	totalCells: number,
	head: { number },      -- cellIndex -> first entityIndex
	nextEntity: { number },-- entityIndex -> next entityIndex in same cell
	clear: (self: SpatialGrid) -> (),
	insert: (self: SpatialGrid, entityIndex: number, x: number, z: number) -> (),
	forEachInRadius: (self: SpatialGrid, x: number, z: number, radius: number, callback: (entityIndex: number) -> ()) -> (),
}

function IdemSpatialGrid.new(cellSize: number, gridWidth: number, maxEntities: number): SpatialGrid
	local totalCells = gridWidth * gridWidth
	local head = table.create(totalCells, 0)
	local nextEntity = table.create(maxEntities, 0)

	local self = {
		cellSize = cellSize,
		gridWidth = gridWidth,
		totalCells = totalCells,
		head = head,
		nextEntity = nextEntity,
	}

	-- Clears grid linked lists in O(totalCells) with 0 GC allocations
	function self:clear()
		for i = 1, self.totalCells do
			self.head[i] = 0
		end
	end

	-- Inserts an entity into its spatial cell in O(1) time
	function self:insert(entityIndex: number, x: number, z: number)
		local cx = math.floor(x / self.cellSize) % self.gridWidth
		local cz = math.floor(z / self.cellSize) % self.gridWidth
		if cx < 0 then cx += self.gridWidth end
		if cz < 0 then cz += self.gridWidth end

		local cellIndex = cz * self.gridWidth + cx + 1
		self.nextEntity[entityIndex] = self.head[cellIndex]
		self.head[cellIndex] = entityIndex
	end

	-- Iterates neighbors within search radius without generating table allocations
	function self:forEachInRadius(x: number, z: number, radius: number, callback: (entityIndex: number) -> ())
		local minCx = math.floor((x - radius) / self.cellSize)
		local maxCx = math.floor((x + radius) / self.cellSize)
		local minCz = math.floor((z - radius) / self.cellSize)
		local maxCz = math.floor((z + radius) / self.cellSize)

		for cz = minCz, maxCz do
			local wrappedZ = cz % self.gridWidth
			if wrappedZ < 0 then wrappedZ += self.gridWidth end

			for cx = minCx, maxCx do
				local wrappedX = cx % self.gridWidth
				if wrappedX < 0 then wrappedX += self.gridWidth end

				local cellIndex = wrappedZ * self.gridWidth + wrappedX + 1
				local curr = self.head[cellIndex]
				while curr ~= 0 do
					callback(curr)
					curr = self.nextEntity[curr]
				end
			end
		end
	end

	return (self :: any) :: SpatialGrid
end

return IdemSpatialGrid

