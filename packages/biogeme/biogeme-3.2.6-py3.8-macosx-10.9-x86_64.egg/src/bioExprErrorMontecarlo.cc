//-*-c++-*------------------------------------------------------------
//
// File name : bioExprErrorMontecarlo.cc
// @date   Sat May  2 15:05:25 2020
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#include "bioExprErrorMontecarlo.h"
#include <sstream>
#include "bioDebug.h"
#include "bioExceptions.h"

bioExprErrorMontecarlo::bioExprErrorMontecarlo(bioExpression* c) :
  child(c) {
  listOfChildren.push_back(c) ;
}
bioExprErrorMontecarlo::~bioExprErrorMontecarlo() {

}

bioDerivatives* bioExprErrorMontecarlo::getValueAndDerivatives(std::vector<bioUInt> literalIds,
							  bioBoolean gradient,
							  bioBoolean hessian) {

  if (theDerivatives == NULL) {
    theDerivatives = new bioDerivatives(literalIds.size()) ;
  }
  else {
    if (gradient && theDerivatives->getSize() != literalIds.size()) {
      delete(theDerivatives) ;
      theDerivatives = new bioDerivatives(literalIds.size()) ;
    }
  }

  theDerivatives->f = 0.0 ;
  if (gradient) {
    if (hessian) {
      theDerivatives->setDerivativesToZero() ;
    }
    else {
      theDerivatives->setGradientToZero() ;
    }
  }

  if (numberOfDraws == 0) {
    throw bioExceptions(__FILE__,__LINE__,"Cannot perform Monte-Carlo integration with no draws.") ;
  }

  bioUInt n = literalIds.size() ;
  child->setDrawIndex(&drawIndex) ;

  bioReal integral = 0 ;
  bioReal integralSquared = 0 ; 
  for (drawIndex = 0 ; drawIndex < numberOfDraws ; ++drawIndex) {
    bioDerivatives* childResult = child->getValueAndDerivatives(literalIds,gradient,hessian) ;
    integral += childResult->f ;
    integralSquared += childResult->f * childResult->f  ;
  }

  integral /= bioReal(numberOfDraws) ;
  integralSquared /= bioReal(numberOfDraws) ;
  bioReal variance = integralSquared - integral * integral ;
  theDerivatives->f = pow(variance / bioReal(numberOfDraws), 0.5) ;

  if (gradient || hessian) {
    throw bioExceptions(__FILE__,__LINE__,"No derivatives are available for the error on Monte-Carlo integration.") ;
  }
  return theDerivatives ;
}

bioString bioExprErrorMontecarlo::print(bioBoolean hp) const {
  std::stringstream str ; 
  str << "ErrorMontecarlo(" << child->print(hp) << ")";
  return str.str() ;
}
