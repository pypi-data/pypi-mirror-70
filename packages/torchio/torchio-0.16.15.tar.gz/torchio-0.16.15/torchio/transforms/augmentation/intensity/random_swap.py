from typing import Optional
import torch
import numpy as np
from ....data.subject import Subject
from ....utils import to_tuple
from ....torchio import DATA, TypeTuple, TypeData
from ....data.sampler.sampler import get_random_indices_from_shape, crop
from .. import RandomTransform


class RandomSwap(RandomTransform):
    r"""Randomly swap patches within an image.

    Args:
        patch_size: Tuple of integers :math:`(d, h, w)` to swap patches
            of size :math:`d \times h \times w`.
            If a single number :math:`n` is provided, :math:`d = h = w = n`.
        num_iterations: Number of times that two patches will be swapped.
        p: Probability that this transform will be applied.
        seed: See :py:class:`~torchio.transforms.augmentation.RandomTransform`.
    """
    def __init__(
            self,
            patch_size: TypeTuple = 15,
            num_iterations: int = 100,
            p: float = 1,
            seed: Optional[int] = None,
            ):
        super().__init__(p=p, seed=seed)
        self.patch_size = to_tuple(patch_size)
        self.num_iterations = num_iterations

    @staticmethod
    def get_params():
        # TODO: return locations?
        return

    def apply_transform(self, sample: Subject) -> dict:
        for image_dict in sample.get_images():
            swap(image_dict[DATA][0], self.patch_size, self.num_iterations)
        return sample


def swap(
        tensor: torch.Tensor,
        patch_size: TypeTuple,
        num_iterations: int,
        ) -> None:
    patch_size = to_tuple(patch_size)
    for _ in range(num_iterations):
        first_ini, first_fin = get_random_indices_from_shape(
            tensor.shape,
            patch_size,
        )
        while True:
            second_ini, second_fin = get_random_indices_from_shape(
                tensor.shape,
                patch_size,
            )
            larger_than_initial = np.all(second_ini >= first_ini)
            less_than_final = np.all(second_fin <= first_fin)
            if larger_than_initial and less_than_final:
                continue  # patches overlap
            else:
                break  # patches don't overlap
        first_patch = crop(tensor, first_ini, first_fin)
        second_patch = crop(tensor, second_ini, second_fin).clone()
        insert(tensor, first_patch, second_ini)
        insert(tensor, second_patch, first_ini)


def insert(tensor: TypeData, patch: TypeData, index_ini: np.ndarray) -> None:
    index_fin = index_ini + np.array(patch.shape)
    i_ini, j_ini, k_ini = index_ini
    i_fin, j_fin, k_fin = index_fin
    tensor[i_ini:i_fin, j_ini:j_fin, k_ini:k_fin] = patch
