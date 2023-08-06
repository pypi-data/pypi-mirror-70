//-*-c++-*------------------------------------------------------------
//
// File name : bioExprErrorMontecarlo.h
// @date   Sat May  2 15:05:02 2020
// @author Michel Bierlaire
// @version Revision 1.0
//
//--------------------------------------------------------------------

#ifndef bioExprErrorMontecarlo_h
#define bioExprErrorMontecarlo_h

#include "bioExpression.h"
#include "bioString.h"

class bioExprErrorMontecarlo: public bioExpression {
 public:
  bioExprErrorMontecarlo(bioExpression* c) ;
  ~bioExprErrorMontecarlo() ;
  virtual bioDerivatives* getValueAndDerivatives(std::vector<bioUInt> literalIds,
						 bioBoolean gradient,
						 bioBoolean hessian) ;

  virtual bioString print(bioBoolean hp = false) const ;

 protected:
  bioUInt drawIndex ;
  bioExpression* child ;
};
#endif
