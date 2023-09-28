//==================================================================================================
/*!
  @file

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <simd_test.hpp>
#include <boost/simd/pack.hpp>
#include <boost/simd/constant/false.hpp>
#include <boost/simd/constant/true.hpp>
#include <boost/simd/function/bitwise_select.hpp>
#include <boost/simd/function/plus.hpp>
#include <boost/simd/function/multiplies.hpp>
#include <boost/simd/function/is_odd.hpp>
#include <boost/simd/function/is_gtz.hpp>
#include <boost/simd/meta/cardinal_of.hpp>

template <typename T, int N, typename Env>
void test(Env& $)
{
  namespace bs = boost::simd;
  using p_t = bs::pack<T, N>;

  T a1[N], a2[N], a3[N], b[N];
  for(int i = 0; i < N; ++i)
  {
    a1[i] = (i%2) ? T(1) : T(0);
    a2[i] = (i%2) ? T(i+N) : T(-(i+N));
    a3[i] = (i%2) ? T(i+2*N) : T(-(i+2*N));
    b[i] = bs::bitwise_select(a1[i], a2[i], a3[i]);
  }
  p_t aa1(&a1[0], &a1[0]+N);
  p_t aa2(&a2[0], &a2[0]+N);
  p_t aa3(&a3[0], &a3[0]+N);
  p_t bb(&b[0], &b[0]+N);
  STF_EQUAL(bs::bitwise_select(aa1, aa2, aa3), bb);
}

STF_CASE_TPL("Check bitwise_select on pack" , STF_NUMERIC_TYPES)
{
  namespace bs = boost::simd;
  using p_t = bs::pack<T>;
  static const std::size_t N = bs::cardinal_of<p_t>::value;
  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}
