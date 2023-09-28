//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/function/cummin.hpp>
#include <boost/simd/pack.hpp>
#include <simd_test.hpp>

namespace bs = boost::simd;

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  using p_t = bs::pack<T, N>;

  std::array<T,N> a1,b;

  a1[0] = T(1);
  b[0]  = a1[0];

  for(std::size_t i = 1; i < N; ++i)
  {
    a1[i] = i%2 ? T(i*3) : T(i+1);
    b[i]  = std::min(b[i-1], a1[i]);
  }
  p_t aa1(&a1[0], &a1[0]+N);

  STF_ALL_EQUAL(bs::cummin(aa1), b);
}

STF_CASE_TPL("Check min on pack", STF_NUMERIC_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;

  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}
