//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/function/repeat_lower_half.hpp>
#include <boost/simd/pack.hpp>
#include <simd_test.hpp>

namespace bs = boost::simd;

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  using p_t = bs::pack<T, N>;

  T a1[N], b[N];
  for(std::size_t i = 0; i < N; ++i)
  {
     a1[i] = (i%3) ? T(i) : T(2*i);
     b[i] = i < N/2 ? a1[i] : a1[i-N/2];
  }

  p_t aa1(&a1[0], &a1[0]+N);
  p_t bb(&b[0], &b[0]+N);

  STF_EQUAL(bs::repeat_lower_half(aa1), bb);
}

STF_CASE_TPL("Check repeat_lower_half on pack", STF_NUMERIC_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;
  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}
