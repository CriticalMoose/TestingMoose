#ifndef TESTINGMOOSEAPP_H
#define TESTINGMOOSEAPP_H

#include "MooseApp.h"

class TestingmooseApp;

template<>
InputParameters validParams<TestingmooseApp>();

class TestingmooseApp : public MooseApp
{
public:
  TestingmooseApp(InputParameters parameters);
  virtual ~TestingmooseApp();

  static void registerApps();
  static void registerObjects(Factory & factory);
  static void associateSyntax(Syntax & syntax, ActionFactory & action_factory);
};

#endif /* TESTINGMOOSEAPP_H */
