import traceback
from pathlib import Path
from typing import Union

import anvil
from nbt.nbt import TAG


gtnh_instance_path = Path('~/.local/share/multimc/instances/GT_New_Horizons_2.6.1_Java_8/').expanduser()
mc_world_path = Path('.minecraft/saves/GotG seed')
region_file_path = Path('DIM1/region/r.0.0.mca')
full_path = gtnh_instance_path / mc_world_path / region_file_path

region: anvil.Region = anvil.Region.from_file(str(full_path))

print(region)
print(dir(region))

# Note: 1.7.10 doesn't have a DataVersion,
#   but passing 100 fixes it since it only checks for self.version < _VERSION_17w47a:

# Overwrite get_chunk classmethod (can't pass in NBT in the original implementation)
def from_region_override(cls, region: Union[str, anvil.Region], chunk_x: int, chunk_z: int):
    """
    Creates a new chunk from region and the chunk's X and Z

    Parameters
    ----------
    region
        Either a :class:`anvil.Region` or a region file name (like ``r.0.0.mca``)

    Raises
    ----------
    anvil.ChunkNotFound
        If a chunk is outside this region or hasn't been generated yet
    """
    if isinstance(region, str):
        region = anvil.Region.from_file(region)
    nbt_data = region.chunk_data(chunk_x, chunk_z)
    if nbt_data is None:
        raise anvil.errors.ChunkNotFound(f'Could not find chunk ({chunk_x}, {chunk_z})')

    print(type(nbt_data))
    nbt_data['DataVersion'] = TAG(name='DataVersion', value=100)

    return cls(nbt_data)
anvil.Chunk.from_region = from_region_override

try:
    chunk = anvil.Chunk.from_region(anvil.Chunk, region, 0, 0)
    block = chunk.get_block(2, 66, 5)

    print(region)
    print(block)
    print(block.id)
    # print(block.properties) # 'OldBlock' object has no attribute 'properties'
    print(chunk.get_palette(15))
except Exception as e:
    traceback.print_exc()

print(len(region.data))