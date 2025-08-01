import unittest

import numpy as np
from numpy.testing import assert_almost_equal

import openmdao.api as om
from openmdao.utils.general_utils import env_truthy
from openmdao.utils.testing_utils import use_tempdirs


# Modify class so we can run it standalone.
import dymos as dm
from dymos.examples.brachistochrone.brachistochrone_ode import BrachistochroneODE
from dymos.examples.brachistochrone.test.ex_brachistochrone import brachistochrone_min_time as brach


_DYMOS_2 = env_truthy('DYMOS_2')


@use_tempdirs
class TestCollocationBalanceIndex(unittest.TestCase):
    """
    Test that the indices used in the StateIndependentsComp are as expected.
    """

    def setUp(self):
        dm.options['include_check_partials'] = True

    def tearDown(self):
        dm.options['include_check_partials'] = False

    def test_3_lgl(self):
        """
        Test one 3rd order LGL segment indices

        All nodes are:   [0, 1, 2]
        Input nodes:     [^     ^]
        Solver nodes:    [      ^]
        Indep nodes:     [^      ]
        Of input nodes, solver nodes for fix_initial are: {1}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='gauss-lobatto', num_segments=1, transcription_order=3,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    def test_5_lgl(self):
        """
        Test one 5th order LGL segment indices

        All nodes are:   [0, 1, 2, 3, 4]
        Input nodes:     [^     ^     ^]
        Solver nodes:    [      ^     ^]
        Of input nodes, solver nodes for fix_initial are: {1, 2}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='gauss-lobatto', num_segments=1, transcription_order=5,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    def test_3_lgl_compressed(self):
        """
        Test one 3rd order LGL segment indices

        All nodes are:   [0, 1, 2, 3, 4]
        Input nodes:     [^     ^     ^]
        Solver nodes:    [      ^     ^]
        Indep nodes:     [^            ]
        Of input nodes, solver nodes for fix_initial are: {1, 2}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='gauss-lobatto', num_segments=2, transcription_order=3,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    def test_5_lgl_compressed(self):
        """
        Test two 5th order LGL segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        Input nodes:     [^     ^     ^        ^     ^]
        Solver nodes:    [      ^     ^        ^     ^]
        Indep nodes:     [^                        ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 3, 4}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='gauss-lobatto', num_segments=2, transcription_order=5,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 3, 4})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    def test_3_lgl_uncompressed(self):
        """
        Test two 3rd order LGL segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5]
        Input nodes:     [^     ^  ^     ^]
        Solver nodes:    [      ^        ^]
        Indep nodes:     [^        ^      ]
        Of input nodes, solver nodes for fix_initial are: {1, 3}
        The indep node is just the first one: {0, 2}
        """
        p = brach(transcription='gauss-lobatto', num_segments=2, transcription_order=3,
                  compressed=False, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 3})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0, 2})

    def test_5_lgl_uncompressed(self):
        """
        Test two 5th order LGL segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        Input nodes:     [^     ^     ^  ^     ^     ^]
        Solver nodes:    [      ^     ^        ^     ^]
        Indep nodes:     [^              ^         ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 4, 5}
        The indep node is just the first one in each segment: {0, 3}
        """
        p = brach(transcription='gauss-lobatto', num_segments=2, transcription_order=5,
                  compressed=False, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 4, 5})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0, 3})

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_3_radau(self):
        """
        Test one 3rd order radau segment indices

        All nodes are:   [0, 1, 2, 3]
        Input nodes:     [^  ^  ^  ^]
        Solver nodes:    [   ^  ^  ^]
        Indep nodes:     [^         ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 3}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='radau-ps', num_segments=1, transcription_order=3,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 3})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_5_radau(self):
        """
        Test one 5th order radau segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5]
        Input nodes:     [^  ^  ^  ^  ^  ^]
        Solver nodes:    [   ^  ^  ^  ^  ^]
        Indep nodes:     [^         ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 3, 4, 5}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='radau-ps', num_segments=1, transcription_order=5,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 3, 4, 5})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_3_radau_compressed(self):
        """
        Test one 3rd order radau segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5, 6, 7]
        Input nodes:     [^  ^  ^  ^     ^  ^  ^]
        Solver nodes:    [   ^  ^  ^     ^  ^  ^]
        Indep nodes:     [^            ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 3, 4, 5, 6}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='radau-ps', num_segments=2, transcription_order=3,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 3, 4, 5, 6})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_5_radau_compressed(self):
        """
        Test two 5th order radau segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        Input nodes:     [^  ^  ^  ^  ^  ^     ^  ^  ^   ^   ^]
        Solver nodes:    [   ^  ^  ^  ^  ^     ^  ^  ^   ^   ^]
        Indep nodes:     [^                                   ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
        The indep node is just the first one: {0}
        """
        p = brach(transcription='radau-ps', num_segments=2, transcription_order=5,
                  compressed=True, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0})

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_3_radau_uncompressed(self):
        """
        Test one 3rd order radau segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5, 6, 7]
        Input nodes:     [^  ^  ^  ^  ^  ^  ^  ^]
        Solver nodes:    [   ^  ^  ^     ^  ^  ^]
        Indep nodes:     [^           ^         ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 3, 5, 6, 7}
        The indep node is just the first one: {0, 4}
        """
        p = brach(transcription='radau-ps', num_segments=2, transcription_order=3,
                  compressed=False, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 3, 5, 6, 7})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0, 4})

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_5_radau_uncompressed(self):
        """
        Test two 5th order radau segment indices

        All nodes are:   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        Input nodes:     [^  ^  ^  ^  ^  ^  ^  ^  ^  ^   ^   ^]
        Solver nodes:    [   ^  ^  ^  ^  ^     ^  ^  ^   ^   ^]
        Indep nodes:     [^                 ^                 ]
        Of input nodes, solver nodes for fix_initial are: {1, 2, 3, 4, 5, 7, 8, 9, 10, 11}
        The indep node is just the first one: {0, 6}
        """
        p = brach(transcription='radau-ps', num_segments=2, transcription_order=5,
                  compressed=False, solve_segments='forward', run_driver=True)

        state_indeps_comp = p.model.traj0.phases.phase0.indep_states

        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['solver']), {1, 2, 3, 4, 5, 7, 8, 9, 10, 11})
        self.assertSetEqual(set(state_indeps_comp.state_idx_map['x']['indep']), {0, 6})


@use_tempdirs
class TestCollocationBalanceApplyNL(unittest.TestCase):

    def tearDown(self):
        dm.options['include_check_partials'] = False

    def make_prob(self, transcription, num_segments, transcription_order, compressed):

        p = om.Problem(model=om.Group())

        if transcription == 'gauss-lobatto':
            t = dm.GaussLobatto(num_segments=num_segments,
                                order=transcription_order,
                                compressed=compressed,)
        else:
            t = dm.Radau(num_segments=num_segments,
                         order=transcription_order,
                         compressed=compressed)

        traj = dm.Trajectory()
        phase = dm.Phase(ode_class=BrachistochroneODE, transcription=t)
        p.model.add_subsystem('traj0', traj)
        traj.add_phase('phase0', phase)

        phase.set_time_options(fix_initial=True, duration_bounds=(.5, 10))

        phase.add_state('x', fix_initial=True, fix_final=False, solve_segments='forward')
        phase.add_state('y', fix_initial=True, fix_final=False, solve_segments='forward')

        # Note that by omitting the targets here Dymos will automatically attempt to connect
        # to a top-level input named 'v' in the ODE, and connect to nothing if it's not found.
        phase.add_state('v', fix_initial=True, fix_final=False, solve_segments='forward')

        phase.add_control('theta',
                          continuity=True, rate_continuity=True,
                          units='deg', lower=0.01, upper=179.9)

        phase.add_parameter('g', targets=['g'], units='m/s**2')

        phase.add_boundary_constraint('x', loc='final', equals=10)
        phase.add_boundary_constraint('y', loc='final', equals=5)
        # Minimize time at the end of the phase
        phase.add_objective('time_phase', loc='final', scaler=10)

        p.setup(force_alloc_complex=True)

        phase.set_time_val(initial=0.0, duration=2.0)
        phase.set_state_val('x', [0, 10])
        phase.set_state_val('y', [10, 5])
        phase.set_state_val('v', [0, 9.9])
        phase.set_control_val('theta', [5, 100])
        phase.set_parameter_val('g', 9.80665)

        return p

    def test_apply_nonlinear_gl(self):
        dm.options['include_check_partials'] = True
        p = self.make_prob(transcription='gauss-lobatto', num_segments=3, transcription_order=3,
                           compressed=True)

        p.final_setup()
        p.model.run_apply_nonlinear()  # need to make sure residuals are computed

        expected = np.array([[0., 1., 1., 1.]]).T

        outputs = p.model.traj0.phases.phase0.indep_states.list_outputs(residuals=True, out_stream=None)
        resids = {k: v['resids'] for k, v in outputs}

        assert_almost_equal(resids['states:x'], expected)
        assert_almost_equal(resids['states:v'], expected)

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_apply_nonlinear_radau(self):
        dm.options['include_check_partials'] = True
        p = self.make_prob(transcription='radau-ps', num_segments=3, transcription_order=3,
                           compressed=True)

        p.final_setup()
        p.model.run_apply_nonlinear()  # need to make sure residuals are computed

        expected = np.array([[0., 1., 1., 1., 1., 1., 1., 1., 1., 1.]]).T

        outputs = p.model.traj0.phases.phase0.indep_states.list_outputs(residuals=True, out_stream=None)
        resids = {k: v['resids'] for k, v in outputs}

        assert_almost_equal(resids['states:x'], expected)
        assert_almost_equal(resids['states:v'], expected)

    def test_partials_gl(self):
        dm.options['include_check_partials'] = True
        p = self.make_prob(transcription='gauss-lobatto', num_segments=3, transcription_order=3,
                           compressed=True)

        def assert_partials(data):
            for of, wrt in data:
                if of == wrt:
                    # IndepVarComp like outputs have correct derivs, but FD is wrong so we skip
                    # them (should be some form of -I)
                    continue
                check_data = data[(of, wrt)]
                fwd_abs_error = check_data['abs error'].forward
                if fwd_abs_error is not None:
                    self.assertLess(check_data['abs error'].forward, 1e-8)

        cpd = p.check_partials(compact_print=True, method='fd', out_stream=None)
        data = cpd['traj0.phases.phase0.indep_states']
        assert_partials(data)

    @unittest.skipIf(_DYMOS_2, 'Test invalid for updated Radau transcription')
    def test_partials_radau(self):
        dm.options['include_check_partials'] = True
        p = self.make_prob(transcription='radau-ps', num_segments=3, transcription_order=3,
                           compressed=True)

        def assert_partials(data):
            for of, wrt in data:
                if of == wrt:
                    # IndepVarComp like outputs have correct derivs, but FD is wrong so we skip
                    # them (should be some form of -I)
                    continue
                check_data = data[(of, wrt)]
                fwd_abs_error = check_data['abs error'].forward
                if fwd_abs_error is not None:
                    self.assertLess(check_data['abs error'].forward, 1e-8)

        cpd = p.check_partials(compact_print=True, method='fd', out_stream=None)
        data = cpd['traj0.phases.phase0.indep_states']
        assert_partials(data)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
