#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import re

base = '''[GlobalParams]
  block = 0
[]

[Mesh]
  type = GeneratedMesh
  dim = 2
  distribution = DEFAULT
  elem_type = QUAD4
  nx = 250
  ny = 250
  nz = 0
  xmin = 0
  xmax = 250
  ymin = 0
  ymax = 250
  zmin = 0
  zmax = 0
[]

[Variables]
  [./cr]
    # Molar fraction Cr
    order = FIRST
    family = LAGRANGE
  [../]
  [./ni]
    # Molar fraction Ni
    order = FIRST
    family = LAGRANGE
  [../]
  [./E_cr]
    # Cr local energy
    order = FIRST
    family = LAGRANGE
  [../]
  [./E_ni]
    # Ni local energy
    order = FIRST
    family = LAGRANGE
  [../]
[]

[ICs]
  [./randomCr]
    type = RandomIC
    variable = cr
    min = xxCRLOxx
    max = xxCRHIxx
  [../]
  [./randomNi]
    type = RandomIC
    variable = ni
    min = xxNILOxx
    max = xxNIHIxx
  [../]
[]

[BCs]
  # Periodic boundary conditions
  [./Periodic]
    [./c_bcs]
      auto_direction = 'x y'
    [../]
  [../]
[]

[Kernels]
  [./w_dot_cr]
    variable = E_cr
    v = cr
    type = CoupledTimeDerivative
  [../]
  [./w_dot_ni]
    variable = E_ni
    v = ni
    type = CoupledTimeDerivative
  [../]
  [./coupled_res_cr]
    variable = E_cr
    type = SplitCHWRes
    mob_name = M_cr
  [../]
  [./coupled_res_ni]
    variable = E_ni
    type = SplitCHWRes
    mob_name = M_ni
  [../]
  [./coupled_parsed_cr]
    variable = cr
    type = SplitCHParsed
    f_name = f_loc_cr
    mob_name = M_cr
    kappa_name = kappa_cr
    w = E_cr
  [../]
  [./coupled_parsed_ni]
    variable = ni
    type = SplitCHParsed
    f_name = f_loc_ni
    mob_name = M_ni
    kappa_name = kappa_ni
    w = E_ni
  [../]
[]

[Materials]
  [./kappa]
    type = GenericFunctionMaterial
    prop_names = 'kappa_cr kappa_ni'
    prop_values = '1.23899e+3*6.24150934e+18*1e-27 xxKNIxx*6.24150934e+18*1e-27'
  [../]
  [./mobility_cr]
    type = DerivativeParsedMaterial
    f_name = M_cr
    args = 'cr ni'
    constant_names = 'T Q R nm_m eV_J d'
    constant_expressions = '575 246000 8.314 1e+09 6.24150934e+18 1e-27'
    function = 'nm_m^2/eV_J/d*((cr*0.19*exp(-Q/R/T)) / (2*18600 - 4*R*T))'
  [../]
  [./mobility_ni]
    type = DerivativeParsedMaterial
    f_name = M_ni
    args = 'cr ni'
    constant_names = 'T Q R nm_m eV_J d'
    constant_expressions = '575 245800 8.314 1e+09 6.24150934e+18 1e-27'
    function = 'nm_m^2/eV_J/d*abs((ni*1.4*exp(-Q/R/T)) / (2*(-957-1.287*T + (-5225-2.319*T)*(1-cr-2*ni)) - 4*R*T))'
  [../]
  [./local_energy_cr]
    type = DerivativeParsedMaterial
    f_name = f_loc_cr
    args = 'cr ni'
    constant_names = 'f0 A1 A2 A3 A4 A5
                         B1 B2 B3 B4 B5
                         C1 C2 C3 C4
                         D1 D2 D3 D4
                         E1 E2 E3 E4
                         F1 F2 F3 F4
                         eV_J d'
    constant_expressions = '-2.83880e+04 -8.41700e+03  3.94880e+04 -2.57680e+04 -2.18875e+05  3.40064e+05 2.27150e+05
                            -2.10367e+06  9.21503e+06 -1.91016e+07  1.50997e+07 -2.93900e+03  1.62750e+04 1.39360e+04
                             1.39230e+04  1.02000e+03  1.36120e+04  1.21040e+04  1.37500e+04 -2.04700e+03 1.04580e+04
                             1.11170e+04  9.12300e+03 -1.17870e+04  7.71300e+03  7.12800e+03  2.79000e+02 6.24150934e+18 1e-27'
    function = 'd*eV_J*(f0 + A1*ni + A2*ni^2 + A3*ni^3 + A4*ni^4 + A5*ni^5 + B1*cr + B2*cr^2 + B3*cr^3 + B4*cr^4 + B5*cr^5 +  C1*cr*ni + C2*cr^2*ni + C3*cr^3*ni + C4*cr^4*ni + D1*cr*ni^2 + D2*cr^2*ni^2 + D3*cr^3*ni^2 + D4*cr^4*ni^2 + E1*cr*ni^3 + E2*cr^2*ni^3 + E3*cr^3*ni^3 + E4*cr^4*ni^3 + F1*cr*ni^4 + F2*cr^2*ni^4 + F3*cr^3*ni^4 + F4*cr^4*ni^4)'
    derivative_order = 2
  [../]
  [./local_energy_ni]
    type = DerivativeParsedMaterial
    f_name = f_loc_ni
    args = 'cr ni'
    constant_names = 'f0 A1 A2 A3 A4 A5
                         B1 B2 B3 B4 B5
                         C1 C2 C3 C4
                         D1 D2 D3 D4
                         E1 E2 E3 E4
                         F1 F2 F3 F4
                         eV_J d'
    constant_expressions = '-3.48770e+04  2.68988e+05 -2.37323e+06  9.98652e+06 -2.01053e+07 1.55955e+07 -1.27590e+04
                             1.09468e+05 -4.29605e+05  7.11555e+05 -3.91682e+05 -1.70000e+01 2.98700e+03 -5.10000e+03
                            -7.76700e+03  1.61410e+04  1.35380e+04  1.17850e+04  1.19660e+04 1.51950e+04  1.41530e+04
                             8.14600e+03  1.32640e+04  1.30210e+04  1.30300e+04  9.09900e+03 1.25320e+04  6.24150934e+18 1e-27'
    function = 'd*eV_J*(f0 + A1*ni + A2*ni^2 + A3*ni^3 + A4*ni^4 + A5*ni^5 + B1*cr + B2*cr^2 + B3*cr^3 + B4*cr^4 + B5*cr^5 +  C1*cr*ni + C2*cr^2*ni + C3*cr^3*ni + C4*cr^4*ni + D1*cr*ni^2 + D2*cr^2*ni^2 + D3*cr^3*ni^2 + D4*cr^4*ni^2 + E1*cr*ni^3 + E2*cr^2*ni^3 + E3*cr^3*ni^3 + E4*cr^4*ni^3 + F1*cr*ni^4 + F2*cr^2*ni^4 + F3*cr^3*ni^4 + F4*cr^4*ni^4)'
    derivative_order = 2
  [../]
[]

[Preconditioning]
  [./coupled]
    type = SMP
    full = true
  [../]
[]

[Executioner]
  type = Transient
  solve_type = NEWTON
  l_max_its = 30
  l_tol = 1e-6
  nl_max_its = 50
  nl_abs_tol = 1e-9
  end_time = 3144960000
  [./TimeStepper]
    type = IterationAdaptiveDT
    dt = 10
    cutback_factor = 0.8
    growth_factor = 1.5
    optimal_iterations = 7
  [../]
  [./Adaptivity]
    coarsen_fraction = 0.1
    refine_fraction = 0.7
    max_h_level = 2
  [../]
[]

[Postprocessors]
  [./step_size]
    type = TimestepSize
  [../]
  [./iterations]
    type = NumNonlinearIterations
  [../]
  [./nodes]
    type = NumNodes
  [../]
  [./evaluations]
    type = NumResidualEvaluations
  [../]
  [./active_time]
    type = RunTime
    time_type = active
  [../]
[]

[Debug]
  show_var_residual_norms = true
[]

[Outputs]
  exodus = true
  console = true
  csv = true
  print_perf_log = true
  output_initial = true
  [./console]
    type = Console
    max_rows = 10
  [../]
[]'''

if len(sys.argv) < 3:
	print 'Usage: python input-builder.py [Ni] [Cr]'
	sys.exit()
else:
	ni = float(sys.argv[1])
	cr = float(sys.argv[2])

filename = 'Fe-%.1fNi-%.1fCr.i'%(ni, cr)
ni /= 100
cr /= 100
fe = (1.0-ni-cr)

T = 575.0
L_FeNi = abs(-957 - 1.287*T + (-5225 - 2.319*T)*(fe-ni))
K_Ni = 0.5 * 0.365**2 * L_FeNi

base = base.split('\n')

base = [re.sub(r'''xxCRLOxx''', '%.3f'%(cr-0.005), line) for line in base]
base = [re.sub(r'''xxCRHIxx''', '%.3f'%(cr+0.005), line) for line in base]
base = [re.sub(r'''xxNILOxx''', '%.3f'%(ni-0.005), line) for line in base]
base = [re.sub(r'''xxNIHIxx''', '%.3f'%(ni+0.005), line) for line in base]
base = [re.sub(r'''xxKNIxx''', '%.5e'%(K_Ni), line) for line in base]

base = '\n'.join(base)

with open(filename, 'w') as file:
	file.write(base)
