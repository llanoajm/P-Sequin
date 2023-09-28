//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/function/deinterleave.hpp>
#include <boost/simd/pack.hpp>
#include <simd_test.hpp>

namespace bs = boost::simd;

template <typename T, int N, typename Env>
void test(Env&, std::false_type const&)
{}

template <typename T, int N, typename Env>
void test(Env& $, std::true_type const& = {})
{
  using p_t = bs::pack<T, N>;

  T a1[N], a2[N];
  for(int i = 0; i < N; ++i)
  {
    a1[i] = (i%2) ? T(i) : T(2*i);
    a2[i] = (i%2) ? T(i+N) : T(2*(i+N));
  }

  p_t aa1(&a1[0], &a1[0]+N);
  p_t aa2(&a2[0], &a2[0]+N);

  std::array<p_t,2> out = bs::deinterleave(aa1, aa2);
  STF_EQUAL( out[0], bs::deinterleave_first(aa1,aa2)  );
  STF_EQUAL( out[1], bs::deinterleave_second(aa1,aa2) );
}

STF_CASE_TPL("Check deinterleave on pack", STF_NUMERIC_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;
  test<T, N  >($, brigand::bool_<(N>1)>());
  test<T, N/2>($, brigand::bool_<(N>2)>());
  test<T, N*2>($);
}
