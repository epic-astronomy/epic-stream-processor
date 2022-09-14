from functools import lru_cache
import numpy as np


class PatchMan:
    @ staticmethod
    @ lru_cache(maxsize=None)
    def get_patch_indices(patch_type='3x3'):
        patch = patch_type
        if type(patch_type) == str:
            patch = int(patch_type.split('x')[0])

        return np.meshgrid(np.arange(patch)-int(patch/2),
                           np.arange(patch)-int(patch/2))

    @ staticmethod
    def get_patch_pixels(pixel, x=None, y=None, patch_type='3x3'):
        xgrid, ygrid = PatchMan.get_patch_indices(patch_type)

        if pixel is not None:
            return (xgrid+pixel[0]).flatten(), (ygrid+pixel[1]).flatten()
        else:
            return (xgrid+x).flatten(), (ygrid+y).flatten()
