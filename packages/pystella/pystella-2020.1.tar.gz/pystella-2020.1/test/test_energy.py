__copyright__ = "Copyright (C) 2019 Zachary J Weiner"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


import numpy as np
import pyopencl as cl
import pyopencl.clrandom as clr
import pystella as ps
import pytest

from pyopencl.tools import (  # noqa
    pytest_generate_tests_for_pyopencl as pytest_generate_tests)


@pytest.mark.parametrize("h", [1, 2])
@pytest.mark.parametrize("dtype", [np.float64, np.float32])
def test_scalar_energy(ctx_factory, grid_shape, proc_shape, h, dtype, timing=False):
    if ctx_factory:
        ctx = ctx_factory()
    else:
        ctx = ps.choose_device_and_make_context()

    queue = cl.CommandQueue(ctx)
    rank_shape = tuple(Ni // pi for Ni, pi in zip(grid_shape, proc_shape))
    mpi = ps.DomainDecomposition(proc_shape, h, rank_shape)

    grid_size = np.product(grid_shape)

    nscalars = 2

    def potential(f):
        phi, chi = f[0], f[1]
        return 1/2 * phi**2 + 1/2 * chi**2 + 1/2 * phi**2 * chi**2

    scalar_sector = ps.ScalarSector(nscalars, potential=potential)
    scalar_energy = ps.Reduction(mpi, scalar_sector, rank_shape=rank_shape,
                                 grid_size=grid_size, halo_shape=h)

    pencil_shape = tuple(ni+2*h for ni in rank_shape)
    f = clr.rand(queue, (nscalars,)+pencil_shape, dtype)
    dfdt = clr.rand(queue, (nscalars,)+pencil_shape, dtype)
    lap = clr.rand(queue, (nscalars,)+rank_shape, dtype)

    energy = scalar_energy(queue, f=f, dfdt=dfdt, lap_f=lap, a=np.array(1.))

    kin_test = []
    grad_test = []
    for fld in range(nscalars):
        df_h = dfdt[fld].get()
        rank_sum = np.sum(df_h[h:-h, h:-h, h:-h]**2)
        kin_test.append(1/2 * mpi.allreduce(rank_sum) / grid_size)

        f_h = f[fld].get()
        lap_h = lap[fld].get()

        rank_sum = np.sum(- f_h[h:-h, h:-h, h:-h] * lap_h)
        grad_test.append(1/2 * mpi.allreduce(rank_sum) / grid_size)

    energy_test = {}
    energy_test['kinetic'] = np.array(kin_test)
    energy_test['gradient'] = np.array(grad_test)

    phi = f[0].get()[h:-h, h:-h, h:-h]
    chi = f[1].get()[h:-h, h:-h, h:-h]
    pot_rank = np.sum(potential([phi, chi]))
    energy_test['potential'] = np.array(mpi.allreduce(pot_rank) / grid_size)

    rtol = 1.e-14 if dtype == np.float64 else 1.e-5

    for key, value in energy.items():
        assert np.allclose(value, energy_test[key], rtol=rtol, atol=0), \
            "%s energy inaccurate for nscalars=%d, grid_shape=%s, proc_shape=%s" \
            % (key, nscalars, grid_shape, proc_shape)

    if timing:
        from common import timer
        t = timer(lambda: scalar_energy(queue, a=np.array(1.),
                                        f=f, dfdt=dfdt, lap_f=lap))
        if mpi.rank == 0:
            print("scalar energy took "
                  "%.3f ms for nscalars=%d, grid_shape=%s, proc_shape=%s"
                  % (t, nscalars, grid_shape, proc_shape))


if __name__ == "__main__":
    args = {'grid_shape': (256,)*3, 'proc_shape': (1,)*3,
            'dtype': np.float64, 'h': 2}
    from common import get_exec_arg_dict
    args.update(get_exec_arg_dict())
    test_scalar_energy(None, **args, timing=True)
