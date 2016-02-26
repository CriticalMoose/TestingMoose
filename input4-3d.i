# http://mooseframework.org/wiki/MooseTutorials/IronChromiumDecomposition/SimpleTestModel/

[GlobalParams]
  block = 0
[]

[Mesh]
  # 3D, 15nm x 15nm x 15 mesh
  type = GeneratedMesh
  dim = 3
  elem_type = PRISM6
  nx = 15
  ny = 15
  nz = 15
  xmax = 15
  ymax = 15
  zmax = 15
  uniform_refine = 2
[]

[Variables]
  [./c]
    # Molar fraction Cr
    order = FIRST
    family = LAGRANGE
  [../]
  [./w]
    # Chemical potential (eV/mol)
    order = FIRST
    family = LAGRANGE
  [../]
[]

[ICs]
  # Bounding box initial condition at equilibrium concentrations
  [./testIC]
    type = RandomIC
    variable = c
    min = 0.44774
    max = 0.48774
    seed = 210
  [../]
[]

[BCs]
  # Periodic boundary conditions
  [./Periodic]
    [./c_bcs]
      auto_direction = 'x y z'
    [../]
  [../]
[]

[Kernels]
  # Cahn-Hilliard Equation
  [./w_dot]
    variable = w
    v = c
    type = CoupledTimeDerivative
  [../]
  [./coupled_res]
    variable = w
    type = SplitCHWRes
    mob_name = M
  [../]
  [./coupled_parsed]
    variable = c
    type = SplitCHParsed
    f_name = f_loc
    kappa_name = kappa_c
    w = w
  [../]
[]

[Materials]
  # d is a scaling factor that makes it easier for the solution to converge
  # without changing the results. It is defined in each of the first three
  # materials and must have the same value in each one.
  [./kappa]
    # Gradient energy coefficient (eV nm^2/mol)
    # kappa_c*eV_J*nm_m^2*d
    type = GenericFunctionMaterial
    prop_names = kappa_c
    prop_values = 8.125e-16*6.24150934e+18*1e+09^2*1e-27
  [../]
  [./mobility]
    # Mobility (nm^2 mol/eV/s)
    type = DerivativeParsedMaterial
    f_name = M
    args = c
    constant_names = 'Acr    Bcr    Ccr    Dcr Ecr    Fcr    Gcr Afe    Bfe    Cfe    Dfe Efe    Ffe    Gfe nm_m   eV_J   d'
    constant_expressions = '-32.770969 -25.8186669 -3.29612744 17.669757 37.6197853 20.6941796  10.8095813 -31.687117 -26.0291774 0.2286581   24.3633544 44.3334237 8.72990497  20.956768 1e+09      6.24150934e+18          1e-27'
    function = 'nm_m^2/eV_J/d*((1-c)^2*c*10^ (Acr*c+Bcr*(1-c)+Ccr*c*log(c)+Dcr*(1-c)*log(1-c)+ Ecr*c*(1-c)+Fcr*c*(1-c)*(2*c-1)+Gcr*c*(1-c)*(2*c-1)^2) +c^2*(1-c)*10^ (Afe*c+Bfe*(1-c)+Cfe*c*log(c)+Dfe*(1-c)*log(1-c)+ Efe*c*(1-c)+Ffe*c*(1-c)*(2*c-1)+Gfe*c*(1-c)*(2*c-1)^2))'
    derivative_order = 1
    outputs = exodus
  [../]
  [./local_energy]
    # Local free energy function (eV/mol)
    type = DerivativeParsedMaterial
    f_name = f_loc
    args = c
    constant_names = 'A   B   C   D   E   F   G  eV_J  d'
    constant_expressions = '-2.446831e+04 -2.827533e+04 4.167994e+03 7.052907e+03 1.208993e+04 2.568625e+03 -2.354293e+03 6.24150934e+18 1e-27'
    function = 'eV_J*d*(A*c+B*(1-c)+C*c*log(c)+D*(1-c)*log(1-c)+ E*c*(1-c)+F*c*(1-c)*(2*c-1)+G*c*(1-c)*(2*c-1)^2)'
    derivative_order = 2
  [../]
  [./precipitate_indicator]
    # Returns 1/625 if precipitate
    type = ParsedMaterial
    f_name = prec_indic
    args = c
    function = if(c>0.6,0.0016,0)
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
  end_time = 604800
  petsc_options_iname = '-pc_type -ksp_grmres_restart -sub_ksp_type -sub_pc_type -pc_asm_overlap'
  petsc_options_value = 'asm      31                  preonly ilu          1'
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
  [./precipitate_area]
    type = ElementIntegralMaterialProperty
    mat_prop = prec_indic
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
[]
