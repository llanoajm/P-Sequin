//==================================================================================================
/*!
  @file

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/pack.hpp>
#include <boost/simd/function/is_not_greater_equal.hpp>
#include <boost/simd/meta/cardinal_of.hpp>
#include <boost/simd/logical.hpp>
#include <simd_test.hpp>

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  namespace bs = boost::simd;
  using p_t = bs::pack<T, N>;
  using pl_t = bs::pack<bs::logical<T>, N>;

  T a1[N], a2[N];
  bs::logical<T> b[N];
  for(std::size_t i = 0; i < N; ++i)
  {
     a1[i] = (i%2) ? T(i) : T(2*i);
     a2[i] = (i%2) ? T(i) : T(2*i+1);
     b[i] = bs::is_not_greater_equal(a1[i], a2[i]);
   }
  p_t aa1(&a1[0], &a1[0]+N);
  p_t aa2(&a2[0], &a2[0]+N);
  pl_t bb(&b[0], &b[0]+N);
  STF_EQUAL(bs::is_not_greater_equal(aa1, aa2), bb);
}

STF_CASE_TPL("Check is_not_greater_equal on pack", STF_NUMERIC_TYPES)
{
  namespace bs = boost::simd;
  using p_t = bs::pack<T>;
  static const std::size_t N = bs::cardinal_of<p_t>::value;
  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}

