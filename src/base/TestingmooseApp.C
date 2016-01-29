#include "TestingmooseApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "ModulesApp.h"
#include "MooseSyntax.h"

template<>
InputParameters validParams<TestingmooseApp>()
{
  InputParameters params = validParams<MooseApp>();

  params.set<bool>("use_legacy_uo_initialization") = false;
  params.set<bool>("use_legacy_uo_aux_computation") = false;
  params.set<bool>("use_legacy_output_syntax") = false;

  return params;
}

TestingmooseApp::TestingmooseApp(InputParameters parameters) :
    MooseApp(parameters)
{
  Moose::registerObjects(_factory);
  ModulesApp::registerObjects(_factory);
  TestingmooseApp::registerObjects(_factory);

  Moose::associateSyntax(_syntax, _action_factory);
  ModulesApp::associateSyntax(_syntax, _action_factory);
  TestingmooseApp::associateSyntax(_syntax, _action_factory);
}

TestingmooseApp::~TestingmooseApp()
{
}

// External entry point for dynamic application loading
extern "C" void TestingmooseApp__registerApps() { TestingmooseApp::registerApps(); }
void
TestingmooseApp::registerApps()
{
  registerApp(TestingmooseApp);
}

// External entry point for dynamic object registration
extern "C" void TestingmooseApp__registerObjects(Factory & factory) { TestingmooseApp::registerObjects(factory); }
void
TestingmooseApp::registerObjects(Factory & factory)
{
}

// External entry point for dynamic syntax association
extern "C" void TestingmooseApp__associateSyntax(Syntax & syntax, ActionFactory & action_factory) { TestingmooseApp::associateSyntax(syntax, action_factory); }
void
TestingmooseApp::associateSyntax(Syntax & /*syntax*/, ActionFactory & /*action_factory*/)
{
}
