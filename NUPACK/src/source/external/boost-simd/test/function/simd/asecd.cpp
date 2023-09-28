//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <simd_test.hpp>
#include <boost/simd/function/asecd.hpp>
#include <boost/simd/pack.hpp>
#include <boost/simd/function/std.hpp>
#include <boost/simd/constant/inf.hpp>
#include <boost/simd/constant/minf.hpp>
#include <boost/simd/constant/nan.hpp>
#include <boost/simd/constant/one.hpp>
#include <boost/simd/constant/mone.hpp>
#include <boost/simd/constant/zero.hpp>
#include <boost/simd/constant/mzero.hpp>
#include <boost/simd/constant/two.hpp>


namespace bs = boost::simd;

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  using p_t = bs::pack<T, N>;

  T a1[N], b[N];
  for(std::size_t i = 0; i < N; ++i)
  {
    a1[i] = i%2 ?N/T(i) : -(N/T(i));
    b[i] = bs::asecd(a1[i]);
  }

  p_t aa1(&a1[0], &a1[0]+N);
  p_t bb (&b[0], &b[0]+N);
  STF_ULP_EQUAL(bs::asecd(aa1), bb, 3.5);
}

STF_CASE_TPL("Check asecd on pack" , STF_IEEE_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;

  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}


STF_CASE_TPL (" asecd",  STF_IEEE_TYPES)
{
  namespace bs = boost::simd;
  namespace bd = boost::dispatch;
  using bs::asecd;
  using p_t = bs::pack<T>;

  using r_t = decltype(asecd(p_t()));

  // return type conformity test
  STF_TYPE_IS(r_t, p_t);

  // specific values tests
#ifndef BOOST_SIMD_NO_INVALIDS
  STF_ULP_EQUAL(asecd(bs::Inf<p_t>()), r_t(90), 0.5);
  STF_ULP_EQUAL(asecd(bs::Minf<p_t>()), r_t(90), 0.5);
  STF_IEEE_EQUAL(asecd(bs::Nan<p_t>()), bs::Nan<r_t>());
  STF_IEEE_EQUAL(asecd(bs::Zero<p_t>()), bs::Nan<r_t>());
#endif

  STF_ULP_EQUAL(asecd(-bs::Two<p_t>()), r_t(120), 0.5);
  STF_ULP_EQUAL(asecd(bs::Mone<p_t>()), r_t(180), 0.5);
  STF_ULP_EQUAL(asecd(bs::One<p_t>()), bs::Zero<r_t>(), 0.5);
  STF_ULP_EQUAL(asecd(bs::Two<p_t>()), r_t(60), 0.5);
}
