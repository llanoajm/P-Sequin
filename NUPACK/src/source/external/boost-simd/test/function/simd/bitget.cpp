//==================================================================================================
/*!
  @file

  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
*/
//==================================================================================================
#include <boost/simd/pack.hpp>
#include <boost/simd/function/bitget.hpp>
#include <boost/simd/meta/cardinal_of.hpp>
#include <simd_test.hpp>

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  namespace bs = boost::simd;
  namespace bd = boost::dispatch;

  using p_t = bs::pack<T, N>;
  using iT  = bd::as_integer_t<T, unsigned>;
  using i_t = bs::pack<iT, N>;

  T a1[N];
  iT a2[N], b[N];
  for(std::size_t i = 0; i < N; ++i)
  {
    a1[i] = T(N+i+1);
    a2[i] =  1;
    b[i] = bs::bitget(a1[i], a2[i]);
   }
  p_t aa1(&a1[0], &a1[0]+N);
  i_t aa2(&a2[0], &a2[0]+N);
  i_t bb(&b[0], &b[0]+N);
  std::cout << aa1 << std::endl;
  std::cout << bb << std::endl;
  std::cout <<bs::bitget(aa1, aa2)<< std::endl;
  STF_EQUAL(bs::bitget(aa1, aa2), bb);
}

STF_CASE_TPL("Check bitget on pack" ,  STF_NUMERIC_TYPES)
{
  namespace bs = boost::simd;
  using p_t = bs::pack<T>;
  static const std::size_t N = bs::cardinal_of<p_t>::value;
  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}
