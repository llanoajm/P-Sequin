//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/function/logical_not.hpp>
#include <boost/simd/constant/false.hpp>
#include <boost/simd/constant/true.hpp>
#include <boost/simd/logical.hpp>
#include <boost/simd/pack.hpp>
#include <simd_test.hpp>

namespace bs = boost::simd;

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  using p_t  = bs::pack<T, N>;
  using pl_t = bs::pack<bs::logical<T>, N>;

  T a1[N];
  bs::logical<T> b[N];

  for(std::size_t i = 0; i < N; ++i)
  {
    a1[i] = (i%2) ? T(i) : T(2*i);
    b[i] = bs::logical_not(a1[i]);
  }

  p_t aa1(&a1[0], &a1[0]+N);
  pl_t bb(&b[0], &b[0]+N);

  STF_EQUAL(bs::logical_not(aa1), bb);
  STF_EQUAL(!aa1, bb);
}

STF_CASE_TPL("Check logical_not on pack", STF_NUMERIC_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;

  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}

template <typename T, std::size_t N, typename Env>
void testl(Env& $)
{
  using lT = bs::logical<T>;
  using pl_t = bs::pack<lT, N>;

  lT a1[N], b[N];

  for(std::size_t i = 0; i < N; ++i)
  {
    a1[i] = (i%2) ? bs::True<lT>() : bs::False<lT>();
    b[i] = bs::logical_not(a1[i]);
  }

  pl_t aa1(&a1[0], &a1[0]+N);
  pl_t bb(&b[0], &b[0]+N);

  STF_EQUAL(bs::logical_not(aa1), bb);
  STF_EQUAL(!aa1, bb);
}

STF_CASE_TPL("Check logical_not on pack of logical", STF_NUMERIC_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;

  testl<T, N>($);
  testl<T, N/2>($);
  testl<T, N*2>($);
}
