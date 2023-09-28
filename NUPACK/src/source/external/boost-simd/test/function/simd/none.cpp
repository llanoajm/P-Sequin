//==================================================================================================
/**
  Copyright 2016 NumScale SAS

  Distributed under the Boost Software License, Version 1.0.
  (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)
**/
//==================================================================================================
#include <boost/simd/function/none.hpp>
#include <boost/simd/function/splatted.hpp>
#include <boost/simd/pack.hpp>
#include <boost/simd/logical.hpp>
#include <simd_test.hpp>

namespace bs = boost::simd;

template <typename T, std::size_t N, typename Env>
void test(Env& $)
{
  using p_t = bs::pack<T, N>;

  T a1[N], a2[N];
  bs::logical<T> b = true,  c = true;
  for(std::size_t i = 0; i < N; ++i)
  {
    a1[i] = (i%2) ? T(i) : T(-i);
    a2[i] = (i%2) ? T(i+1) : T(-i*2+1);
    b = b && a1[i] == 0;
    c = c && a2[i] == 0;
  }
  p_t aa1(&a1[0], &a1[0]+N);
  p_t aa2(&a2[0], &a2[0]+N);

  STF_EQUAL(bs::none(aa1), b);
  STF_EQUAL(bs::none(aa2), c);

  STF_EQUAL(bs::splatted_(bs::none)(aa1), (bs::pack<bs::logical<T>,N>(b)) );
  STF_EQUAL(bs::splatted_(bs::none)(aa2), (bs::pack<bs::logical<T>,N>(c)) );
}

STF_CASE_TPL("Check none on pack" , STF_NUMERIC_TYPES)
{
  static const std::size_t N = bs::pack<T>::static_size;

  test<T, N>($);
  test<T, N/2>($);
  test<T, N*2>($);
}
