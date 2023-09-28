//==================================================================================================
/*!

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/function/scalar/conj.hpp>
#include <scalar_test.hpp>
#include <boost/simd/detail/dispatch/meta/as_integer.hpp>
#include <boost/simd/constant/inf.hpp>
#include <boost/simd/constant/minf.hpp>
#include <boost/simd/constant/mone.hpp>
#include <boost/simd/constant/nan.hpp>
#include <boost/simd/constant/one.hpp>
#include <boost/simd/constant/zero.hpp>

STF_CASE_TPL (" conj real",  STF_IEEE_TYPES)
{
  namespace bs = boost::simd;

  using bs::conj;

  // return type conformity test
  STF_EXPR_IS(conj(T()), T);

  // specific values tests
#ifndef BOOST_SIMD_NO_INVALIDS
  STF_EQUAL(conj(bs::Inf<T>()), bs::Inf<T>());
  STF_EQUAL(conj(bs::Minf<T>()), bs::Minf<T>());
  STF_IEEE_EQUAL(conj(bs::Nan<T>()), bs::Nan<T>());
#endif
  STF_EQUAL(conj(bs::Mone<T>()), bs::Mone<T>());
  STF_EQUAL(conj(bs::One<T>()), bs::One<T>());
  STF_EQUAL(conj(bs::Zero<T>()), bs::Zero<T>());
} // end of test for floating_

STF_CASE_TPL (" conj unsigned_int",  STF_UNSIGNED_INTEGRAL_TYPES)
{
  namespace bs = boost::simd;

  using bs::conj;
  // return type conformity test
  STF_EXPR_IS(conj(T()), T);


  // specific values tests
  STF_EQUAL(conj(bs::One<T>()), bs::One<T>());
  STF_EQUAL(conj(bs::Zero<T>()), bs::Zero<T>());
} // end of test for unsigned_int_

STF_CASE_TPL (" conj signed_int",  STF_SIGNED_INTEGRAL_TYPES)
{
  namespace bs = boost::simd;

  using bs::conj;

  // return type conformity test
  STF_EXPR_IS(conj(T()), T);

  // specific values tests
  STF_EQUAL(conj(bs::Mone<T>()), bs::Mone<T>());
  STF_EQUAL(conj(bs::One<T>()), bs::One<T>());
  STF_EQUAL(conj(bs::Zero<T>()), bs::Zero<T>());
} // end of test for signed_int_


