//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <simd_test.hpp>
#include <boost/simd/function/sinc.hpp>
#include <boost/simd/pack.hpp>
#include <boost/simd/constant/inf.hpp>
#include <boost/simd/constant/minf.hpp>
#include <boost/simd/constant/nan.hpp>
#include <boost/simd/constant/one.hpp>
#include <boost/simd/constant/mone.hpp>
#include <boost/simd/constant/zero.hpp>
#include <boost/simd/constant/mzero.hpp>
#include <boost/simd/constant/eps.hpp>
#include <boost/simd/constant/mindenormal.hpp>


namespace bs = boost::simd;

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  using p_t = bs::pack<T, N>;

  T a1[N], b[N], c[N];
  for(std::size_t i = 0; i < N; ++i)
  {
    a1[i] = (i%2) ? T(i) : -T(i);
    b[i] = bs::sinc(a1[i]) ;
  }

  p_t aa1(&a1[0], &a1[0]+N);
  p_t bb (&b[0], &b[0]+N);
  p_t cc (&c[0], &c[0]+N);
  STF_ULP_EQUAL(bs::sinc(aa1), bb, 0.5);
}

STF_CASE_TPL("Check sinc on pack" , STF_IEEE_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;

  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}


STF_CASE_TPL(" sinc",  STF_IEEE_TYPES)
{
  namespace bs = boost::simd;
  namespace bd = boost::dispatch;
  using bs::sinc;
  using p_t = bs::pack<T>;

  STF_EXPR_IS(sinc(p_t()),p_t);


  // specific values tests
#ifndef BOOST_SIMD_NO_INVALIDS
  STF_ULP_EQUAL(sinc(bs::Inf<p_t>()), bs::Zero<p_t>(), 0.5);
  STF_ULP_EQUAL(sinc(bs::Minf<p_t>()), bs::Zero<p_t>(), 0.5);
  STF_ULP_EQUAL(sinc(bs::Nan<p_t>()), bs::Nan<p_t>(), 0.5);
#endif
  STF_ULP_EQUAL(sinc(-bs::Pio_2<p_t>()), p_t(2)/(bs::Pi<p_t>()), 0.5);
  STF_ULP_EQUAL(sinc(-bs::Pio_4<p_t>()), bs::sin(bs::Pio_4<p_t>())/(bs::Pio_4<p_t>()), 0.5);
  STF_ULP_EQUAL(sinc(bs::Pio_2<p_t>()),  p_t(2)/(bs::Pi<p_t>()), 0.5);
  STF_ULP_EQUAL(sinc(bs::Pio_4<p_t>()), bs::sin(bs::Pio_4<p_t>())/(bs::Pio_4<p_t>()), 0.5);
  STF_ULP_EQUAL(sinc(bs::Eps<p_t>()), bs::One<p_t>(), 0.5);
  STF_ULP_EQUAL(sinc(bs::Zero<p_t>()), bs::One<p_t>(), 0.5);

#if !defined(BOOST_SIMD_NO_DENORMALS)
  STF_ULP_EQUAL(sinc(bs::Mindenormal<p_t>()), bs::One<p_t>(), 0.5);
#endif
}
