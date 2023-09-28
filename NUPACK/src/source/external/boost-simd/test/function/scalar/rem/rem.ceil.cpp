//==================================================================================================
/*!

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/function/scalar/rem.hpp>
#include <scalar_test.hpp>
#include <boost/simd/detail/dispatch/meta/as_integer.hpp>
#include <boost/simd/constant/inf.hpp>
#include <boost/simd/constant/minf.hpp>
#include <boost/simd/constant/mone.hpp>
#include <boost/simd/constant/nan.hpp>
#include <boost/simd/constant/one.hpp>
#include <boost/simd/constant/zero.hpp>
#include <boost/simd/constant/three.hpp>

STF_CASE_TPL (" rem ceil real",  STF_IEEE_TYPES)
{
  namespace bs = boost::simd;
  namespace bd = boost::dispatch;
  using bs::rem;
  using r_t = decltype(rem(bs::ceil, T(), T()));

  // return type conformity test
  STF_TYPE_IS(r_t, T);

  // specific values tests
#ifndef BOOST_SIMD_NO_INVALIDS
  STF_IEEE_EQUAL(rem(bs::ceil, bs::Inf<T>(), bs::Inf<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(rem(bs::ceil, bs::Minf<T>(), bs::Minf<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(rem(bs::ceil, bs::Nan<T>(), bs::Nan<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(rem(bs::ceil, bs::Inf<T>(), bs::One<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(rem(bs::ceil, bs::One<T>(), bs::Zero<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(rem(bs::ceil, bs::Zero<T>(), bs::Zero<T>()), bs::Nan<T>());
#endif
  STF_EQUAL(rem(bs::ceil, bs::Mone<T>(), bs::Mone<T>()), bs::Zero<T>());
  STF_EQUAL(rem(bs::ceil, bs::One<T>(), bs::One<T>()), bs::Zero<T>());
  STF_IEEE_EQUAL(rem(bs::ceil, bs::One<T>(),bs::Zero<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(rem(bs::ceil, bs::Zero<T>(),bs::Zero<T>()), bs::Nan<T>());
} // end of test for floating_

STF_CASE_TPL (" rem ceil signed_int",  STF_SIGNED_INTEGRAL_TYPES)
{
  namespace bs = boost::simd;
  namespace bd = boost::dispatch;
  using bs::rem;
  using r_t = decltype(rem(bs::ceil, T(), T()));

  // return type conformity test
  STF_TYPE_IS(r_t, T);

  // specific values tests
  STF_EQUAL(rem(bs::ceil, bs::Mone<T>(), bs::Mone<T>()), bs::Zero<T>());
  STF_EQUAL(rem(bs::ceil, bs::One<T>(), bs::One<T>()), bs::Zero<T>());
  STF_EQUAL(rem(bs::ceil, bs::Zero<T>(), bs::Zero<T>()), bs::Zero<T>());
  STF_EQUAL(rem(bs::ceil, bs::Two<T>(), bs::Three<T>()), bs::Mone<T>());
} // end of test for signed_int_

STF_CASE_TPL (" remp ceil fast",  STF_IEEE_TYPES)
{
  namespace bs = boost::simd;
  namespace bd = boost::dispatch;
  using bs::rem;
  using r_t = decltype(rem(bs::ceil, T(), T()));

  // return type conformity test
  STF_TYPE_IS(r_t, T);

  // specific values tests
#ifndef BOOST_SIMD_NO_INVALIDS
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Inf<T>(), bs::Inf<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Minf<T>(), bs::Minf<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Nan<T>(), bs::Nan<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Inf<T>(), bs::One<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Minf<T>(), bs::One<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::One<T>(), bs::Zero<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Zero<T>(), bs::Zero<T>()), bs::Nan<T>());
#endif
  STF_EQUAL(bs::fast_(rem)(bs::ceil, bs::Mone<T>(), bs::Mone<T>()), bs::Zero<T>());
  STF_EQUAL(bs::fast_(rem)(bs::ceil, bs::One<T>(), bs::One<T>()), bs::Zero<T>());
  STF_EQUAL(bs::fast_(rem)(bs::ceil, bs::Two<T>(), bs::Three<T>()), bs::Mone<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Two<T>(), bs::Zero<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Two<T>(), bs::Mzero<T>()), bs::Nan<T>());
  STF_IEEE_EQUAL(bs::fast_(rem)(bs::ceil, bs::Zero<T>(), bs::One<T>()), bs::Zero<T>());
} // end of test for signed_int_
